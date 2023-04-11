import os
import re
from datetime import datetime
import json
import subprocess

import quart
import quart_cors
from quart import request

app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

@app.post("/run")
async def run_cmd():
    request_data = await quart.request.get_json(force=True)
    prompt = request_data.get("cmd")
    return_stdout = request_data.get("stdout", True)  # Default to True
    return_stderr = request_data.get("stderr", False)  # Default to False
    timeout = request_data.get("timeout", 10)  # Default to 10 seconds

    try:
        # Run the command and capture the output with a timeout
        process = subprocess.run(
            prompt,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
            timeout=timeout,
        )

        output = {"exit_code": process.returncode}

        if return_stdout:
            output["stdout"] = process.stdout

        if return_stderr:
            output["stderr"] = process.stderr

        return quart.Response(
            response=json.dumps(output), status=200, mimetype="application/json"
        )

    except subprocess.TimeoutExpired as e:
        output = {"error": "Command execution timed out", "stdout": e.stdout, "stderr": e.stderr}
        return quart.Response(
            response=json.dumps(output), status=408, mimetype="application/json"
        )


@app.post("/list_files")
async def list_files():
    request_data = await quart.request.get_json(force=True)
    base_directory = request_data.get("base_directory", os.getcwd())
    regexp = request_data.get("regexp", None)
    limit = request_data.get("limit", None)

    if not os.path.isdir(base_directory):
        return quart.Response(
            response=json.dumps({"error": "Invalid base directory"}),
            status=400,
            mimetype="application/json",
        )

    if regexp is not None:
        pattern = re.compile(regexp)

    def filter_files(file):
        if regexp is None:
            return True
        return pattern.match(file)

    file_list = []

    for root, _, files in os.walk(base_directory):
        for file in filter(filter_files, files):
            file_path = os.path.join(root, file)
            print(file_path)
            stat = os.stat(file_path)
            try:
                file_data = {
                    "path": file_path,
                    "ctime": datetime.fromtimestamp(stat.st_ctime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "mtime": datetime.fromtimestamp(stat.st_mtime).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "size": stat.st_size,
                }
                file_list.append(file_data)
            except:
                pass

            if limit is not None and len(file_list) >= limit:
                break

        if limit is not None and len(file_list) >= limit:
            break

    return quart.Response(
        response=json.dumps(file_list), status=200, mimetype="application/json"
    )


@app.post("/read_file")
async def read_file():
    request_data = await quart.request.get_json(force=True)
    file_path = request_data.get("path")

    if not os.path.isfile(file_path):
        return quart.Response(
            response=json.dumps({"error": "Invalid file path"}),
            status=400,
            mimetype="application/json",
        )

    try:
        with open(file_path, "r") as file:
            content = file.read()

        stat = os.stat(file_path)

        file_data = {
            "path": file_path,
            "ctime": datetime.fromtimestamp(stat.st_ctime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "mtime": datetime.fromtimestamp(stat.st_mtime).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "content": content,
        }

        return quart.Response(
            response=json.dumps(file_data), status=200, mimetype="application/json"
        )

    except Exception as e:
        return quart.Response(
            response=json.dumps({"error": str(e)}),
            status=500,
            mimetype="application/json",
        )


@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
