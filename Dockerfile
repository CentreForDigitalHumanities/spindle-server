# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && apt-get install -y \
  python3 \
  python3-pip

# Install GIT
RUN apt update
RUN apt install -y git

# Clone the repository and enter the directory
RUN git clone https://github.com/konstantinosKokos/spindle.git
WORKDIR /spindle

# Copy the requirements file
COPY requirements.txt requirements.txt

# Upgrade PIP to latest version (needed for aethel)
RUN pip3 install --upgrade pip

# Install the requirements
RUN pip3 install -r requirements.txt

# Install aethel
RUN pip3 install git+https://github.com/konstantinosKokos/aethel@795f34046b7970a28e0e2491ba23dea5e716f1d2

# Install PyTorch and its dependencies
RUN pip3 install torch==1.12.0 \
  torch-cluster==1.6.1 \
  torch-geometric==2.3.1 \
  torch-scatter==2.1.1 \
  torch-sparse==0.6.17 \
  torch-spline-conv==1.2.2

# Copy data files
COPY atom_map.tsv data/atom_map.tsv
COPY bert_config.json data/bert_config.json
COPY model_weights.pt data/model_weights.pt

COPY app.py app.py
COPY spindle_analysis.py spindle_analysis.py

# Expose the port on which the Flask server will run
EXPOSE 5000

# Set the environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
