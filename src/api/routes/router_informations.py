from fastapi import APIRouter, Depends
from fastapi_limiter.depends import RateLimiter

from ..services.handle_stream import get_informations

router = APIRouter()


@router.get(
    "/informations",
    tags=["Informations"],
    summary="Obter as informações do vídeo",
    dependencies=[Depends(RateLimiter(times=15, seconds=60))],
)
async def informations(url: str):
    """
    # Summary:
        Retorna informações do vídeo da URL.
        Taxa Limite de Consumo: 15 solicitações por minuto

    # Params:
        url (str): URL do vídeo do Youtube

    # Returns:
        json: Informações do vídeo

        ex. {
                "title": "Victor & Leo - Sem Limites Pra Sonhar part. Lucyana [Clipe Oficial]",
                "author": "Victor e Leo",
                "length": 231,
                "views": 112445527,
                "description": "Sem Limites Pra Sonhar...",
                "image": "https://i.ytimg.com/vi/7eST1nQ6fiI/sddefault.jpg"
            }
    """
    data = get_informations(url=url)

    return data
