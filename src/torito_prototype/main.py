
from torito_prototype.repository.torrcRepository import TorrcRepository
from torito_prototype.usecase.handle import Handle

# fastapiのエンドポイントを作成する
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

class Dto(BaseModel):
    useBridge: bool
    BridgeText: str
    ProxyText: str
    others: list[str]
    backUpPath: str
    useDefaultBridges: bool

def main():
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

    # path = input("torrcのパスを入力してください: ")
    path = "/home/user/git-space/torito-prototype/src/torito_prototype/torrc.example"
    usecase = Handle(TorrcRepository(path))

    @app.get("/torrc")
    def get_torrc():
        dto = usecase.load()
        return dto
    
    @app.post("/torrc")
    def post_torrc(dto: Dto):
        try:
            usecase.save(dto=dto)
            return {"message": "torrc saved"}
        except Exception as e:
            return {"message": f"Error: {e}"}
    
    

    uvicorn.run(app, host="0.0.0.0", port=3001)

main()