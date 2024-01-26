[![DOI](https://zenodo.org/badge/671386963.svg)](https://zenodo.org/doi/10.5281/zenodo.10571294)

## Spindle Server

This repository contains a Dockerfile that can be used to create an image for a Spindle parser, wrapped in a very simple Flask webserver.

**Setup**

1. Put a copy of `model_weights.pt` in the root directory. (This file is too large to check in on GitHub.)

2. Build an image with `docker build -t spindle-server:latest .`

3. Run container and expose a port with `docker run -d -p 32768:5000 --name spindle-server spindle-server`

4. Connect to the parser by sending a request to `localhost:32768`.
