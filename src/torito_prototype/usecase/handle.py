import re
from torito_prototype.repository import TorrcRepository
from torito_prototype.entity import config

bridgeEntryPattern = re.compile(
    r"(?P<directive>Bridge )(?P<args>.*)"
)

proxyEntryPattern = re.compile(
    r"(?P<directive>HTTPProxy |HTTPProxyAuthenticator |HTTPSProxy |HTTPSProxyAuthenticator |Socks4Proxy |Socks5Proxy |Socks5ProxyUsername |Socks5ProxyPassword )(?P<args>.*)"
)


class dto:
    useBridge: bool
    BridgeText: str
    ProxyText: str
    others: list[str]

    def __init__(self, useBridge: bool, BridgeText: str, ProxyText: str, others: list[str]):
        self.useBridge = useBridge
        self.BridgeText = BridgeText
        self.ProxyText = ProxyText
        self.others = others

class hande:
    torrcRepository: TorrcRepository

    def __init__(self, torrcRepository: TorrcRepository):
        self.torrcRepository = torrcRepository

    def load(self, dto: dto) -> dto:
        config = self.torrcRepository.load()

        bridgeText = "\n".join(f"Bridge {bridgeParam}" for bridgeParam in config.BridgeConfig.bridgeParams)
        proxyText = "\n".join(f"HTTPProxy {HTTPProxyParam}" for HTTPProxyParam in config.ProxyConfig.HTTPProxyParams) + "\n" + \
            "\n".join(f"HTTPProxyAuthenticator {HTTPProxyAuthenticatorParam}" for HTTPProxyAuthenticatorParam in config.ProxyConfig.HTTPProxyAuthenticatorParams) + "\n" + \
            "\n".join(f"HTTPSProxy {HTTPSProxyParam}" for HTTPSProxyParam in config.ProxyConfig.HTTPSProxyParams) + "\n" + \
            "\n".join(f"HTTPSProxyAuthenticator {HTTPSProxyAuthenticatorParam}" for HTTPSProxyAuthenticatorParam in config.ProxyConfig.HTTPSProxyAuthenticatorParams) + "\n" + \
            "\n".join(f"Socks4Proxy {Socks4ProxyParam}" for Socks4ProxyParam in config.ProxyConfig.Socks4ProxyParams) + "\n" + \
            "\n".join(f"Socks5Proxy {Socks5ProxyParam}" for Socks5ProxyParam in config.ProxyConfig.Socks5ProxyParams) + "\n" + \
            "\n".join(f"Socks5ProxyUsername {Socks5ProxyUsernameParam}" for Socks5ProxyUsernameParam in config.ProxyConfig.Socks5ProxyUsernameParams) + "\n" + \
            "\n".join(f"Socks5ProxyPassword {Socks5ProxyPasswordParam}" for Socks5ProxyPasswordParam in config.ProxyConfig.Socks5ProxyPasswordParams) + "\n"

        dto = dto(
            useBridge=config.useBridge,
            BridgeText=bridgeText,
            ProxyText=proxyText,
            others=config.others
        )

        return dto
    
    def save(self, dto: dto) -> None:
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

        config = config.Config(
            useBridge=tmp["UseBridges"],
            BridgeConfig=config.BridgeConfig(bridgeParams=tmp["Bridge"]),
            ProxyConfig=config.ProxyConfig(
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
        