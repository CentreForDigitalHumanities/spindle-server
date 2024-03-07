from flask import Flask, abort, jsonify, request
import json
from inference import InferenceWrapper
from aethel.mill.serialization import serial_proof_to_json, serialize_proof
from aethel.utils.tex import sample_to_tex
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("spindle")

def create_app():
    log.info('Loading model')
    inferer = InferenceWrapper(
        weight_path="./data/model_weights.pt",
        atom_map_path="./data/atom_map.tsv",
        config_path="./data/bert_config.json",
        device="cpu",
    )  # replace with 'cpu' if no GPU accelaration

    log.info('Loaded model')
    app = Flask(__name__)

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

        if len(results) < 1:
            log.error("Got no results")
            abort(500)

        analysis = results[0]
        # spindle will store an exception value in the proof variable, at least in some failure modes
        if isinstance(analysis.proof, Exception):
            log.error("Error in analysis", exc_info=analysis.proof)
            abort(500)

        try:
            tex_from_sample = sample_to_tex(analysis)
        except:
            log.exception("Failed to convert result to TeX.")
            abort(500)
            return  # not necessary given abort, but helps type-checker understand that we leave the function here

        log.info("TeX conversion successful.")
        log.info("TeX: %s", tex_from_sample)

        # prepare json-ready version of proof and lexical phrases
        proof = serial_proof_to_json(serialize_proof(analysis.proof))
        lexical_phrases = [phrase.json() for phrase in analysis.lexical_phrases]

        response = dict(
            tex=tex_from_sample,
            proof=proof,
            lexical_phrases=lexical_phrases)
        return jsonify(response)

    log.info('App is ready')
    return app


if __name__ == "__main__":
    log.info("Starting Spindle Server!")
    app = create_app()
    app.run()
