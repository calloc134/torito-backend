

from .proxyConfig import ProxyConfig
from .bridgeConfig import BridgeConfig


class Config:
    useBridge: bool
    BridgeConfig: BridgeConfig
    ProxyConfig: ProxyConfig
    others: list[str]

    def __init__(self, useBridge: bool, BridgeConfig: BridgeConfig, ProxyConfig: ProxyConfig, others: list[str]):
        # validate 
        if not isinstance(useBridge, bool):
            raise ValueError(f"Invalid useBridge: {useBridge}")
        if not isinstance(others, list):
            raise ValueError(f"Invalid others: {others}")
        if not isinstance(BridgeConfig, BridgeConfig):
            raise ValueError(f"Invalid BridgeConfig: {BridgeConfig}")
        if not isinstance(ProxyConfig, ProxyConfig):
            raise ValueError(f"Invalid ProxyConfig: {ProxyConfig}")
        self.useBridge = useBridge
        self.others = others
        self.BridgeConfig = BridgeConfig
        self.ProxyConfig = ProxyConfig
        