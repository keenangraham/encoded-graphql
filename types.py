import json
import requests
from graphene import Field
from graphene import ObjectType
from graphene import Union
from graphene import String
from graphene import List
from graphene import Int
from graphene import Boolean
from graphene.types.resolver import get_default_resolver

from .constants import BASE_URL
from .constants import DEFAULT_PARAMS
from .serializers import convert_fields_to_types


with open('gql/encoded/schemas.json', 'r') as f:
    schemas = json.load(f)


graphql_key_to_schema_key = {}


def key_aware_resolver(attname, default_value, root, info, **args):
    resolver = get_default_resolver()
    attname = graphql_key_to_schema_key.get(attname, attname)
    return resolver(attname, default_value, root, info, **args)


def get_url(url):
    return requests.get(url).json()


def resolve_link(at_id):
    return get_url(
        f'{BASE_URL}{at_id}?{DEFAULT_PARAMS}'
    )


def make_meta_class():
    return type(
        'Meta',
        (object,),
        {
            'default_resolver': key_aware_resolver
        }
    )


def generate_graphql_type(name):
    return type(
        name,
        (ObjectType, ),
        {
            'Meta': make_meta_class()
        }
    )


def generate_graphql_types_from_encoded_schemas(schemas):
    encoded_types = {}
    for name, value in schemas.items():
        encoded_types[name] = generate_graphql_type(name)
    return encoded_types


encoded_types = generate_graphql_types_from_encoded_schemas(schemas)


class EncodedType(Union):

    class Meta:
        types = tuple(encoded_types.values())

    @classmethod
    def resolve_type(cls, instance, info):
        return encoded_types.get(
            instance['@type'][0]
        )


class LinkTo(ObjectType):

    at_id = Field(String)
    embedded = Field(EncodedType)

    def resolve_at_id(self, args):
        return self

    def resolve_embedded(self, args):
        return resolve_link(self)


class Query(ObjectType):
    encoded = Field(LinkTo, at_id=String(required=True))

    def resolve_encoded(self, args, at_id):
        return at_id


mapping = {
    'string': Field(String),
    'array': Field(List(String)),
    'integer': Field(Int),
    'boolean': Field(Boolean),
    'number': Field(Int),
    'arrayLinkTo': Field(List(LinkTo)),
    'linkTo': Field(LinkTo),
}


def update_graph_ql_types_with_schema_fields(encoded_types, schemas):
    for name, values in schemas.items():
        encoded_types[name]._meta.fields.update(
            convert_fields_to_types(
                values,
                graphql_key_to_schema_key,
                mapping
            )
        )

update_graph_ql_types_with_schema_fields(encoded_types, schemas)
