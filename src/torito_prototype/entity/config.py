from .proxyConfig import ProxyConfig
from .bridgeConfig import BridgeConfig

class Config:
    useBridge: bool
    bridgeConfig: BridgeConfig  
    proxyConfig: ProxyConfig
    others: list[str]

    def __init__(self, useBridge: bool, bridgeConfig: BridgeConfig, proxyConfig: ProxyConfig, others: list[str]):
        # validate 
        if not isinstance(useBridge, bool):
            raise ValueError(f"Invalid useBridge: {useBridge}")
        if not isinstance(others, list):
            raise ValueError(f"Invalid others: {others}")
        if not isinstance(bridgeConfig, BridgeConfig):
            raise ValueError(f"Invalid BridgeConfig: {bridgeConfig}")
        if not isinstance(proxyConfig, ProxyConfig):
            raise ValueError(f"Invalid ProxyConfig: {proxyConfig}")
        self.useBridge = useBridge
        self.others = others
        self.bridgeConfig = bridgeConfig
        self.proxyConfig = proxyConfig
        