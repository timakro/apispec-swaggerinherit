# apispec-oneofschema

Plugin for apispec adding support for Swagger-style inheritance using `allOf`

## Example

    from apispec import APISpec
    from marshmallow import Schema, fields

    class PetBaseSchema(Schema):
        name = fields.Str(required=True)

    class DogSchema(PetBaseSchema):
        barks = fields.Bool(required=True)

    class CatSchema(PetBaseSchema):
        cuteness = fields.Int(required=True)

    spec = APISpec(
        title='Pet shop',
        version='1.0.0',
        plugins=[
            'apispec.ext.marshmallow',
            'apispec_swaggerinherit'
        ]
    )
    spec.definition('PetBase', schema=PetBaseSchema)
    spec.definition('Dog', schema=DogSchema)
    spec.definition('Cat', schema=CatSchema)
    print(spec.to_yaml())

Resulting OpenAPI spec:

    definitions:
      Cat:
        allOf:
        - {$ref: '#/definitions/PetBase'}
        - properties:
            cuteness: {format: int32, type: integer}
          required: [cuteness]
          type: object
      Dog:
        allOf:
        - {$ref: '#/definitions/PetBase'}
        - properties:
            barks: {type: boolean}
          required: [barks]
          type: object
      PetBase:
        properties:
          name: {type: string}
        required: [name]
        type: object
    info: {title: Pet shop, version: 1.0.0}
    parameters: {}
    paths: {}
    swagger: '2.0'
    tags: []

## Installation

    pip install apispec-swaggerinherit

## License

Copyright (C) 2018 Tim Schumacher

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent per‐mitted by law.
