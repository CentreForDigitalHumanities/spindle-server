from flask import Flask, abort, jsonify, request
import json
from inference import InferenceWrapper
from aethel.utils.tex import sample_to_tex

app = Flask(__name__)

inferer = InferenceWrapper(
    weight_path="./data/model_weights.pt",
    atom_map_path="./data/atom_map.tsv",
    config_path="./data/bert_config.json",
    device="cpu",
)  # replace with 'cpu' if no GPU accelaration


@app.route("/", methods=["POST"])
def handle_request():
    print("Request received!")
    request_body = request.data.decode("utf-8")

    try:
        request_body_json = json.loads(request_body)
        spindle_input = request_body_json['input']
    except:
        print('Failed to parse request body.')
        abort(400)

    print("Starting analysis with input:", spindle_input)
    results = inferer.analyze([spindle_input])

    print("Analysis complete!")
    print("Results:", results)

    try:
        tex_from_sample = sample_to_tex(results[0])
        print('tex from sample:', tex_from_sample)
    except:
        print('Failed to convert result to TeX.')
        abort(400)
    
    response = {"results": tex_from_sample}

    return jsonify(response)


if __name__ == "__main__":
    print("Starting Spindle Server!")
    app.run()
