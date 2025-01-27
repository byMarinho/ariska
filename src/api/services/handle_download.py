import os

from fastapi import HTTPException
from fastapi.responses import FileResponse
from pytubefix import YouTube

from ..core import config

download_path = config.DOWNLOAD_PATH


def make_download_mp3(url: str, resolution: str, filename: str = None):
    """_summary_
        Baixa mp3 da url do youtube, na resolução especificada com o filename informado.
    Args:
        url (str): url do vídeo do youtube
        resolution (str): resolução do áudio
        filename (str, optional): nome do arquivo. Defaults to None.

    Returns:
        json:
            title (str): título do arquivo mp3
            file (file): arquivo de música mp3
    """
    try:
        yt = YouTube(url, "WEB")
        audioStream = yt.streams.filter(only_audio=True, abr=resolution).first()

        filename = yt.title if filename is None else filename

        if not audioStream:
            raise HTTPException(
                status_code=404, detail="Resolução de áudio não encontrada"
            )

        audioFile = audioStream.download(output_path=download_path)
        audioPath = f"{os.path.splitext(audioFile)[0]}.mp3"
        os.rename(audioFile, audioPath)

        return {
            "title": yt.title,
            "file": FileResponse(
                audioPath,
                filename=f"{filename}.mp3",
            ),
        }
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Erro ao baixar .mp3: {err}")


def make_download_mp4(url: str, resolution: str, filename: str = None):
    """_summary_
        Baixa mp4 da url do youtube, na resolução especificada com o filename informado.
    Args:
        url (str): url do vídeo do youtube
        resolution (str): resolução do áudio
        filename (str, optional): nome do arquivo. Defaults to None.

    Returns:
        json:
            title (str): título do arquivo mp4
            file (file): arquivo de vídeo mp4
    """
    try:
        yt = YouTube(url, "WEB")
        videoStream = yt.streams.filter(
            progressive=True, file_extension="mp4", resolution=resolution
        ).first()

        filename = yt.title if filename is None else filename

        if not videoStream:
            raise HTTPException(
                status_code=404, detail="Resolução de vídeo não encontrada"
            )

        videoPath = videoStream.download(output_path=download_path)

        return {
            "title": yt.title,
            "file": FileResponse(videoPath, filename=f"{filename}.mp4"),
        }
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Erro ao baixar vídeo: {err}")
