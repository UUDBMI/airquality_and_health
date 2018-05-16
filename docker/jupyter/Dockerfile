FROM jupyter/datascience-notebook:latest
MAINTAINER chapmanbe <brian.chapman@utah.edu>
USER root
# for physionet instructions see
# https://www.physionet.org/physiotools/wfdb-linux-quick-start.shtml
# dependencies for spell nbextensions (including spell check) and other requirements

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
      tree \
      graphviz\ 
      less \
      openssh-client \
      gcc \
      libcurl4-openssl-dev \
      libexpat1-dev \
      libnetcdff-dev \
      locales-all \
      libxrender-dev \
      libfontconfig-dev \
      libffi-dev \
      rsync \
      mongodb-clients \
      libmariadb-client-lgpl-dev \
      binutils \
      libproj-dev \
      gdal-bin \
  && rm -rf /var/lib/apt/lists/*



# Set default editor to vim
RUN update-alternatives --set editor /usr/bin/vim.basic

USER jovyan

WORKDIR /home/jovyan
ADD .condarc /home/jovyan/.condarc


RUN conda update conda -y && conda install -y -c conda-forge \
    pip \
    gdal \
    geopandas \
    folium

RUN pip install census us
WORKDIR /home/jovyan

# RUN nbstripout --install
CMD ["start-notebook.sh"]
