from flask import Flask, request, Response, jsonify
from services.file_api import FileApi
from services.file_api import FileAlreadyExistsError
from services.file_api import InvalidTypeError

app = Flask(__name__)


@app.route("/blob/<path:path>")
def get_file(path):
    """Get file content"""
    try:
        content = FileApi().get_file(path)
        return Response(content, content_type="application/octet-stream")
    except FileNotFoundError:
        return jsonify(error="File not found"), 404


@app.route("/blob/<path:path>", methods=["PUT"])
def update_file(path):
    """Update file content"""
    try:
        FileApi().update_file(path, request.data)
        return "", 204
    except FileNotFoundError:
        return jsonify(error="File not found"), 404


@app.route("/blob/<path:path>", methods=["POST"])
def create_file(path):
    """Create a new file"""
    try:
        FileApi().create_file(path, request.data)
        return "", 201
    except FileAlreadyExistsError:
        return jsonify(error="File already exists"), 409


@app.route("/blob/<path:path>", methods=["DELETE"])
def delete_file(path):
    """Delete file"""
    try:
        FileApi().delete_file(path)
        return "", 204
    except FileNotFoundError:
        return jsonify(error="File not found"), 404


@app.route("/tree/<path:path>", methods=["GET"])
def list_folder(path):
    """List Folder"""
    try:
        dirs = FileApi().list_dir(path)
        return jsonify(dirs, 200)
    except FileNotFoundError:
        return jsonify(error="File not found"), 404
    except InvalidTypeError:
        return jsonify(error="Invalid type"), 422


if __name__ == "__main__":
    app.run(debug=True)
