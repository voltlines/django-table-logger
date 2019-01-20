from django.utils.module_loading import import_string
from django.db.models.signals import post_save

from tablelogger.config import LOGGER_MODELS

POST_SAVE_FUNC_TEMPLATE = """
from tablelogger.logger import log_table
@log_table({fields})
def table_logger_{model_name}(sender, instance, created, **kwargs):
    pass
""" # noqa
POST_SAVE_FUNCS = {}


# register post save signals to related models
for model_path, fields in LOGGER_MODELS.items():
    model_name = model_path.rsplit('.', 1)[1].lower()

    post_save_signal_code = POST_SAVE_FUNC_TEMPLATE.format(
        fields=fields, model_name=model_name
    )
    exec(post_save_signal_code, {}, POST_SAVE_FUNCS)

    key = 'table_logger_{}'.format(model_name)
    func = POST_SAVE_FUNCS[key]

    sender = import_string(model_path)
    post_save.connect(func, sender=sender)
