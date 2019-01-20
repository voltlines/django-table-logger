#  DJANGO TABLE LOGGER #


### What is this repository for? ###

A django package that allows easy logging of table changes to anywhere


### How do I get set up? ###

* Add `tablelogger` into INSTALLED_APPS (bottom)
* Add TABLE_LOGGER_CONFIG properly, see below sample

```
TABLE_LOGGER_CONFIG = {
    'LOGGER_ENABLED': True, (default: False)
    'LOGGER_ADD_LOG_TIME': True, (default: False, will be added as UTC timestamp in milliseconds)
    'LOGGER_FUNC': 'voltlines.core.log_table_change_revision',
    'LOGGER_VALUE_CAST_MAPPING': {
        'django.contrib.gis.geos.point.Point': 'voltlines.core.helpers.convert_point_to_str' # noqa
        'builtins.int': 'builtins.str'
    },
    'LOGGER_MODELS': {
        'voltlines.companies.models.Company': ['name']
        'voltlines.routes.models.Route': ['origin', 'name']
    }
}
```

### How it works? ###

* It binds post_save signal based on LOGGER_MODELS' model name and the fields
* When something changed and once that model saved, your LOGGER_FUNC will be getting
latest table data as a callback
* It will also add the table name as `table_name` in the log data
* If you don't specify a LOGGER_FUNC, you ll see the data as log on stdout (add `tablelogger` into LOGGING)
* BONUS: You can also use `log_table` decorator separately if you wish!


### Example ###

```
In [4]: c = Company.objects.last()

In [5]: c.save()
[11:17:39][DEBUG] tablelogger.config config.py:<lambda>:21 | {'log_time': 1547983059794, 'table_name': 'companies_company', 'name': 'Volt Lines'}

In [6]: c.name = 'Foo Bar'

In [7]: c.save()
[11:17:57][DEBUG] tablelogger.config config.py:<lambda>:21 | {'log_time': 1547983077860, 'table_name': 'companies_company', 'name': 'Foo Bar'}
```
