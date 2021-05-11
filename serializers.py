from graphene import Field
from graphene import String
from graphene import List
from graphene import Int
from graphene import Boolean


def sanitize_field_name(field):
    key = field
    key = key.replace(' ', '_')
    key = key.replace('-', '_')
    key = key.replace('%', 'percent')
    key = key.replace(':', '')
    key = key.replace(',', '')
    key = key.replace('/', '_')
    key = key.replace('(', '')
    key = key.replace(')', '')
    key = key.replace('@', 'at_')
    key = key.lower()
    if key[0].isdigit():
            key = '_' + key
    return key



def convert_fields_to_types(fields, graphql_key_to_schema_key, mapping):
    fields_to_types = {}
    for t in fields:
        sanitized_field = sanitize_field_name(t[0])
        if t[1] == 'object':
            continue
        if t[1] == ['number', 'string']:
            t[1] = 'string'
        if t[1] == ['string', 'null']:
            t[1] = 'string'
        if t[2] is not None:
            mapping_key = 'linkTo'
        elif t[3] is not None:
            mapping_key = 'arrayLinkTo'
        else:
            mapping_key =  t[1]
        graphql_key_to_schema_key[sanitized_field] = t[0]
        fields_to_types[sanitized_field] = mapping[mapping_key]
    if not fields:
        fields_to_types['at_type'] = Field(List(String))
    return fields_to_types
