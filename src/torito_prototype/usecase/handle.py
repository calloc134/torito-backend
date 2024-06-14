import re
from torito_prototype.repository.torrcRepository import TorrcRepository
from torito_prototype.entity.config import Config, ProxyConfig, BridgeConfig
from datetime import datetime, timezone

bridgeEntryPattern = re.compile(
    r"(?P<directive>Bridge )(?P<args>.*)"
)

proxyEntryPattern = re.compile(
    r"(?P<directive>HTTPProxy |HTTPProxyAuthenticator |HTTPSProxy |HTTPSProxyAuthenticator |Socks4Proxy |Socks5Proxy |Socks5ProxyUsername |Socks5ProxyPassword )(?P<args>.*)"
)


# デフォルトのブリッジ内容
defaultBridge = [
    "obfs4 144.217.20.138:80 FB70B257C162BF1038CA669D568D76F5B7F0BABB cert=vYIV5MgrghGQvZPIi1tJwnzorMgqgmlKaB77Y3Z9Q/v94wZBOAXkW+fdx4aSxLVnKO+xNw iat-mode=0",
    "obfs4 85.31.186.26:443 91A6354697E6B02A386312F68D82CF86824D3606 cert=PBwr+S8JTVZo6MPdHnkTwXJPILWADLqfMGoVvhZClMq/Urndyd42BwX9YFJHZnBB3H0XCw iat-mode=0",
    "obfs4 37.218.245.14:38224 D9A82D2F9C2F65A18407B1D2B764F130847F8B5D cert=bjRaMrr1BRiAW8IE9U5z27fQaYgOhX1UCmOpg2pFpoMvo6ZgQMzLsaTzzQNTlm7hNcb+Sg iat-mode=0",
    "obfs4 193.11.166.194:27025 1AE2C08904527FEA90C4C4F8C1083EA59FBC6FAF cert=ItvYZzW5tn6v3G4UnQa6Qz04Npro6e81AP70YujmK/KXwDFPTs3aHXcHp4n8Vt6w/bv8cA iat-mode=0",
    "obfs4 [2a0c:4d80:42:702::1]:27015 C5B7CD6946FF10C5B3E89691A7D3F2C122D2117C cert=TD7PbUO0/0k6xYHMPW3vJxICfkMZNdkRrb63Zhl5j9dW3iRGiCx0A7mPhe5T2EDzQ35+Zw iat-mode=0",
    "obfs4 45.145.95.6:27015 C5B7CD6946FF10C5B3E89691A7D3F2C122D2117C cert=TD7PbUO0/0k6xYHMPW3vJxICfkMZNdkRrb63Zhl5j9dW3iRGiCx0A7mPhe5T2EDzQ35+Zw iat-mode=0",
    "obfs4 209.148.46.65:443 74FAD13168806246602538555B5521A0383A1875 cert=ssH+9rP8dG2NLDN2XuFw63hIO/9MNNinLmxQDpVa+7kTOa9/m+tGWT1SmSYpQ9uTBGa6Hw iat-mode=0",
    "obfs4 85.31.186.98:443 011F2599C0E9B27EE74B353155E244813763C3E5 cert=ayq0XzCwhpdysn5o0EyDUbmSOx3X/oTEbzDMvczHOdBJKlvIdHHLJGkZARtT4dcBFArPPg iat-mode=0",
    "obfs4 193.11.166.194:27015 2D82C2E354D531A68469ADF7F878FA6060C6BACA cert=4TLQPJrTSaDffMK7Nbao6LC7G9OW/NHkUwIdjLSS3KYf0Nv4/nQiiI8dY2TcsQx01NniOg iat-mode=0",
    "obfs4 51.222.13.177:80 5EDAC3B810E12B01F6FD8050D2FD3E277B289A08 cert=2uplIpLQ0q9+0qMFrK5pkaYRDOe460LL9WHBvatgkuRr/SL31wBOEupaMMJ6koRE6Ld0ew iat-mode=0",
    "obfs4 38.229.33.83:80 0BAC39417268B96B9F514E7F63FA6FBA1A788955 cert=VwEFpk9F/UN9JED7XpG1XOjm/O8ZCXK80oPecgWnNDZDv5pdkhq1OpbAH0wNqOT6H6BmRQ iat-mode=1",
    "obfs4 193.11.166.194:27020 86AC7B8D430DAC4117E9F42C9EAED18133863AAF cert=0LDeJH4JzMDtkJJrFphJCiPqKx7loozKN7VNfuukMGfHO0Z8OGdzHVkhVAOfo1mUdv9cMg iat-mode=0",
    "obfs4 192.95.36.142:443 CDF2E852BF539B82BD10E27E9115A31734E378C2 cert=qUVQ0srL1JI/vO6V6m/24anYXiJD3QP2HgzUKQtQ7GRqqUvs7P+tG43RtAqdhLOALP7DJQ iat-mode=1",
]


class Dto:
    useBridge: bool
    useDefaultBridges: bool
    BridgeText: str
    ProxyText: str
    backUpPath: str
    others: list[str]

    def __init__(self, useBridge: bool, BridgeText: str, ProxyText: str, others: list[str], backUpPath: str, useDefaultBridges: bool):
        self.useBridge = useBridge
        self.useDefaultBridges = useDefaultBridges
        self.BridgeText = BridgeText
        self.ProxyText = ProxyText
        self.others = others
        self.backUpPath = backUpPath

class Handle:
    torrcRepository: TorrcRepository

    def __init__(self, torrcRepository: TorrcRepository):
        self.torrcRepository = torrcRepository

    def load(self) -> Dto:
        config = self.torrcRepository.load()

        bridgeText = "\n".join(f"Bridge {bridgeParam}" for bridgeParam in config.bridgeConfig.bridgeParams)
        proxyText = "\n".join(f"HTTPProxy {HTTPProxyParam}" for HTTPProxyParam in config.proxyConfig.HTTPProxyParams) + "\n" + \
            "\n".join(f"HTTPProxyAuthenticator {HTTPProxyAuthenticatorParam}" for HTTPProxyAuthenticatorParam in config.proxyConfig.HTTPProxyAuthenticatorParams) + "\n" + \
            "\n".join(f"HTTPSProxy {HTTPSProxyParam}" for HTTPSProxyParam in config.proxyConfig.HTTPSProxyParams) + "\n" + \
            "\n".join(f"HTTPSProxyAuthenticator {HTTPSProxyAuthenticatorParam}" for HTTPSProxyAuthenticatorParam in config.proxyConfig.HTTPSProxyAuthenticatorParams) + "\n" + \
            "\n".join(f"Socks4Proxy {Socks4ProxyParam}" for Socks4ProxyParam in config.proxyConfig.Socks4ProxyParams) + "\n" + \
            "\n".join(f"Socks5Proxy {Socks5ProxyParam}" for Socks5ProxyParam in config.proxyConfig.Socks5ProxyParams) + "\n" + \
            "\n".join(f"Socks5ProxyUsername {Socks5ProxyUsernameParam}" for Socks5ProxyUsernameParam in config.proxyConfig.Socks5ProxyUsernameParams) + "\n" + \
            "\n".join(f"Socks5ProxyPassword {Socks5ProxyPasswordParam}" for Socks5ProxyPasswordParam in config.proxyConfig.Socks5ProxyPasswordParams) + "\n"
        
        # 現在の時刻としてバックアップファイル名を生成
        backUpPath = f"/home/user/git-space/torito-prototype/src/torito_prototype/torrc.bak.{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"

        # デフォルトブリッジであるかどうか
        useDefaultBridges = config.bridgeConfig.bridgeParams == defaultBridge

        dto = Dto(
            useBridge=config.useBridge,
            BridgeText=bridgeText,
            ProxyText=proxyText,
            others=config.others,
            # backUpPath="/etc/tor/torrc.bak"
            backUpPath=backUpPath,
            useDefaultBridges=useDefaultBridges
        )

        return dto
    
    def save(self, dto: Dto) -> None:

        # まずtorrcをバックアップ
        self.torrcRepository.backup(backupPath=dto.backUpPath)

        # configとして解析
        tmp = {
            "UseBridges": dto.useBridge,
            # デフォルトブリッジを利用する場合
            "Bridge": [],
            "HTTPProxy": [],
            "HTTPProxyAuthenticator": [],
            "HTTPSProxy": [],
            "HTTPSProxyAuthenticator": [],
            "Socks4Proxy": [],
            "Socks5Proxy": [],
            "Socks5ProxyUsername": [],
            "Socks5ProxyPassword": [],
            "others": []
        }

        tmp["others"] = dto.others

        # デフォルトブリッジを利用するかどうかの条件分岐が必要
        if dto.useDefaultBridges:
            tmp["Bridge"] = defaultBridge
        else:
            for line in dto.BridgeText.split("\n"):
                match = bridgeEntryPattern.match(line)
                if match:
                    directive = match.group("directive").strip()
                    args = match.group("args").strip()

                    match directive:
                        case "Bridge":
                            tmp["Bridge"].append(args)
                        case _:
                            tmp["others"].append(line)
        
        for line in dto.ProxyText.split("\n"):
            match = proxyEntryPattern.match(line)
            if match:
                directive = match.group("directive").strip()
                args = match.group("args").strip()

                match directive:
                    case "HTTPProxy":
                        tmp["HTTPProxy"].append(args)
                    case "HTTPProxyAuthenticator":
                        tmp["HTTPProxyAuthenticator"].append(args)
                    case "HTTPSProxy":
                        tmp["HTTPSProxy"].append(args)
                    case "HTTPSProxyAuthenticator":
                        tmp["HTTPSProxyAuthenticator"].append(args)
                    case "Socks4Proxy":
                        tmp["Socks4Proxy"].append(args)
                    case "Socks5Proxy":
                        tmp["Socks5Proxy"].append(args)
                    case "Socks5ProxyUsername":
                        tmp["Socks5ProxyUsername"].append(args)
                    case "Socks5ProxyPassword":
                        tmp["Socks5ProxyPassword"].append(args)
                    case _:
                        tmp["others"].append(line)

        config = Config(
            useBridge=tmp["UseBridges"],
            bridgeConfig=BridgeConfig(bridgeParams=tmp["Bridge"]),
            proxyConfig=ProxyConfig(
                HTTPProxyParams=tmp["HTTPProxy"],
                HTTPProxyAuthenticatorParams=tmp["HTTPProxyAuthenticator"],
                HTTPSProxyParams=tmp["HTTPSProxy"],
                HTTPSProxyAuthenticatorParams=tmp["HTTPSProxyAuthenticator"],
                Socks4ProxyParams=tmp["Socks4Proxy"],
                Socks5ProxyParams=tmp["Socks5Proxy"],
                Socks5ProxyUsernameParams=tmp["Socks5ProxyUsername"],
                Socks5ProxyPasswordParams=tmp["Socks5ProxyPassword"]
            ),
            others=tmp["others"]
        )

        self.torrcRepository.save(config)
        