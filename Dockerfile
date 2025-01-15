# syntax=docker/dockerfile:1
FROM python:3.10.12-bookworm


# Show print logs; don't write .pyc files.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

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

# Copy and set up the shell scripts 
COPY install_pytorch_deps_amd.sh /usr/local/bin/install_pytorch_deps_amd.sh
COPY install_pytorch_deps_arm.sh /usr/local/bin/install_pytorch_deps_arm.sh
RUN chmod +x /usr/local/bin/install_pytorch_deps_amd.sh
RUN chmod +x /usr/local/bin/install_pytorch_deps_arm.sh

# Run the shell script conditionally based on the build architecture
ARG BUILDARCH
RUN if [ "$BUILDARCH" = "arm64" ]; then \
    /usr/local/bin/install_pytorch_deps_arm.sh; \
  else \
    /usr/local/bin/install_pytorch_deps_amd.sh; \
  fi

RUN pip3 install transformers==4.20.1 six Flask

# Download BERTje model ahead of time
RUN python -c 'from transformers import pipeline; pipeline("fill-mask", model="GroNLP/bert-base-dutch-cased")'

# Install Gunicorn
RUN pip install gunicorn

# Create a directory for Gunicorn logs (production).
RUN mkdir -p /logs

# Copy data files
COPY atom_map.tsv data/atom_map.tsv
COPY bert_config.json data/bert_config.json
COPY model_weights.pt data/model_weights.pt

COPY app.py app.py

# Expose the port on which the Flask server will run
EXPOSE 32768

# Set the environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=$SPINDLE_PORT

# Run the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]
