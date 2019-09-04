from ariadne import QueryType, gql, make_executable_schema
from ariadne.wsgi import GraphQL


type_defs = gql("""
    type Query {
	hello: String!
    }
""")

query = QueryType()

@query.field("hello")
def resolve_hello(*_):
    return "Hello!"

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
