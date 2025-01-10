from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from ..services.handle_stream import get_resolutions

router = APIRouter()


@router.get(
    "/resolutions",
    tags=["Resolutions"],
    summary="Obter as resoluções do áudio e vídeo disponíveis",
    dependencies=[Depends(RateLimiter(times=6, seconds=60))],
)
async def resolutions(url: str):
    """
    # Summary:
        Retorna as resoluções disponíveis para áudio e vídeo da URL informada.
        Taxa Limite de Consumo: 6 solicitações por minuto.

    # Params:
        url (str): URL do vídeo do youtube

    # Returns:
        json: Objeto com lista de resoluções do áudio e vídeo separados

        ex. {
                "video_resolutions": [
                    "360p"
                ],
                "audio_resolutions": [
                    "48kbps",
                    "128kbps",
                    "50kbps",
                    "70kbps",
                    "160kbps"
                ]
            }
    """
    data = get_resolutions(url=url)

    return data
