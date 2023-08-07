import os
import logging

from flask import Flask, request, Response, jsonify, json, Blueprint
from flask_restx import Resource, Api, fields

from werkzeug.exceptions import HTTPException

from services.file_api import FileApi
from services.file_api import FileAlreadyExistsError
from services.file_api import InvalidTypeError

app = Flask(__name__)
blueprint = Blueprint("fileapi", __name__, url_prefix="/")
api = Api(
    blueprint,
    version="1.0",
    title="File API",
    description="File API allowing GET, POST, PUT, DELETE file operations + List Folder",
    doc="/docs/",
)

app.register_blueprint(blueprint)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

get_blob_response_model = api.model(
    "GetBlob", {"status": fields.String(), "data": fields.String()}
)
dir_list_record = api.model(
    "DirListRecord",
    {
        "name": fields.String(),
        "type": fields.String(),
    },
)


get_tree_response_model = api.model(
    "GetTree",
    {
        "status": fields.String(),
        "data": fields.List(fields.Nested(dir_list_record)),
    },
)

get_file_not_found = "File not found"
post_file_already_exists = "File already exists"
put_file_not_found = "File not found"
internal_error = "Internal Error"
list_dir_file_not_found = "File not found"
invalid_type = "Invalid type"


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    # replace the body with JSON
    response.content_type = "application/json"
    return jsonify(status="error", message=e.description), e.code


@app.errorhandler(Exception)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # replace the body with JSON
    logger.exception(e)
    return jsonify(status="error", message=internal_error), 500


@api.route("/blob/<path:path>")
@api.doc(params={"path": "A Path"})
class Blob(Resource):
    @api.response(200, "success", model=get_blob_response_model)
    @api.response(404, get_file_not_found)
    @api.response(422, invalid_type)
    @api.response(500, internal_error)
    def get(self, path):
        """Get file content"""
        try:
            content = FileApi().get_file(path)
            return {"status": "success", "data": content}, 200
        except FileNotFoundError:
            return {"status": "error", "message": get_file_not_found}, 404
        except IsADirectoryError:
            return {"status": "error", "message": invalid_type}, 422

    @api.response(200, "success")
    @api.response(409, post_file_already_exists)
    @api.response(500, internal_error)
    def post(self, path):
        """Create a new file"""
        try:
            FileApi().create_file(path, request.data.decode("utf-8"))
            return {"status": "success"}, 201
        except FileAlreadyExistsError:
            return {
                "status": "error",
                "message": post_file_already_exists,
            }, 409

    @api.response(204, "success")
    @api.response(404, put_file_not_found)
    @api.response(500, internal_error)
    def put(self, path):
        """Update file content"""
        try:
            FileApi().update_file(path, request.data.decode("utf-8"))
            return {"status": "success"}, 204
        except FileNotFoundError:
            return {"status": "error", "message": put_file_not_found}, 404

    @api.response(204, "success")
    @api.response(404, put_file_not_found)
    @api.response(500, internal_error)
    def delete(self, path):
        """Delete file"""
        try:
            FileApi().delete_file(path)
            return {"status": "success"}, 204
        except FileNotFoundError:
            return {"status": "error", "message": "File not found"}, 404


@api.route("/tree/", defaults={"path": ""})
@api.route("/tree/<path:path>")
@api.doc(params={"path": "A Path"})
class Tree(Resource):
    @api.response(200, "success", model=get_tree_response_model)
    @api.response(404, list_dir_file_not_found)
    @api.response(422, invalid_type)
    @api.response(500, internal_error)
    def get(self, path):
        """List Folder"""
        try:
            dirs = FileApi().list_dir(path)
            return {"status": "success", "data": dirs}, 200
        except FileNotFoundError:
            return {"status": "error", "message": list_dir_file_not_found}, 404
        except InvalidTypeError:
            return {"status": "error", "message": invalid_type}, 422


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7777))
    app.run(host="0.0.0.0", debug=True, port=port)
