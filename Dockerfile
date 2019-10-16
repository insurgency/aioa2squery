FROM python:${PYTHON_VERSION:-3.8}

LABEL maintainer="insurgency.gg"

# Manually install uvloop for 3.8 compatibility
# See: https://github.com/MagicStack/uvloop/pull/275#issuecomment-542887504
RUN git clone \
	--recursive \
	--branch patch-1 \
	https://github.com/dmontagu/uvloop.git
WORKDIR /uvloop/
RUN pip3 install -r ./requirements.dev.txt
RUN make -j2
RUN pip3 install ./
RUN rm -rf /uvloop/
ADD ./ /aioa2squery/
RUN pip3 install /aioa2squery/[speedups]
RUN rm -rf /aioa2squery/

ENTRYPOINT ["a2squery"]