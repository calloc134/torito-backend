

from .proxyConfig import ProxyConfig
from .bridgeConfig import BridgeConfig


class Config:
    useBridge: bool
    useDefaultBridge: bool
    useProxy: bool
    others: list[str]
    BridgeConfig: BridgeConfig
    ProxyConfig: ProxyConfig

    def __init__(self, useBridge: bool, useDefaultBridge: bool, useProxy: bool, others: list[str], BridgeConfig: BridgeConfig, ProxyConfig: ProxyConfig):
        # validate 
        if not isinstance(useBridge, bool):
            raise ValueError(f"Invalid useBridge: {useBridge}")
        if not isinstance(useDefaultBridge, bool):
            raise ValueError(f"Invalid useDefaultBridge: {useDefaultBridge}")
        if not isinstance(useProxy, bool):
            raise ValueError(f"Invalid useProxy: {useProxy}")
        if not isinstance(others, list):
            raise ValueError(f"Invalid others: {others}")
        if not isinstance(BridgeConfig, BridgeConfig):
            raise ValueError(f"Invalid BridgeConfig: {BridgeConfig}")
        if not isinstance(ProxyConfig, ProxyConfig):
            raise ValueError(f"Invalid ProxyConfig: {ProxyConfig}")
        self.useBridge = useBridge
        self.useDefaultBridge = useDefaultBridge
        self.useProxy = useProxy
        self.others = others
        self.BridgeConfig = BridgeConfig
        self.ProxyConfig = ProxyConfig
        