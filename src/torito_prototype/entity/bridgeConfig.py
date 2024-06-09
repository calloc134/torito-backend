import re 

bridgePattern = re.compile(
    r"(?P<type>obfs4|snowflake|meek-azure) (?P<ip>[\d\.]+|\[[0-9a-fA-F:]+\]):(?P<port>\d{1,5}) (?P<key>[0-9A-F]{40}) cert=(?P<cert>[a-zA-Z0-9+/=]+) iat-mode=(?P<iat_mode>\d)"
)


class BridgeConfig:
    bridgeParams: list[str]

    def __init__(self, bridgeParams: list[str]):

        # validate bridge parameters
        # ここでは正規表現でフォーマットを確認
        for bridgeParam in bridgeParams:
            if not bridgePattern.match(bridgeParam):
                raise ValueError(f"Invalid bridge parameter: {bridgeParam}")
            
        self.bridgeParams = bridgeParams