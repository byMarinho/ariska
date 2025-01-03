from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from ..services.handle_playlist import (
    make_download_playlist_mp3,
    make_download_playlist_mp4,
    playzip,
)

router = APIRouter()


@router.get(
    "/download/playlist/audio",
    tags=["Playlists"],
    summary="Baixar playlist de áudio",
    dependencies=[Depends(RateLimiter(times=1, seconds=120))],
)
async def download_playlist_audio(
    url: str, list: str, resolution: str, zip: bool = True
):
    """Summary: Baixa todos os áudios de uma playlist do Youtube na resolução especificada

    # Params:
        url (str): URL da playlist do Youtube
        resolution (str): Resolução de áudio desejada (e.g., "128kbps")
        zip (bool): Arquivos da playlist compactados

    # Returns:
        array_files: arquivos .mp3 com o título de cada vídeo ou compactado .zip
    """
    data = make_download_playlist_mp3(url=url, list=list, resolution=resolution)

    if zip:
        files = []
        filename = data["title"]
        files = data["files"]
        zipData = playzip(filename=filename, files=files)

        return zipData

    return data


@router.get(
    "/download/playlist/video",
    tags=["Playlists"],
    summary="Baixar playlist de vídeos",
    dependencies=[Depends(RateLimiter(times=1, seconds=120))],
)
async def download_playlist_video(
    url: str, list: str, resolution: str, zip: bool = True
):
    """Summary: Baixa todos os vídeos da playlist do Youtube na resolução especificada

    # Params:
        url (str): URL da playlist do Youtube
        resolution (str): Resolução de vídeo desejada (e.g., "720p")

    # Returns:
        array_files: vários arquivos .mp4 com o título de cada vídeo
    """
    data = make_download_playlist_mp4(url=url, list=list, resolution=resolution)

    if zip:
        files = []
        filename = data["title"]
        files = data["files"]
        zipData = playzip(filename=filename, files=files)

        return zipData

    return data
