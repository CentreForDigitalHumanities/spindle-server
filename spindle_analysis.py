from inference import InferenceWrapper

def run_spindle_analysis(input_string: str):
    print('Starting analysis with input:', input_string)

    inferer = InferenceWrapper(weight_path='./data/model_weights.pt',
                              atom_map_path='./data/atom_map.tsv',
                              config_path='./data/bert_config.json', 
                              device='cpu')  # replace with 'cpu' if no GPU accelaration
    return inferer.analyze([input_string])
