import json
import requests


excluded_keys = [
    '@type',
    '_subtypes'
]


url = 'https://www.encodeproject.org/profiles/?format=json'

data = requests.get(url).json()

types_= list(set(list(data.keys()) + list(data['_subtypes'].keys())) - set(excluded_keys))


def parse_schema(properties):
    schema = []
    for k, v in properties.items():
        link_from =  v.get('items', {}).get('linkFrom')
        if link_from is not None:
            link_from = link_from.split('.')[0]
        schema.append(
            [
                k,
                v['type'],
                v.get('linkTo'),
                link_from or v.get('items', {}).get('linkTo')
            ]
        )
    return schema


schemas = {}
for type_ in types_:
    schemas[type_] = parse_schema(data.get(type_, {}).get('properties', {}))


with open('schemas.json', 'w') as f:
    json.dump(schemas, f)
