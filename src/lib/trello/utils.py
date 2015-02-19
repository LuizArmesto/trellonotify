# -*- coding: utf-8 -*-


def camelcase(content):
    buff = ''.join([s.capitalize() for s in content.split('_')])
    return ''.join([buff[0].lower(), buff[1:]])


def get_model(model):
    if isinstance(model, basestring):
        package = __name__.split('.')[:-1]
        module = __import__('.'.join(package + ['models']),
                globals(), locals(), [model])
        return getattr(module, model)
    else:
        return model
