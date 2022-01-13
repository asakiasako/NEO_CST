"""
All database configs
"""

from peewee import SqliteDatabase, Model, Field
from paths import get_sub_dir
import os.path
import json

class JSONField(Field):
    field_type = 'json'

    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if isinstance(value, str):
            return json.loads(value)
        else:
            return value

db_app = SqliteDatabase(
            os.path.abspath(os.path.join(get_sub_dir('Data'), 'appData.db')), pragmas=(
                            ('cache_size', -1024 * 64),  # 64MB page-cache.
                            ('journal_mode', 'wal'),  # Use WAL-mode (you should always use this!).
                            ('foreign_keys', 1)),
                            field_types={'json': 'json'}
                            )  # Enforce foreign-key constraints.

# base models including configurations
class AppModel(Model):
    class Meta:
        database = db_app
