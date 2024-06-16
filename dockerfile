# FROM ubuntu:jammy as build
FROM ubuntu:jammy as build

RUN apt-get update -qq && apt-get -y install \
    autoconf \
    automake \
    build-essential \
    cmake \
    git-core \
    libass-dev \
    libfreetype6-dev \
    libgnutls28-dev \
    libmp3lame-dev \
    libsdl2-dev \
    libtool \
    libva-dev \
    libvdpau-dev \
    libvorbis-dev \
    libxcb1-dev \
    libxcb-shm0-dev \
    libxcb-xfixes0-dev \
    meson \
    ninja-build \
    pkg-config \
    texinfo \
    wget \
    yasm \
    zlib1g-dev

RUN mkdir -p /opt/ffmpeg/ffmpeg_sources /opt/ffmpeg/bin

WORKDIR /opt/ffmpeg

# Baixando / compilando libs necessárias
## NASM (usado para algumas libs)
RUN apt-get install nasm -y
## VP8
RUN apt-get install libvpx-dev -y
## VP9
RUN apt-get install libopus-dev -y
## AV1
WORKDIR /opt/ffmpeg/ffmpeg_sources
RUN git -C aom pull 2> /dev/null || git clone --depth 1 https://aomedia.googlesource.com/aom
RUN mkdir -p aom_build
WORKDIR /opt/ffmpeg/ffmpeg_sources/aom_build
RUN PATH="/opt/ffmpeg/bin:$PATH" cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="/opt/ffmpeg/ffmpeg_build" -DENABLE_TESTS=OFF -DENABLE_NASM=on ../aom
RUN PATH="/opt/ffmpeg/bin:$PATH" make && make install

# Compilando
WORKDIR /opt/ffmpeg/ffmpeg_sources
RUN wget -O ffmpeg-snapshot.tar.bz2 https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
RUN tar xjvf ffmpeg-snapshot.tar.bz2
WORKDIR /opt/ffmpeg/ffmpeg_sources/ffmpeg
RUN PATH="/opt/ffmpeg/bin:$PATH" PKG_CONFIG_PATH="/opt/ffmpeg/ffmpeg_build/lib/pkgconfig" \
./configure \
  --prefix="/opt/ffmpeg/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I/opt/ffmpeg/ffmpeg_build/include" \
  --extra-ldflags="-L/opt/ffmpeg/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --ld="g++" \
  --bindir="/opt/ffmpeg/bin" \
  --enable-libopus \
  --enable-libvpx \
  --enable-libaom

RUN PATH="/opt/ffmpeg/bin:$PATH" make && make install && hash -r

# python resources
RUN apt install python3 python3-pip -y
RUN apt install python3-venv -y

WORKDIR /home
RUN python3 -m venv env
COPY ./requirements.txt .
SHELL ["/bin/bash", "-c"]
RUN source ./env/bin/activate
RUN pip3 install -r requirements.txt
ENV PATH=/opt/ffmpeg/bin:$PATH
COPY ./src ./src

CMD python3 -m output_videos/h264_vp9_changing_bitrate/h264_vp9_bitrate_2M.mp4 output_videos/h264_vp9_changing_bitrate/h264_vp9_bitrate_1M.mp4