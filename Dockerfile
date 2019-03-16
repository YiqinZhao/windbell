FROM python:3-slim

RUN mkdir -p /windbell

WORKDIR /windbell/
COPY ./ /windbell/
RUN python setup.py install
RUN rm -rf ./*

CMD ["windbell", "send"]
