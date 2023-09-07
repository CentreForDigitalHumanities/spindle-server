from flask import Flask, abort, jsonify, request
import json
from inference import InferenceWrapper
from aethel.utils.tex import sample_to_tex
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("spindle")

inferer = InferenceWrapper(
    weight_path="./data/model_weights.pt",
    atom_map_path="./data/atom_map.tsv",
    config_path="./data/bert_config.json",
    device="cpu",
)  # replace with 'cpu' if no GPU accelaration


@app.route("/", methods=["POST"])
def handle_request():
    log.info("Request received!")
    request_body = request.data.decode("utf-8")

    try:
        request_body_json = json.loads(request_body)
    except json.JSONDecodeError:
        log.error("Failed to parse request body as JSON.")
        abort(400)

    if "input" not in request_body_json:
        log.error("Request body does not contain 'input' field.")
        abort(400)

    spindle_input = request_body_json["input"]

    if not isinstance(spindle_input, str):
        log.error("Input is not a string.")
        abort(400)

    log.info("Starting analysis with input:", spindle_input)
    results = inferer.analyze([spindle_input])

    log.info("Analysis complete!")
    log.info("Results: %s", results)

    try:
        tex_from_sample = sample_to_tex(results[0])
    except:
        log.error("Failed to convert result to TeX.")
        abort(400)

    log.info("TeX conversion successful.")
    log.info("TeX: %s", tex_from_sample)

    response = {"results": tex_from_sample}
    return jsonify(response)


if __name__ == "__main__":
    log.info("Starting Spindle Server!")
    app.run()
