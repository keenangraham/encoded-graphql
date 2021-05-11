from gql.types import Query
from graphene import Schema

schema = Schema(
    query=Query,
    auto_camelcase=False,
)
