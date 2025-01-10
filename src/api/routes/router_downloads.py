from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from ..services.handle_download import make_download_mp3, make_download_mp4

router = APIRouter()


@router.get(
    "/download/audio",
    tags=["Downloads"],
    summary="Baixar apenas o áudio do vídeo",
    dependencies=[Depends(RateLimiter(times=6, seconds=60))],
)
async def download_audio(url: str, resolution: str):
    """
    # Summary:
        Baixar apenas o áudio do vídeo do Youtube na resolução especificada.
        Taxa Limite de Consumo: 6 solicitações por minuto.

    # Params:
        url (str): URL do vídeo no Youtube
        resolution (str): Resolução de áudio desejada (ex., "128kbps")

    # Returns:
        file: arquivo .mp3 com o título do vídeo
    """
    data = make_download_mp3(url=url, resolution=resolution)

    return data


@router.get(
    "/download/video",
    tags=["Downloads"],
    summary="Baixar o vídeo completo",
    dependencies=[Depends(RateLimiter(times=6, seconds=60))],
)
async def download_video(url: str, resolution: str):
    """
    # Summary:
        Baixa o vídeo completo do Youtube na resolução especificada.
        Taxa Limite de Consumo: 6 solicitações por minuto.


    # Params:
        url (str): URL do vídeo no Youtube
        resolution (str): Resolução do vídeo desejada (e.g., "720p")

    # Returns:
        file: arquivo .mp4 com o título do vídeo
    """
    data = make_download_mp4(url=url, resolution=resolution)

    return data
