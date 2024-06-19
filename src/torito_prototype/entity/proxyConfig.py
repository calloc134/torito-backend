import re

# ホスト名は任意の文字列もしくはアドレス、ポート番号は1~5桁の数字
proxyPattern = r"^([a-zA-Z0-9.-]+):\d{1,5}$"

class ProxyConfig: 

    HTTPProxyParams: list[str]
    HTTPProxyAuthenticatorParams: list[str]
    HTTPSProxyParams: list[str]
    HTTPSProxyAuthenticatorParams: list[str]
    Socks4ProxyParams: list[str]
    Socks5ProxyParams: list[str]
    Socks5ProxyUsernameParams: list[str]
    Socks5ProxyPasswordParams: list[str]


    # 基本的にファクトリメソッドを利用するようにする
    def __init__(self, HTTPProxyParams: list[str], HTTPProxyAuthenticatorParams: list[str], HTTPSProxyParams: list[str], HTTPSProxyAuthenticatorParams: list[str], Socks4ProxyParams: list[str], Socks5ProxyParams: list[str], Socks5ProxyUsernameParams: list[str], Socks5ProxyPasswordParams: list[str]):

        # vaildate proxy parameters
        # ここでは正規表現でフォーマットを確認
        for HTTPProxyParam in HTTPProxyParams:
            if not re.match(proxyPattern, HTTPProxyParam):
                raise ValueError(f"Invalid HTTPProxy Parameter: {HTTPProxyParam}")
        for HTTPProxyAuthenticatorParam in HTTPProxyAuthenticatorParams:
            if not re.match(proxyPattern, HTTPProxyAuthenticatorParam):
                raise ValueError(f"Invalid HTTPProxyAuthenticator Parameter: {HTTPProxyAuthenticatorParam}")
        for HTTPSProxyParam in HTTPSProxyParams:
            if not re.match(proxyPattern, HTTPSProxyParam):
                raise ValueError(f"Invalid HTTPSProxy Parameter: {HTTPSProxyParam}")
        for HTTPSProxyAuthenticatorParam in HTTPSProxyAuthenticatorParams:
            if not re.match(proxyPattern, HTTPSProxyAuthenticatorParam):
                raise ValueError(f"Invalid HTTPSProxyAuthenticator Parameter: {HTTPSProxyAuthenticatorParam}")
        for Socks4ProxyParam in Socks4ProxyParams:
            if not re.match(proxyPattern, Socks4ProxyParam):
                raise ValueError(f"Invalid Socks4Proxy Parameter: {Socks4ProxyParam}")
        for Socks5ProxyParam in Socks5ProxyParams:
            if not re.match(proxyPattern, Socks5ProxyParam):
                raise ValueError(f"Invalid Socks5Proxy Parameter: {Socks5ProxyParam}")
            
        self.HTTPProxyParams = HTTPProxyParams
        self.HTTPProxyAuthenticatorParams = HTTPProxyAuthenticatorParams
        self.HTTPSProxyParams = HTTPSProxyParams
        self.HTTPSProxyAuthenticatorParams = HTTPSProxyAuthenticatorParams
        self.Socks4ProxyParams = Socks4ProxyParams
        self.Socks5ProxyParams = Socks5ProxyParams
        self.Socks5ProxyUsernameParams = Socks5ProxyUsernameParams
        self.Socks5ProxyPasswordParams = Socks5ProxyPasswordParams