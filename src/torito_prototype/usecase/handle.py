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


class Dto:
    useBridge: bool
    BridgeText: str
    ProxyText: str
    backUpPath: str
    others: list[str]

    def __init__(self, useBridge: bool, BridgeText: str, ProxyText: str, others: list[str], backUpPath: str):
        self.useBridge = useBridge
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

        dto = Dto(
            useBridge=config.useBridge,
            BridgeText=bridgeText,
            ProxyText=proxyText,
            others=config.others,
            # backUpPath="/etc/tor/torrc.bak"
            backUpPath=backUpPath
        )

        return dto
    
    def save(self, dto: Dto) -> None:

        # まずtorrcをバックアップ
        self.torrcRepository.backup(backupPath=dto.backUpPath)

        # configとして解析
        tmp = {
            "UseBridges": dto.useBridge,
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
        