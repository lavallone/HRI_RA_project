FROM python:2.7

RUN pip install --user tornado==5.1.1

ENV MODIM_HOME /opt/modim
ENV PYTHONPATH /opt/modim/src/GUI

RUN echo "20211224c" > /tmp/lastdockerbuild

RUN cd /opt && git clone --depth 1 https://bitbucket.org/mtlazaro/modim.git

WORKDIR /opt/modim/src/GUI

CMD [ "python", "ws_server.py" ]

