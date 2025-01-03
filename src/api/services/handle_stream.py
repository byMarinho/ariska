from fastapi import HTTPException
from pytubefix import YouTube


def get_informations(url: str):
    """_summary_
        Retorna as informações do vídeo
    Args:
        url (str): link do vídeo do youtube
    """
    try:
        yt = YouTube(url)

        return {
            "title": yt.title,
            "author": yt.author,
            "length": yt.length,
            "views": yt.views,
            "description": yt.description,
            "image": yt.thumbnail_url,
        }
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"Erro ao obter informações do vídeo: {err}"
        )


def get_resolutions(url: str):
    """_summary_
        Retorna as resoluções de áudio e vídeo da url
    Args:
        url (str): link do vídeo do youtube
    """
    try:
        yt = YouTube(url)
        sVideo = [
            stream.resolution
            for stream in yt.streams.filter(progressive=True, file_extension="mp4")
        ]
        sAudio = [stream.abr for stream in yt.streams.filter(only_audio=True)]

        return {"video_resolutions": sVideo, "audio_resolutions": sAudio}
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Erro ao obter resoluções: {err}")
