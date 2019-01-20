import inspect
from datetime import datetime

from django.utils.module_loading import import_string

from tablelogger.config import (LOGGER_FUNC,
                                LOGGER_VALUE_CAST_MAPPING,
                                LOGGER_ADD_LOG_TIME,
                                LOGGER_LOG_TIME_IN_MILLISEC)


def get_instance_type_by_value(value):
    """
    returns full path of instance type
    """
    _type = type(value)
    cls_path = inspect.getmodule(_type).__name__
    function_or_method_path = _type.__name__
    return '{}.{}'.format(cls_path, function_or_method_path)


def prepare_log_data(instance, fields):
    log_data = {}

    for field in fields:
        try:
            # check if field has custom converter function
            custom_converter_func = None
            field_args = field.split('|')
            if len(field_args) == 2:
                field, custom_converter_func = (
                    field_args[0], import_string(field_args[1]))

            # check if field has `__` like `company__id`
            relations = field.split('__')
            if len(relations) > 1:
                fake_instance = instance
                for relation in relations:
                    value = getattr(fake_instance, relation, None)
                    fake_instance = value
            else:
                value = getattr(instance, field, None)

            if custom_converter_func:
                # convert value using converter func based on config
                value = custom_converter_func(value)

            # convert value based on config, such as: datetime to timestamp
            value_type = get_instance_type_by_value(value)
            cast_func = LOGGER_VALUE_CAST_MAPPING.get(value_type)
            if cast_func:
                value = cast_func(value)

            log_data[field] = value
        except Exception: # noqa TODO make it more specific and good handling
            log_data[field] = None

    # add table name
    log_data['table_name'] = instance._meta.db_table
    # it will add log_time if enabled
    if LOGGER_ADD_LOG_TIME:
        ts = datetime.utcnow().timestamp()
        if LOGGER_LOG_TIME_IN_MILLISEC:
            ts *= 100
        log_data['log_time'] = int(ts)

    return log_data


def log_table(fields):

    def decorator(f):
        def wrapper(sender, instance, created, **kwargs):
            result = f(sender, instance, created, **kwargs)
            log_data = prepare_log_data(instance, fields)
            LOGGER_FUNC(log_data)
            return result
        return wrapper
    return decorator
