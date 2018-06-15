# apispec-swaggerinherit - Plugin for apispec adding support for Swagger-style
#                          inheritance using `allOf`
# Copyright (C) 2018  Tim Schumacher

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from apispec.ext.marshmallow import swagger

from marshmallow import Schema
std_bases = [Schema]

try:
    from marshmallow_oneofschema import OneOfSchema
    std_bases.append(OneOfSchema)
except ImportError:
    pass


def swaggerinherit_definition_helper(spec, name, schema, definition, **kwargs):
    """Definition helper that modifies the schema definition to make use of
    swagger-style inheritance using `allOf`. Uses the `schema` parameter.
    """
    parents = [b for b in schema.__bases__ if b not in std_bases]
    if not parents:
        return
    ref_path = swagger.get_ref_path(spec.openapi_version.version[0])
    try:
        refs = ['#/{}/{}'.format(ref_path,
                spec.plugins['apispec.ext.marshmallow']['refs'][schema_cls])
                for schema_cls in parents]
    except KeyError:
        raise ValueError("Parent schemas must be added to the spec before the "
                         "child schema")
    child_def = definition.copy()
    for parent in parents:
        for name in parent._declared_fields.keys():
            del child_def['properties'][name]
            try:
                child_def['required'].remove(name)
            except ValueError:
                pass
    if not child_def['required']:
        del child_def['required']
    definition.clear()
    return {
        'allOf': [{'$ref': ref} for ref in refs] + [child_def]
    }


def setup(spec):
    spec.register_definition_helper(swaggerinherit_definition_helper)
