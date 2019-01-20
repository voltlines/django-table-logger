from django.conf import settings
from django.utils.module_loading import import_string


TABLE_LOGGER_CONFIG = getattr(settings, 'TABLE_LOGGER_CONFIG', {})
LOGGER_ENABLED = TABLE_LOGGER_CONFIG.get('LOGGER_ENABLED', False)
LOGGER_ADD_LOG_TIME = TABLE_LOGGER_CONFIG.get('LOGGER_ADD_LOG_TIME', False)
LOGGER_LOG_TIME_IN_MILLISEC = TABLE_LOGGER_CONFIG.get(
    'LOGGER_LOG_TIME_IN_MILLISEC', False)
LOGGER_FUNC = TABLE_LOGGER_CONFIG.get('LOGGER_FUNC')
LOGGER_VALUE_CAST_MAPPING = TABLE_LOGGER_CONFIG.get(
    'LOGGER_VALUE_CAST_MAPPING')
LOGGER_MODELS = TABLE_LOGGER_CONFIG.get('LOGGER_MODELS')

try:
    # import logger function
    LOGGER_FUNC = import_string(LOGGER_FUNC)
except (AttributeError, ImportError):
    # use fallback logger to log stdout
    import logging

    logger = logging.getLogger(__name__)
    LOGGER_FUNC = lambda v: logger.debug(v) # noqa


# convert strings to functions
for typ in LOGGER_VALUE_CAST_MAPPING:
    LOGGER_VALUE_CAST_MAPPING[typ] = import_string(
        LOGGER_VALUE_CAST_MAPPING[typ]
    )
