import os
import re
from pathlib import Path

from pytube import YouTube, exceptions


def movie2mp3(url):
    try:
        yTub = YouTube(url)

        # @Extract audio with 160kbps quality from video
        movie = yTub.streams.filter(abr='160kbps').last()

        # @Download file
        outFile = movie.download(output_path='tmp')
        base, ext = os.path.splitext(outFile)
        newFile = Path(f"{base}.mp3")
        os.rename(outFile, newFile)

        if newFile.exists():
            return {
                "message": "success",
                "title": yTub.title,
                "file": newFile
            }
        else:
            return {
                "code": 510,
                "message": "Ops... Não conseguimos acessar esse vídeo"
            }
    except exceptions.VideoUnavailable:
        return {
            "code": 520,
            "message": "Vídeo indisponível para Download"
        }


def delmp3(file):
    if os.path.exists(file):
        os.remove(file)


def validurl(url):
    regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
    )
    if re.match(regex, url):
        return True
    else:
        return False
