import base64
import json
import logging

from flask import Flask, jsonify, request
import object_detection

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def index():
    return "Hello World!"


# ## Usage format

# python iWebLens_client.py  <input folder name> <URL> <num_threads>
# python object_detection.py yolo_tiny_configs/ inputfolder/000000007454.jpg

# ## Sample run command

# python iWebLens_client.py  inputfolder/  http://localhost:5000/api/v1/object_detection 4
# python iWebLens_client.py inputfolder/ http://localhost:5000/api/v1/detection 1

@app.route("/api/v1/detection", methods=["POST"])
def detection():
    # Convert JSON string to dictionary
    data_dict = json.loads(request.get_json())

    # img_data is decoded from base64 to byte object
    img_data = base64.b64decode(data_dict["image"])

    # call the objection_detection to perform prediction with the POST input image
    result = object_detection.main(img_data)

    # get image uuid
    image_id = data_dict["id"]

    # combine id and prediction result for output
    output = {"id": image_id, "objects": result}

    # make the response and return to client iWebLens
    response = app.response_class(
        # convert output dictionary to json
        response=json.dumps(output, indent=4),
        status=200,
        mimetype='application/json'
    )
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
