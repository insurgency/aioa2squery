FROM python:${PYTHON_VERSION:-3.8}

LABEL maintainer="insurgency.gg"

ADD ./ /aioa2squery/
RUN pip3 install /aioa2squery/[speedups]
RUN rm -rf /aioa2squery/

ENTRYPOINT ["a2squery"]