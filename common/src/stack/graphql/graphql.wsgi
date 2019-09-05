from ariadne import QueryType, graphql_sync,make_executable_schema
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify


type_defs = """
    type Query {
	hello: String!
    }
"""

query = QueryType()

@query.field("hello")
def resolve_hello(*_):
    return "Hello!"

schema = make_executable_schema(type_defs, query)
application = Flask(__name__)

@application.route("/", methods=["GET"])
def graphql_playgroud():
    return PLAYGROUND_HTML, 200

@application.route("/", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
