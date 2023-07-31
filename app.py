from flask import Flask, jsonify, request
import spindle_analysis

app = Flask(__name__)

@app.route('/', methods=['GET'])
def handle_get_request():
    return 'Hello, world!'

@app.route('/', methods=['POST'])
def handle_request():
    print('Handling request...')
    analysis_input = request.data.decode('utf-8')
    analysis_results = spindle_analysis.run_spindle_analysis(analysis_input)
    print('Analysis complete!')
    
    response = { 'results': analysis_results }

    return jsonify(response)

if __name__ == '__main__':
    print('Starting Spindle Server!')
    app.run()