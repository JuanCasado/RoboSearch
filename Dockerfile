
FROM python:3.9-rc-buster

ARG root=/planning

ADD ./bin  ${root}/bin
ADD ./src  ${root}/src
ENV PATH ${root}/bin:${PATH}
WORKDIR ${root}/src

RUN pip install -r PathPlanPrinter/requirements.txt
RUN pip install -r server/requirements.txt

CMD [ "python", "server/server.py" ]
