
from torito_prototype.repository.torrcRepository import TorrcRepository
from torito_prototype.usecase.handle import Handle
from pprint import pprint


def main():
    # 初期化

    # path = input("torrcのパスを入力してください: ")
    path = "/home/user/git-space/torito-prototype/src/torito_prototype/torrc.example"
    usecase = Handle(TorrcRepository(path))

    # torrc読み込み
    dto = usecase.load()
    pprint(dto.__dict__)

    # torrc保存
    usecase.torrcRepository.path = "torrc.new"

    usecase.save(dto)


main()