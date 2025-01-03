from contextlib import asynccontextmanager
from math import ceil

import redis.asyncio as redis
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi_limiter import FastAPILimiter
from scalar_fastapi import get_scalar_api_reference

from .core import config
from .routes import (
    router_downloads,
    router_informations,
    router_playlists,
    router_resolutions,
)

REDIS_URL = config.REDIS_URL


async def service_name_id(request: Request):
    service = request.headers.get("Service-Name")
    return service


async def custom_callback(request: Request, response: Response, pexpire: int):
    """_summary_
        Retorno de chamada padrão quando há muitas solicitaçõs
    Params:
        request (Request):
        response (Response):
        pexpire (int): milissegundos restantes

    Returns:
    """
    expire = ceil(pexpire / 1000)

    raise HTTPException(
        status.HTTP_429_TOO_MANY_REQUESTS,
        f"Muitas solicitações. Tente novamente após {expire} segundos.",
        headers={"Retry-After": str(expire)},
    )


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_conn = redis.from_url(url=REDIS_URL, encoding="utf-8", decode_responses=True)

    await FastAPILimiter.init(
        redis=redis_conn,
        identifier=service_name_id,
        http_callback=custom_callback,
    )
    yield
    await FastAPILimiter.close()


app = FastAPI(
    title="Arisksa API",
    summary="Downloader Audio/Vídeo e Playlist Youtube",
    description="""
        API para obter informações dos vídeos, 
        resoluções de áudio e vídeo,
        fazer download dos apenas de áudio
        ou vídeo nas resoluções especificadas, 
        além de fazer o download de playlists.

        Desenvolvida em FastAPI 🚀 com ❤️ byMario.dev

        * github:  https://github.com/byMarinho/ariska
        * e-mail:  me@bymario.dev
        * license: MIT
    """,
    lifespan=lifespan,
)

app.include_router(router_informations.router)
app.include_router(router_resolutions.router)
app.include_router(router_downloads.router)
app.include_router(router_playlists.router)


@app.get("/", include_in_schema=False)
async def document():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
        scalar_favicon_url="https://cdn3d.iconscout.com/3d/premium/thumb/api-9711442-7946873.png",
    )
