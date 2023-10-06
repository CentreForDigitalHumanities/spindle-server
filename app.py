from enum import Enum
from flask import Flask, abort, jsonify, request
import json
from inference import InferenceWrapper
from aethel.utils.tex import sample_to_tex
import logging


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("spindle")

inferer = InferenceWrapper(
    weight_path="./data/model_weights.pt",
    atom_map_path="./data/atom_map.tsv",
    config_path="./data/bert_config.json",
    device="cpu",
)  # replace with 'cpu' if no GPU accelaration

app = Flask(__name__)


class SpindleAnalysisError(Enum):
    VALUE_ERROR = "value_error"
    TEX_CONVERSION_FAILED = "tex_conversion_failed"


class ResultAnalyser:
    tex: str | None = None
    errors: list[SpindleAnalysisError] = []
    proof: str | None = None
    phrases = []

    def __init__(self, parse_result):
        self.tex = None
        self.errors = []
        self.proof = None
        self.phrases = []
        # For now we only take the first sentence.
        self.analyse_result(parse_result[0])

    def __dict__(self):
        return {
            "tex": self.tex,
            "errors": self.errors,
            "proof": self.proof,
            "phrases": self.phrases,
        }

    def analyse_result(self, parse_result) -> None:
        analysis = vars(parse_result)

        proof = analysis["proof"]
        self.proof = self.unpack_proof(proof=proof)

        if type(proof) == ValueError:
            self.errors.append(SpindleAnalysisError.VALUE_ERROR)
            self.proof = None

        try:
            tex_from_sample = sample_to_tex(parse_result)
            self.tex = tex_from_sample
        except:
            self.errors.append(SpindleAnalysisError.TEX_CONVERSION_FAILED)
            self.tex = None

        lexical_phrases = analysis["lexical_phrases"]
        self.phrases = self.unpack_phrases(phrases=lexical_phrases)

    def unpack_proof(self, proof) -> dict[str, str | list[str]]:
        proof_props = vars(proof)
        premises = proof_props.get("premises", [])
        premises_list = list(map(str, premises)) if premises != [] else []
        conclusion = proof_props.get("conclusion", None)
        rule = proof_props.get("rule", None)
        rule_name = vars(rule).get("_name_", None) if rule is not None else None
        focus = proof_props.get("focus", None)

        return {
            'premises': premises_list,
            'conclusion': str(conclusion) if conclusion else None,
            'rule': rule_name,
            'focus': str(focus) if focus else None
        }


    def unpack_phrases(self, phrases: list) -> list:
        unpacked_phrases = []
        for phrase in phrases:
            phrase_props = vars(phrase)
            phrase_type = phrase_props.get("type", None)
            phrase_type_sign = (
                vars(phrase_type).get("sign", None) if phrase_type is not None else None
            )
            lexical_items = phrase_props.get("items", [])

            return_items = []
            for item in lexical_items:
                item_props = vars(item)  # type: dict[str, str]
                return_items.append(
                    {
                        "word": item_props.get("word", None),
                        "pos": item_props.get("pos", None),
                        "pt": item_props.get("pt", None),
                        "lemma": item_props.get("lemma", None),
                    }
                )

            unpacked_phrases.append(
                {"phrase_type": phrase_type_sign, "items": return_items}
            )

        return unpacked_phrases


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

    analyser = ResultAnalyser(parse_result=results)

    response_data = {
        "tex": analyser.tex,
        "errors": analyser.errors,
        "proof": analyser.proof,
        "phrases": analyser.phrases,
    }

    return jsonify(response_data)


if __name__ == "__main__":
    log.info("Starting Spindle Server!")
    app.run()
