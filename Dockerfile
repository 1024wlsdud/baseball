FROM ubuntu:22.04

# 필요한 패키지 한 번에 설치 및 설정
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    xinetd netcat socat \
    && rm -rf /var/lib/apt/lists/*

ENV TERM=linuxs

# 사용자 추가 및 작업 디렉토리 설정
RUN useradd -m prob -s /bin/bash
RUN chown -R prob:prob /home/prob

# 필요한 파일 추가 및 권한 설정
ADD baseball /home/prob/
ADD prob /etc/xinetd.d/
ADD flag /home/prob/


RUN chmod 755 /home/prob/baseball \
    && chown prob:prob /home/prob/baseball


RUN echo "prob 10005/tcp" >> /etc/services
CMD ["/usr/sbin/xinetd","-dontfork"]