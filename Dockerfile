# syntax=docker/dockerfile:1
FROM python:3.10.12-bookworm

# Shows print logs from our server in the container logs.
ENV PYTHONUNBUFFERED=1

# Install GIT
RUN apt update
RUN apt install -y git

# Clone the repository and enter the directory
RUN git clone https://github.com/konstantinosKokos/spindle.git
WORKDIR /spindle

# Install aethel
RUN pip install git+https://github.com/konstantinosKokos/aethel@41eab8fb178a197cdf8de738b68e386f07e6e4f5

# Install PyTorch and its dependencies
RUN pip3 install torch==1.12.0 opt_einsum --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install torch-geometric==2.3.1
RUN pip3 install --no-index \
  torch-cluster \
  torch-scatter \
  torch-sparse \
  torch-spline-conv -f https://data.pyg.org/whl/torch-1.12.0+cpu.html

RUN pip3 install transformers==4.20.1 six Flask

# Download BERTje model ahead of time
RUN python -c 'from transformers import pipeline; pipeline("fill-mask", model="GroNLP/bert-base-dutch-cased")'

# Install Gunicorn
RUN pip install gunicorn

# Copy data files
COPY atom_map.tsv data/atom_map.tsv
COPY bert_config.json data/bert_config.json
COPY model_weights.pt data/model_weights.pt

COPY app.py app.py

# Allow the user to specify the port for the Flask server.
ARG SPINDLE_PORT=32768

# Expose the port on which the Flask server will run
EXPOSE $SPINDLE_PORT

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=$SPINDLE_PORT

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
