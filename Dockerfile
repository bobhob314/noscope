FROM python:3

ADD server.py /

RUN pip3 install bottle
RUN pip install opencv-contrib-python --upgrade

CMD [ "python", "./server.py" ]
