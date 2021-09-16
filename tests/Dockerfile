FROM ubuntu:20.04

RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
        software-properties-common python3-pip && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    python3 -m pip install pytest tox

RUN apt install -y python3.6 python3.7 python3.9

WORKDIR /tests

CMD ["tox"]
