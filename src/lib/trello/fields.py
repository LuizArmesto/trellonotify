# -*- coding: utf-8 -*-

__all__ = ['CollectionField', 'DateTimeField', 'Field', 'JsonField',
        'NotEmptyField', 'ReadOnlyField', 'ObjectField']

import datetime
import json

from .base import Collection

from .utils import camelcase
from .utils import get_model


class BaseField(object):
    def __init__(self, name=None, is_local=False, lazy=False, required=False,
            readonly=True, display=False):
        self.name = name
        self.is_local = is_local
        self.lazy = lazy
        self.required = required
        self.readonly = readonly
        self.display = display

        self.changed = False
        self.received_time = None

    def set_target(self, classname, fieldname):
        self.classname = classname
        self.fieldname = fieldname
        self.target = '__{}_{}'.format(self.classname, self.fieldname)
        if not self.name:
            self.name = camelcase(self.fieldname)


class ReadOnlyField(BaseField):
    def __get__(self, instance, owner):
        if self.lazy and not self.received_time:
            instance.fetch(fields=[self.fieldname])
        return getattr(instance, self.target, None)

    def __set__(self, instance, value):
        raise AttributeError('{} is read only'.format(self.fieldname))


class DateTimeField(ReadOnlyField):
    def __get__(self, instance, owner):
        value = super(DateTimeField, self).__get__(instance, owner)
        if isinstance(value, basestring):
            return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%fZ")
        return value


class Field(ReadOnlyField):
    def __init__(self, readonly=False, *args, **kwargs):
        super(Field, self).__init__(readonly=readonly, *args, **kwargs)

    def __set__(self, instance, value):
        if self.readonly:
            super(Field, self).__set__(instance, value)
        elif self.required and (not bool(value) and
                                not value is False and
                                not value is 0):
            # verify for empty strings/lists/tuples/dicts an None
            # but bypass 0 (int) and False (bool)
            raise ValueError('{} should not be empty'.format(self.fieldname))
        else:
            self.changed = True
            self.received_time = None
            setattr(instance, self.target, value)


class JsonField(Field):
    def __set__(self, instance, value):
        if isinstance(value, basestring):
            value = json.loads(value)
        super(JsonField, self).__set__(instance, value)


class NotEmptyField(Field):
    def __init__(self, required=True, *args, **kwargs):
        super(NotEmptyField, self).__init__(required=required, *args, **kwargs)


class ObjectField(ReadOnlyField):
    def __init__(self, is_local=True, model=None, ref=None, *args, **kwargs):
        self.modelname = model
        self.ref = ref
        super(ObjectField, self).__init__(is_local=is_local, *args, **kwargs)

    def __get__(self, instance, owner):
        value = getattr(instance, self.target, None)
        if not value:
            value = self.create_object(instance)
            setattr(instance, self.target, value)
        return value

    def create_object(self, instance, content=None, lazy=False,
            from_get_method=False, **kwargs):
        model = get_model(self.modelname)
        if content:
            obj = model(instance.trello, content=content, lazy=lazy, **kwargs)
        elif self.ref and not from_get_method:
            # Get id from another field
            id_ = getattr(instance, self.ref)
            obj = model(instance.trello, id_=id_, lazy=lazy, **kwargs)
        else:
            # Get directly from server
            path = '{}/{}'.format(instance.path, self.name)
            content = instance.trello.fetch(path, **kwargs)
            obj = model(instance.trello, content=content, lazy=lazy, **kwargs)
        return obj


class CollectionField(ObjectField):
    def __init__(self, addable=None, removable=False, *args, **kwargs):
        self.addable = bool(addable)
        self.addable_fields = addable
        self.removable = removable
        super(CollectionField, self).__init__(*args, **kwargs)

    def create_object(self, instance, content=None, lazy=False, **kwargs):
        path = '{}/{}'.format(instance.path, self.name)
        model = get_model(self.modelname)
        collection = Collection(instance.trello, model, path=path,
                lazy=lazy, **kwargs)
        return collection

    def add_object(self, instance, obj, from_add_method=False,
                   *args, **kwargs):
        # TODO: should move or create a copy of obj if it already have id?
        # or should raise an exception?
        path = '{}/{}'.format(instance.path, self.name)
        obj.validate()
        params = kwargs
        for addable_field in self.addable_fields:
            param_name = None
            if isinstance(addable_field, tuple):
                param_name = addable_field[0]
                instance_field = addable_field[1]
            else:
                instance_field = addable_field
            field = obj.fields.get(instance_field)
            if not param_name:
                param_name = field.name
            if field:
                params.update({param_name: getattr(obj, field.fieldname)})
        content = instance._post(path, *args, **params)
        obj.deserialize(content)

    def remove_object(self, instance, obj, *args, **kwargs):
        path = '{}/{}/{}'.format(instance.path, self.name, obj.id)
        content = instance._delete(path, *args, **kwargs)
        print content
