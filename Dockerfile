FROM --platform=linux/arm64 python:3.12.4 AS build

ADD main.py .
ADD bromas.py .
ADD reproductor.py .
ADD apikeys.py .

RUN pip install yt-dlp
RUN pip install pynacl
RUN pip install -U discord.py
RUN apt update && apt install ffmpeg -y 

CMD ["python", "./main.py"]

