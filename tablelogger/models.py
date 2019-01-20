from tablelogger.config import LOGGER_ENABLED


if LOGGER_ENABLED:
    from tablelogger.signals import * # noqa
