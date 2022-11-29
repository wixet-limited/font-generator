FROM ubuntu:22.04

RUN apt update
RUN apt-get install -y potrace imagemagick libjpeg-dev libtiff5-dev libpng-dev libfreetype6-dev libgif-dev libgtk-3-dev libxml2-dev libpango1.0-dev libcairo2-dev libspiro-dev python3-dev ninja-build cmake build-essential gettext
RUN curl https://bootstrap.pypa.io/get-pip.py | python3

RUN curl -L https://github.com/fontforge/fontforge/archive/refs/tags/20220308.tar.gz -o fontforge.tar.gz && \
    tar xf fontforge.tar.gz && \
    rm fontforge.tar.gz && \
    cd fontforge-20220308 && \
    mkdir build && \
    cd build && \
    cmake -GNinja .. && \ 
    ninja && \
    ninja install

COPY main.py main.py

RUN mkdir /svg

CMD ["fontforge", "--script", "/main.py"]
