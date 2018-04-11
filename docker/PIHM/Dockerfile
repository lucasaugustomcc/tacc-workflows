FROM ubuntu
MAINTAINER add Lucas Carvalho <lucas.carvalho@ic.unicamp.br>

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y wget zip make gcc
RUN wget https://computation.llnl.gov/projects/sundials/download/sundials-2.2.0.tar.gz && tar xvf sundials-2.2.0.tar.gz && cd sundials && ./configure && make && make install
RUN wget http://www.pihm.psu.edu/PIHM_v2.2.tar && tar xvf PIHM_v2.2.tar && cd PIHM_v2.2 && make clean
RUN cd PIHM_v2.2 && grep -rl Makefile . | xargs sed -i 's/\/Users\/xxy113\/software/\/app/g'
RUN cd PIHM_v2.2 && make pihm && mv pihm /usr/bin