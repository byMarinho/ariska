import os

from fastapi import HTTPException
from fastapi.responses import FileResponse
from pytubefix import Playlist

from ..core import config
from ..services.utility import FileMedia

download_path = config.DOWNLOAD_PATH


def playzip(filename: str, files: list):
    compact = FileMedia()
    playzip = compact.zipPlaylistFiles(filename, files)

    return {
        "title": filename,
        "file": FileResponse(playzip, filename=f"{filename}.zip"),
    }


def make_download_playlist_mp3(url: str, list: str, resolution: str):
    """_summary_
        Baixar todas as mp3 da playlist na resolução especificada
    Args:
        url (str): link da playlist do youtube
        resolution (str): resolução do áudio
        zip (bool): arquivo compactado .zip com todas as músicas

    Returns:
        json:
            title (str): título do arquivo mp3
            file:
                (array): lista de arquivos .mp3 | file: arquivo compactado .zip
    """
    try:
        audioPaths = []
        pl = Playlist(f"{url}&list={list}", "WEB")
        print(f"Baixando playlist: {pl.title}")

        for video in pl.videos:
            try:
                print(f"Baixando: {video.title}")
                audioStream = video.streams.filter(
                    only_audio=True, abr=resolution
                ).first()

                if not audioStream:
                    continue

                audioFile = audioStream.download(output_path=download_path)
                audioPath = f"{os.path.splitext(audioFile)[0]}.mp3"
                os.rename(audioFile, audioPath)
                audioPaths.append(audioPath)
            except Exception as err:
                print(f"Erro ao baixar o áudio {video.title}: {err}")

        return {"title": pl.title, "files": audioPaths}
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"Erro ao baixar áudios da playlist: {err}"
        )


def make_download_playlist_mp4(url: str, list: str, resolution: str):
    """_summary_
        Baixar todos os mp4 da playlist na resolução especificada
    Args:
        url (str): link da playlist do youtube
        resolution (str): resolução do vídeo
        zip (bool): arquivo compactado .zip com todos os vídeos

    Returns:
        json:
            title (str): título do arquivo mp4
            file:
                (array): lista de arquivos .mp4 | file: arquivo compactado .zip
    """
    try:
        videoPaths = []
        pl = Playlist(f"{url}&list={list}", "WEB")
        print(f"Baixando playlist: {pl.title}")

        for video in pl.videos:
            try:
                print(f"Baixando: {video.title}")
                videoStream = video.streams.filter(
                    progressive=True, file_extension="mp4", resolution=resolution
                ).first()

                if not videoStream:
                    continue

                videoPath = videoStream.download(output_path=download_path)
                videoPaths.append(videoPath)
            except Exception as err:
                print(f"Erro ao baixar o vídeo {video.title}: {err}")

        return {"title": pl.title, "files": videoPaths}
    except Exception as err:
        raise HTTPException(
            status_code=400, detail=f"Erro ao baixar vídeos da playlist: {err}"
        )
