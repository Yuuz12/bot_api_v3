from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.exceptions import AuthError, NotFoundError, BadRequestError, ForbiddenError, ConflictError
from app.utils.http import close_http_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_http_client()


app = FastAPI(
    title="MIKUCHAT Bot API",
    description="MIKUCHAT 聊天机器人后端 API 系统",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins if settings.cors_origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AuthError)
async def auth_error_handler(request: Request, exc: AuthError):
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail})


@app.exception_handler(NotFoundError)
async def not_found_error_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail})


@app.exception_handler(BadRequestError)
async def bad_request_error_handler(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail})


@app.exception_handler(ForbiddenError)
async def forbidden_error_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail})


@app.exception_handler(ConflictError)
async def conflict_error_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=exc.status_code, content={"code": exc.status_code, "message": exc.detail})


from app.routers import user, cave, prize, assistant, email, minecraft, rss, moauth, baidu, bangumi, btsoft, doujinshi, myuz, osu, statistics, storm, invitation  # noqa: E402

app.include_router(user.router, prefix="/api/user", tags=["用户"])
app.include_router(cave.router, prefix="/api/cave", tags=["回声洞"])
app.include_router(prize.router, prefix="/api/prize", tags=["奖池"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["AI助手"])
app.include_router(email.router, prefix="/api/email", tags=["邮件"])
app.include_router(minecraft.router, prefix="/api/minecraft", tags=["Minecraft"])
app.include_router(rss.router, prefix="/api/rss", tags=["RSS/订阅"])
app.include_router(moauth.router, prefix="/api/moauth", tags=["MOAuth"])
app.include_router(baidu.router, prefix="/api/baidu", tags=["百度审核"])
app.include_router(bangumi.router, prefix="/api/bangumi", tags=["番组计划"])
app.include_router(btsoft.router, prefix="/api/btsoft", tags=["宝塔面板"])
app.include_router(doujinshi.router, prefix="/api/doujinshi", tags=["同人志"])
app.include_router(myuz.router, prefix="/api/myuz", tags=["云盘"])
app.include_router(osu.router, prefix="/api/osu", tags=["osu!"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["统计"])
app.include_router(storm.router, prefix="/api/storm", tags=["图片生成"])
app.include_router(invitation.router, prefix="/api/invitation", tags=["邀请码"])


@app.get("/")
async def root():
    return {"message": "MIKUCHAT Bot API v3.0", "docs": "/docs"}
