FROM ubuntu
MAINTAINER add Lucas Carvalho <lucas.carvalho@ic.unicamp.br>

WORKDIR /app

ADD . /app

RUN apt-get update

RUN apt-get install -y wget zip build-essential gfortran

RUN wget https://water.usgs.gov/ogw/modflow/MODFLOW-2005_v1.12.00/MF2005.1_12u.zip
RUN unzip MF2005.1_12u.zip && mv MF2005.1_12u mf2005
RUN cd mf2005/make && make && mv mf2005 /usr/bin/
