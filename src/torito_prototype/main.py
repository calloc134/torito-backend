
from torito_prototype.repository.torrcRepository import TorrcRepository
from torito_prototype.repository.torControlRepository import TorControlRepository
from torito_prototype.usecase.handle import Handle

# fastapiのエンドポイントを作成する
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import tomllib
import platform

class Dto(BaseModel):
    useBridge: bool
    BridgeText: str
    ProxyText: str
    others: list[str]
    useDefaultBridges: bool

def main():

    # 実行デバイスを判定
    deviceType = platform.system()

    # toml構成ファイルを読み込む
    with open("./config.toml", "rb") as f:
        config = tomllib.load(f)

    path = config["torrcPath"]
    torIp = config["torIp"]
    torPort = config["torPort"]
    backUpDirName = config["backUpDirName"]

    app = FastAPI()

    # CORS対策
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    usecase = Handle(TorrcRepository(path=path, backUpDirName=backUpDirName), TorControlRepository(deviceType, torIp, torPort))

    # 初期化
    app = FastAPI()

    # CORS対策
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/torrc")
    def get_torrc():
        dto = usecase.load()
        return dto
    
    @app.post("/torrc")
    def post_torrc(dto: Dto) -> StreamingResponse:
        return StreamingResponse(usecase.save(dto=dto), media_type="text/event-stream")

    uvicorn.run(app, host="localhost", port=3001)

main()