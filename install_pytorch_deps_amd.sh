#!/bin/bash

# Install PyTorch dependencies

pip3 install --no-index \
    torch-cluster \
    torch-scatter \
    torch-sparse \
    torch-spline-conv -f https://data.pyg.org/whl/torch-1.12.0+cpu.html