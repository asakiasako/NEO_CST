"""
Export all Model classes flat.
Initialise tables for all models.
"""
from . import model_inst, model_config
from .database import db_app
from .model_inst import InstrResource, InstrMapping, InstrLib, InstrType
from .model_config import AppConfig

model_list = [model_inst, model_config]
for i in model_list:
    i.create_tables()
