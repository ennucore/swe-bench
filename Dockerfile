# Use an Ubuntu base image
FROM ubuntu:20.04

# Avoid interactive dialog from apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Install basic utilities
RUN apt-get update && apt-get install -y curl wget git build-essential

# Install Miniconda or Miniforge depending on the architecture
ENV CONDA_DIR /opt/conda
RUN ARCH=$(uname -m) && \
    if [ "$ARCH" = "x86_64" ]; then \
        wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh; \
    else \
        wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh -O miniconda.sh; \
    fi && \
    bash miniconda.sh -b -p $CONDA_DIR && \
    rm miniconda.sh
ENV PATH $CONDA_DIR/bin:$PATH

# Initialize Conda for all shell types
RUN conda init

# Install Yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list \
    && apt-get update && apt-get install -y yarn

# Install Trunk
RUN curl https://get.trunk.io -fsSL | bash

# Set the default command to open a bash shell
CMD ["/bin/bash"]
