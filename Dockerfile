FROM python:3

ADD server.py /

RUN pip3 install bottle
RUN pip install opencv-contrib-python --upgrade
RUN pip install bottle-mongo

CMD [ "python", "./server.py" ]
