FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

ENV PLATFORMIO_CORE_DIR=/opt/platformio
ENV PIO_HOME_DIR=/opt/platformio
ENV PATH="/opt/platformio/penv/bin:${PATH}"

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
    git \
    curl \
    ca-certificates \
    build-essential \
    cmake \
    ninja-build \
    pkg-config \
    make \
    udev \
    usbutils \
    && rm -rf /var/lib/apt/lists/*

# --- PlatformIO ---
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir -U platformio


RUN python3 -m pip install --no-cache-dir \
    catkin-pkg \
    lark-parser \
    colcon-common-extensions \
    importlib-resources \
    pyyaml \
    pytz \
    markupsafe==2.0.1 \
    empy==3.3.4

RUN curl -fsSL \
    https://raw.githubusercontent.com/platformio/platformio-core/develop/platformio/assets/system/99-platformio-udev.rules \
    -o /etc/udev/rules.d/99-platformio-udev.rules

RUN pio platform install "atmelsam@^8.3.0" || pio platform install atmelsam


WORKDIR /workspace
COPY platformio.ini /tmp/platformio.ini

RUN mkdir -p /tmp/pio-preload && \
    cp /tmp/platformio.ini /tmp/pio-preload/platformio.ini && \
    cd /tmp/pio-preload && \
    pio pkg install || true

WORKDIR /workspace
CMD ["/bin/bash"]
