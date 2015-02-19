# -*- coding: utf-8 -*-

__all__ = ['Collection', 'Model']

import json
from datetime import datetime


class ModelMeta(type):
    def __init__(cls, name, bases, dic):
        super(ModelMeta, cls).__init__(name, bases, dic)
        cls.fields = {}
        for fieldname, field in dic.items():
            if hasattr(field, 'set_target'):
                field.set_target(name, fieldname)
                cls.fields.update({fieldname: field})
            if getattr(field, 'display', False):
                cls._display_fieldname = fieldname


class BaseModel(object):
    __metaclass__ = ModelMeta


class Model(BaseModel):

    def __init__(self, trello, id_=None, content=None, lazy=False):
        self.trello = trello
        if content:
            if isinstance(content, basestring):
                content = json.loads(content)
            self.deserialize(content)
        elif id_:
            self.__setattr('id', id_)
            if not lazy:
                fields = [f.name for f in self.external_fields if not f.lazy]
                self.fetch(fields=fields)

    def __eq__(self, other):
        return other._prefix == self._prefix and other.id == self.id

    def __getattr__(self, name):
        if name.startswith('get_'):
            # Methods with the format 'get_fieldname' are redirected to filed's
            # create_object method if it exists.
            fieldname = name[4:]
            field = self.fields.get(fieldname)
            if field and hasattr(field, 'create_object'):
                return lambda *args, **kwargs: field.create_object(
                        self, from_get_method=True, *args, **kwargs)
        elif name.startswith('add_'):
            fieldname = name[4:]
            field = self.fields.get('{}s'.format(fieldname)) or \
                    self.fields.get(fieldname)
            if field and field.addable and hasattr(field, 'add_object'):
                return lambda *args, **kwargs: field.add_object(
                        self, from_add_method=True, *args, **kwargs)
        elif name.startswith('remove_'):
            fieldname = name[7:]
            field = self.fields.get('{}s'.format(fieldname)) or \
                    self.fields.get(fieldname)
            if field and field.removable and hasattr(field, 'remove_object'):
                return lambda *args, **kwargs: field.remove_object(
                        self, from_remove_method=True, *args, **kwargs)
        raise AttributeError("'{}' object has no attribute '{}'".format(
            self.__class__.__name__, name))

    def __repr__(self):
        id_ = getattr(self, 'id', None)
        if not id_ and hasattr(self, 'model'):
            id_ = self.model.__name__
        display = getattr(self, 'display_value', '').encode('ascii', errors='replace')
        return '<{}{} at {:#x}>'.format(self.__class__.__name__,
                ((':' + id_) if id_ else '') + \
                (('(' +  display + ')') if display else ''),
                id(self))

    @property
    def _prefix(self):
        raise NotImplementedError

    __received_time = None

    @property
    def display_value(self):
        return getattr(self, self._display_fieldname, None)

    @property
    def received_time(self):
        return self.__received_time

    @property
    def external_fields(self):
        return [f for f in self.fields.values() if not f.is_local]

    @property
    def external_fieldnames(self):
        return [f.name for f in self.external_fields]

    @property
    def path(self):
        if not self._prefix or not self.id:
            return None
        return '{}/{}'.format(self._prefix, self.id)

    def fetch(self, *args, **kwargs):
        if not self.path:
            return
        path = '{}/{}'.format(self.path, kwargs.pop('path', ''))
        content = self.trello.fetch(path, *args, **kwargs)
        self.__received_time = datetime.now()
        self.deserialize(json.loads(content))

    def _post(self, *args, **kwargs):
        response = self.trello.post(*args, **kwargs)
        return json.loads(response.content)

    def _put(self, *args, **kwargs):
        response = self.trello.put(*args, **kwargs)
        return json.loads(response.content)

    def _delete(self, *args, **kwargs):
        response = self.trello.delete(*args, **kwargs)
        return json.loads(response.content)

    def deserialize(self, values):
        if isinstance(values, list):
            # Sometimes we get a list from post requests
            values = values[0]
        for fieldname, field in self.fields.items():
            # Using 'field.name' instead of 'fieldname' because 'values' keys
            # are camelcase and 'fieldname' uses underscore.
            value = values.get(field.name)
            if value:
                self.__setattr(fieldname, value)

    def serialize(self, all=True):
        # TODO: convert everything to json valid values
        fields = [f for f in self.external_fields
                if (f.changed and not f.readonly) or all]
        dic = {f.name: getattr(self, f.fieldname) for f in fields}
        print dic
        return dic

    def __setattr(self, fieldname, value):
        field = self.fields[fieldname]
        field.received_time = self.__received_time
        field.changed = False
        if hasattr(field, 'create_object'):
            value = field.create_object(self, content=value)
        # Using field.target to be possible set attributes to read-only fields.
        setattr(self, field.target, value)

    def validate(self):  # TODO
        return True


class Collection(Model):
    def __init__(self, trello, model, path=None, content=None, lazy=False,
            **params):
        self.trello = trello
        self.model = model
        self.lazy = lazy
        self.children = {}

        if content:
            self.deserialize(content)
        elif path:
            self._path = path
            if not lazy:
                fields = [f.name for f in model.fields.values()
                        if not f.lazy and not f.is_local]
                self.fetch(fields=fields, **params)

    @property
    def path(self):
        return self._path

    def keys(self):
        return self.children.keys()

    def values(self):
        return self.children.values()

    def items(self):
        return self.children.items()

    def __len__(self):
        return len(self.items())

    def __contains__(self, key):
        return key in self.children or (
                hasattr(key, 'id') and isinstance(key, self.model) and
                    key.id in self.keys())

    def __getitem__(self, key):
        return self.values()[key]

    def __iter__(self):
        return iter(self.values())

    def get_by_id(self, id_):
        return self.children[id_]

    def add(self, child):
        self.children[child.id] = child

    def deserialize(self, values):
        for value in values:
            child = self.model(self.trello, content=value, lazy=self.lazy)
            self.add(child)


class Savable(object):
    def save(self):
        # TODO Validate
        params = self.serialize(False)
        content = self._put(path=self.path, **params)
        self.deserialize(content)


class Deletable(object):  # TODO
    pass
