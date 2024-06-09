
from torito_prototype.repository.torrcRepository import TorrcRepository
from torito_prototype.usecase.handle import Handle

# fastapiのエンドポイントを作成する
from fastapi import FastAPI
import uvicorn
app = FastAPI()


def main():
    # 初期化

    # path = input("torrcのパスを入力してください: ")
    path = "/home/user/git-space/torito-prototype/src/torito_prototype/torrc.example"
    usecase = Handle(TorrcRepository(path))

    @app.get("/torrc")
    def get_torrc():
        dto = usecase.load()
        return dto
    
    @app.post("/torrc")
    def post_torrc():
        try:
            usecase.save()
            return {"message": "torrc saved"}
        except Exception as e:
            return {"message": f"Error: {e}"}
        
    uvicorn.run(app, host="0.0.0.0", port=8000)

main()