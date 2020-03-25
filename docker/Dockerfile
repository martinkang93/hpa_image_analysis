ARG cuda_version=9.0
ARG cudnn_version=7
FROM nvidia/cuda:${cuda_version}-cudnn${cudnn_version}-devel
# ARG instruction defines argument which could be overriden at build time with:
# `docker build --build-arg cuda_version=8.0`

# ---- INSTALLS ----
# system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
      vim \
      bzip2 \
      g++ \
      git \
      graphviz \
      libgl1-mesa-glx \
      libhdf5-dev \
      openmpi-bin \
      wget && \
    rm -rf /var/lib/apt/lists/*

# conda
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH

RUN wget --quiet --no-check-certificate https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo "c59b3dd3cad550ac7596e0d599b91e75d88826db132e4146030ef471bb434e9a *Miniconda3-4.2.12-Linux-x86_64.sh" | sha256sum -c - && \
    /bin/bash /Miniconda3-4.2.12-Linux-x86_64.sh -f -b -p $CONDA_DIR && \
    rm Miniconda3-4.2.12-Linux-x86_64.sh && \
    echo export PATH=$CONDA_DIR/bin:'$PATH' > /etc/profile.d/conda.sh

# python packages
ENV NB_USER nfer
ENV NB_UID 1000

RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    chown $NB_USER $CONDA_DIR -R && \
    mkdir -p /src && \
    chown $NB_USER /src

USER $NB_USER

ARG python_version=3.6

RUN conda config --append channels conda-forge
RUN conda install -y python=${python_version} && \
    pip install --upgrade pip && \
    pip install \
      keras==2.2.4 \
      keras-vis \
      sklearn_pandas \
      tensorflow-gpu==1.12 \
      opencv-python \
      boto3 \
      cntk-gpu && \
    conda install \
      bcolz \
      h5py \
      matplotlib \
      mkl \
      nose \
      notebook \
      Pillow \
      pandas \
      pydot \
      pygpu \
      pyyaml \
      scikit-learn \
      six \
      theano \
      mkdocs \
      && \
    conda clean -yt
#    git clone git://github.com/keras-team/keras.git /src && pip install -e /src[tests] && \
#    pip install git+git://github.com/keras-team/keras.git && \


# ---- Config ----
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENV PYTHONPATH='/src/:$PYTHONPATH'

# set the working directory for subsequent RUN, CMD, ENTRYPOINT, COPY, ADD instructions
# this can be overriden by `docker run --workdir="/" IMAGE`
WORKDIR /src/workspace

# run image with `docker run -p 8484:8888 ...` to bind host port 8484 to container port 8888
EXPOSE 8888


# ---- Command ----
# by default, launch a notebook when image is run: `docker run IMAGE [CMD]`
CMD jupyter notebook --port=8888 --ip=0.0.0.0
