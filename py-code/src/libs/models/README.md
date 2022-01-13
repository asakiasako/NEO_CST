# a example of instrument model

## Description

This package is a model definition (a usable example) suitable for pyinst. It is based on peewee and uses SQLite as database, which is lightweight, suitable for local use.

## Dependencies

* peewee
    ``` Bash
    pip install peewee
    ```

    If you got an ERROR by doing this (it really happens sometime), go to official site and get the corresponding .whl file for your platform. Then cd to the right directory and run this below:

    ``` Bash
    pip install your-filename.whl
    ```

    Then it will work.

* pyinst

    A instrument library by me.

    ``` Bash
    git@github.com:asakiasako/pyinst.git
    ```

## Config

All you should config is inst_fields in models.py

InstLib and InstType tables are generated automatically, and you should not modifie them directly.

What you will probably do is add/mod/remove instrument resources to/of/from InstResource table, config instrument resources to corresponding fields, and read information from InstLib.

You can get class_name of a instrument in InstResource, so you can create a instrument instance dynamically.

## Tables

* InstReource

    Abstract Instruments.

    columns: label, inst_type, model, brand, class_name, resource_name, params(json), detail, used_in

* InstConfig

    A map of instrument config fields to InstSource instances.

    Data of field and inst_type will generate automatically.

    columns: field, inst_type, instr_resource

* InstLib

    A library of instruments you can use. It is generated automatically from pyinst.

    It is refreshed when package is imported.

    It happens automatically, all you should know is that the data is always up-to-date with pyinst package.

    columns: model, brand, class_name, param_list(json), detail(json), inst_types(list of InstType)

* InstType

    A table of instrument types. It is generated/refreshes automatically, just as above.

    columns: name, models(list of InstLib)

## Initialize

Every time the models package is imported, it will create database tables, if a table is already existing, it will be skipped.

Then InstLib will be refreshed to keep up-to-date with pyinst package.

Finally, it will manage InstConfig to match inst_fields defined in models.py.