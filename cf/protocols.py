import json
import os
from collections import OrderedDict
from importlib import import_module
from cf import fields
from cf.fields import Parser


# dict[str, Parser]: Stores the imported parsers. Access using protocol ID. """
protocols = {}

# dict[str, dict]: Types are defined in the JSON files, and are used as base-classes for parsers.
types = {}

# dict[str, module]: Python modules that have functions that the parsers use.
modules = {}

# set[str]: Used to keep track of which files we've imported.
imported = set()


def import_from(dir):
    """
    Imports all files from specified directory.

    :type dir: str
    :param dir: Name of directory of files to import.
    :rtype: dict[str, Parser]
    :return: Dictionary contains imported parsers.
    """
    for i in os.listdir(dir):
        if i.split('.')[-1].lower() == 'json':
            import_file(dir, i)

    return protocols


def import_file(dir, name):
    """
    Imports a JSON file from a directory, and generates Parser objects (which are then inserted into protocols).

    :type dir: str
    :param dir: Parser file location.
    :type name: str
    :param name: Name of parser JSON file.
    """
    if name in imported: return
    imported.add(name)

    file = json.loads(open(dir + name, 'r').read())

    # If file depends on other files' data, import them first
    for fn in file.get('using', []): import_file(dir, fn)  # possible TODO: remove file dependency

    # Import python code that the Parser will use
    for m in file.get('include_modules', []):
        if m in modules: continue
        modules[m] = import_module('protocols.python.' + m)

    # Import types
    for t in file.get('types', []):
        if 'base' in t:
            t = dict(types[t['base']], **t)
            t.pop('base')
        types[t['name']] = t

    # Generate Parser and put it in protocols
    if 'protocol' in file:
        file['protocol']['children'] = []  # fixme: does not belong here
        protocols[file['protocol']['id']] = Parser(**fix_JSON_data(file['protocol']))


def default_parse(_, __): pass
# dict. Default values for required attributes of parsers.
default = dict(size=0, name='', id='', bit_value=False, str=str, parse=default_parse)


def fix_JSON_data(data):
    """
    Fixes raw JSON data so it can be used by the Parser.

    :type data: dict[str, object]
    :param data: JSON data to be fixed.
    :rtype: dict[str, object]
    :return: Fixed data.
    """

    # Use values from type
    if 'type' in data:
        data = dict(types[data['type']], **data)
        data.pop('type')

    # Add missing attributes that are required
    data = dict(default, **data)

    # yuck ##############################################################
    if 'header' in data:
        data['parse'] = fields.parse_header
        fields_dict = OrderedDict()
        for f in data['header']:
            fields_dict[f['id']] = Parser(**fix_JSON_data(f))
        data['header'] = fields_dict
    if 'field' in data:
        data['field'] = Parser(**fix_JSON_data(data['field']))
    if 'payload' in data:
        data['payload'] = Parser(**fix_JSON_data(data['payload']))
    #####################################################################

    # Replace function names with actual functions from modules.
    for k in data.keys():
        if k.startswith('f_') and not callable(data[k]):
            data[k[2:]] = get_func(data.pop(k))

    return data


def get_func(name):
    """
    Get a function from the one of the imported modules

    :type name: str
    :param name: Name of the function. Format: '<module>.<function>'
    :rtype: function
    :return: The imported function
    :exception: If the module does not exist or does not have the function.
    """
    s = name.split('.', 1)
    return getattr(modules[s[0]], s[1])
