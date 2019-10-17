FROM python:${PYTHON_VERSION:-3.8}-slim

LABEL maintainer="insurgency.gg"

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -yq git gcc make libtool
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
RUN pip3 uninstall -y -r ./requirements.dev.txt
WORKDIR /
ADD ./ /aioa2squery/
RUN pip3 install /aioa2squery/
RUN rm -rf /uvloop/ /aioa2squery/
RUN DEBIAN_FRONTEND=noninteractive apt-get autoremove -yq git gcc make libtool

ENTRYPOINT ["a2squery"]