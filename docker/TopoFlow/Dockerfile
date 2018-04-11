FROM ubuntu
MAINTAINER add Lucas Carvalho <lucas.carvalho@ic.unicamp.br>

WORKDIR /app

ADD . /app

RUN apt-get update

RUN apt-get install -y python-pip wget zip
RUN wget https://github.com/peckhams/topoflow/archive/master.zip
RUN unzip master.zip && cd topoflow-master && pip install --editable ./ && pip install -U numpy==1.11.0

#CMD ["/bin/sh" "-c" "python -m topoflow --cfg_prefix="June_20_67" --cfg_directory="/app/topoflow/examples/Treynor_Iowa_30m/" --driver_comp_name=tf_infil_green_ampt"]