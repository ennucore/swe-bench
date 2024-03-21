FROM continuumio/miniconda3

# Avoid interactive dialog from apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Install basic utilities
RUN apt-get update && apt-get install -y curl wget git build-essential

# Install Yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list \
    && apt-get update && apt-get install -y yarn

# Install Trunk
RUN curl https://get.trunk.io -fsSL | bash

# Set the default command to open a bash shell
CMD ["/bin/bash"]
