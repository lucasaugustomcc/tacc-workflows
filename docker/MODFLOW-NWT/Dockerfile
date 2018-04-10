FROM ubuntu
MAINTAINER add Lucas Carvalho <lucas.carvalho@ic.unicamp.br>

WORKDIR /app

ADD . /app

RUN apt-get update

RUN apt-get install -y python-pip wget zip gfortran
RUN pip install numpy requests 
RUN pip install https://github.com/modflowpy/pymake/zipball/master
RUN wget https://github.com/modflowpy/pymake/archive/master.zip
RUN unzip master.zip && cd pymake-master/examples && python make_mfnwt.py && cd temp && mv mfnwt /usr/bin/