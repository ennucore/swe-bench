FROM continuumio/miniconda3

# Avoid interactive dialog from apt-get
ARG DEBIAN_FRONTEND=noninteractive

# Install basic utilities
RUN apt-get update && apt-get install -y curl wget git build-essential gcc make \
    pkg-config autoconf automake \
    python3-docutils \
    libseccomp-dev \
    libjansson-dev \
    libyaml-dev \
    libxml2-dev tree

RUN curl https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
RUN bash -c 'source ~/.bashrc && nvm install 18 && nvm use 18'

RUN git clone https://github.com/universal-ctags/ctags.git && cd ctags && ./autogen.sh && ./configure && make && make install

# Install Yarn
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" > /etc/apt/sources.list.d/yarn.list \
    && apt-get update && apt-get install -y yarn

# Install Trunk
RUN curl https://get.trunk.io -fsSL | bash

RUN conda init --all

# Set the default command to open a bash shell
CMD ["/bin/bash"]
