from libs.pyinst import InstrumentType, get_instrument_lib
from peewee import CharField, ForeignKeyField, ManyToManyField
from .database import AppModel, db_app, JSONField

# globals
instr_types = [i.name for i in InstrumentType]


# models meta config

class InstrResource(AppModel):
    """
    Instrument sources.
    """
    label = CharField(max_length=32, unique=True)
    instr_type = CharField(max_length=16, choices=[(i, i) for i in instr_types])
    model = CharField(max_length=32)
    brand = CharField(max_length=32)
    class_name = CharField(max_length=32)
    resource_name = CharField(max_length=128)
    params = JSONField()
    details = JSONField()


class InstrMapping(AppModel):
    """
    A map of instrument field to instrument source.
    The former is the role of a instrument in the test set-up. The latter is the specified instrument source.
    """
    field = CharField(max_length=32)
    instr_type = CharField(max_length=16)
    instr_resource = ForeignKeyField(InstrResource, null=True, backref='used_in')


class InstrLib(AppModel):
    """
    A library of all available instrument models.
    """
    model = CharField(max_length=32, unique=True)
    brand = CharField(max_length=32)
    class_name = CharField(max_length=32)
    param_list = JSONField()
    details = JSONField()


class InstrType(AppModel):
    """
    Inst Types.
    """
    name = CharField(max_length=32, unique=True)
    models = ManyToManyField(InstrLib, backref='instr_types')


def create_tables():
    """
    Create tables. If the table to be created already exists, it will be passed.
    Only necessary during initial.
    """
    model_list = [InstrResource, InstrMapping, InstrLib, InstrType, InstrType.models.get_through_model()]
    with db_app:
        db_app.create_tables(model_list, safe=True)
    print("\n=== inst tables created ===")
    print("InstrResource, InstrMapping, InstrLib, InstrType, InstrType.models.get_through_model()")
    refresh_instr_lib()
    create_instr_mapping_fields()


def refresh_instr_lib():
    """
    Establish/refresh instrument lib models, including InstrLib, InstrType and their many-to-many relationship.
    """
    instr_lib = get_instrument_lib()
    instr_type_list = list(instr_lib.keys())
    instr_lib_list = []
    for instr_type in instr_lib:
        instr_lib_list.extend([(i['model'], i['brand'], i['class_name'], i['params'], i['details'])
                              for i in instr_lib[instr_type] if (i['model'], i['brand'], i['class_name'], i['params'],
                                                               i['details']) not in instr_lib_list])
    with db_app.atomic():
        # First remove existing table records
        InstrType.models.get_through_model().delete().execute()
        InstrLib.delete().execute()
        InstrType.delete().execute()
        # Add models/types to InstrLib/InstrType
        InstrLib.replace_many(
            instr_lib_list,
            fields=[InstrLib.model, InstrLib.brand, InstrLib.class_name, InstrLib.param_list, InstrLib.details]
        ).execute()
        InstrType.replace_many([(i,) for i in instr_type_list], fields=[InstrType.name]).execute()
        # Establish relationship
        for i in instr_type_list:
            instr_type = InstrType.get(name=i)
            model_name_list = [m['model'] for m in instr_lib[i]]
            model_list = InstrLib.select().where(InstrLib.model << model_name_list)
            instr_type.models.add(model_list)

        print("\n=== Instrument Lib Refreshed ===")
        print("InstrLib: %d, InstrType: %d, relationships: %d" %
              (len(InstrLib.select()), len(InstrType.select()), len(InstrType.models.get_through_model().select())))

def create_instr_mapping_fields():
    instr_fields = {
        'ATT1': 'VOA',
        'ATT2': 'VOA',
        'ATT3': 'VOA',
        'OPM1': 'OPM',
        'OPM2': 'OPM',
        'OSA': 'OSA',
        'OMA': 'OMA',
        'OTF': 'OTF',
    }
    field_list = list(instr_fields.keys())
    # add/refresh fields and corresponding instr_type, instr_resource will not change
    with db_app.atomic():
        for i in field_list:
            instr_mapping, created = InstrMapping.get_or_create(
                field=i, defaults={'instr_type': instr_fields[i]})
            if not created:
                if instr_mapping.instr_type != instr_fields[i]:
                    instr_mapping.instr_resource = None
                    instr_mapping.instr_type = instr_fields[i]
                    instr_mapping.save()
    # delete fields not exist any more
        InstrMapping.delete().where(~(InstrMapping.field << field_list)).execute()

    print("\n=== Inst Fields Refreshed ===")
    print(field_list)