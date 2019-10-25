ARG PYTHON_VERSION=3.8
FROM python:${PYTHON_VERSION}-slim

LABEL maintainer="insurgency.gg"

ADD ./ /aioa2squery/
RUN pip3 install /aioa2squery/
RUN rm -rf /aioa2squery/

ENTRYPOINT ["a2squery"]