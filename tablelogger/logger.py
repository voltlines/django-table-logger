import inspect
from datetime import datetime

from tablelogger.config import (LOGGER_FUNC,
                                LOGGER_VALUE_CAST_MAPPING,
                                LOGGER_ADD_LOG_TIME)


def get_instance_type_by_value(value):
    """
    returns full path of instance type
    """
    _type = type(value)
    cls_path = inspect.getmodule(_type).__name__
    function_or_method_path = _type.__name__
    return '{}.{}'.format(cls_path, function_or_method_path)


def log_table(fields):

    def decorator(f):
        def wrapper(sender, instance, created, **kwargs):
            result = f(sender, instance, created, **kwargs)

            log_data = {}
            for field in fields:
                value = getattr(instance, field, None)
                value_type = get_instance_type_by_value(value)
                cast_func = LOGGER_VALUE_CAST_MAPPING.get(value_type)
                if cast_func:
                    value = cast_func(value)
                log_data[field] = value

            # add also table name
            log_data['table_name'] = instance._meta.db_table
            # it will add log_time if enabled
            if LOGGER_ADD_LOG_TIME:
                log_data['log_time'] = int(
                    datetime.utcnow().timestamp() * 1000)

            LOGGER_FUNC(log_data)

            return result
        return wrapper
    return decorator
