# syntax=docker/dockerfile:1
FROM python:3.10.12-bookworm

# Install GIT
RUN apt update
RUN apt install -y git

# Clone the repository and enter the directory
RUN git clone https://github.com/konstantinosKokos/spindle.git
WORKDIR /spindle

# Install aethel
RUN pip install git+https://github.com/konstantinosKokos/aethel@795f34046b7970a28e0e2491ba23dea5e716f1d2

# Install PyTorch and its dependencies
RUN pip3 install torch==1.12.0 opt_einsum --extra-index-url https://download.pytorch.org/whl/cpu
RUN pip3 install torch-geometric==2.3.1
RUN pip3 install --no-index \
  torch-cluster \
  torch-scatter \
  torch-sparse \
  torch-spline-conv -f https://data.pyg.org/whl/torch-1.12.0+cpu.html

RUN pip3 install transformers==4.20.1 six Flask

# Copy data files
COPY atom_map.tsv data/atom_map.tsv
COPY bert_config.json data/bert_config.json
COPY model_weights.pt data/model_weights.pt

COPY app.py app.py

# Expose the port on which the Flask server will run
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
