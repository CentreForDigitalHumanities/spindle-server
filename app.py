from flask import Flask, jsonify, request
from inference import InferenceWrapper

app = Flask(__name__)

inferer = InferenceWrapper(
    weight_path="./data/model_weights.pt",
    atom_map_path="./data/atom_map.tsv",
    config_path="./data/bert_config.json",
    device="cpu",
)  # replace with 'cpu' if no GPU accelaration


@app.route("/", methods=["GET"])
def handle_get_request():
    return "Hello, world!"


@app.route("/", methods=["POST"])
def handle_request():
    print("Request received!")
    analysis_input = request.data.decode("utf-8")

    print('Starting analysis with input:', analysis_input)
    results = inferer.analyze([analysis_input])

    print("Analysis complete!")
    response = {"results": results}

    return jsonify(response)

if __name__ == "__main__":
    print("Starting Spindle Server!")
    app.run()
