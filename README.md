[![DOI](https://zenodo.org/badge/671386963.svg)](https://zenodo.org/doi/10.5281/zenodo.10571294)
[![License](https://img.shields.io/badge/License-BSD_3--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


# Spindle Server

Spindle Server contains a Dockerfile that can be used to create a containerised Flask server with the [Spindle](https://github.com/konstantinosKokos/spindle) parser, which produces type-logical analyses of Dutch sentences. This project is built as a dependency to [ParsePort](https://github.com/UUDigitalHumanitieslab/parseport).

## Contents

The main entry point is a Dockerfile that will create a container, install the necessary dependencies and move the `atom_map.tsv` and `bert_config.json` files over to the container. In addition, this repository expects to find a file with PyTorch model weights (`model_weights.pt`).

## Prerequisites

A host machine with Docker installed and internet access.

## Usage

1. Put a copy of `model_weights.pt` in the root directory of this repository.

2. Build an image with `docker build -t spindle-server:latest .`

3. Run container and expose a port with `docker run -d -p 32768:32768 --name spindle-server spindle-server`

4. After successful startup, the server will setup the parser. This may take a few minutes.

5. Connect to the parser by sending a request to `localhost:32768`. The request should be a JSON object of the shape `{ 'input': '<my-sentence>'}`, where `<my-sentence>` should be replaced with a Dutch sentence.

6. If the parse fails, a response with status code 500 is returned. If the parser returns a so-called proof, it is included in the response.

7. Upon successful parsing, the server will return a JSON object containing the following properties.
    - `tex`: the full analysis of the sentence in `.tex` format;
    - `proof`: the proof of the analysis (in JSON format);
    - `lexical_phrases`: analyses of the individual phrases (in JSON format).

## Licence

Spindle Server is shared under a BSD 3-Clause licence. See [LICENSE](./LICENSE) for more information.

## Citation

If you wish to cite this repository, please use the metadata provided in our [CITATION.cff file](./CITATION.cff).

## Contact

For questions, small feature suggestions, and bug reports, feel free to [create an issue](https://github.com/UUDigitalHumanitieslab/spindle-server/issues/new). If you do not have a Github account, you can also [contact the Centre for Digital Humanities](https://cdh.uu.nl/contact/).