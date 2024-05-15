from requests import post, get
import webbrowser
from json import loads, dumps



def oauth():
    # 重定向
    webbrowser.open("https://login.live.com/oauth20_authorize.srf\
    ?client_id=00000000402b5328\
    &response_type=code\
    &scope=service%3A%3Auser.auth.xboxlive.com%3A%3AMBI_SSL\
    &redirect_uri=https%3A%2F%2Flogin.live.com%2Foauth20_desktop.srf")
    result = input("请输入重定向链接：")
    begin = result.find("code=") + 5
    end = result.find("&lc")
    code = str("")
    for i in range(begin, end):
        code += result[i]
    data = {
        "client_id": "00000000402b5328", 
        "code": code, 
        "grant_type": "authorization_code",
        "redirect_uri": "https://login.live.com/oauth20_desktop.srf",
        "scope": "service::user.auth.xboxlive.com::MBI_SSL"
    }
    url = "https://login.live.com/oauth20_token.srf"
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = post(url = url, data = data, headers = header)
    dic = loads(res.text)
    access_token = dic["access_token"]
    # Xbox Live 验证
    data = dumps({
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": access_token
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    })
    url = "https://user.auth.xboxlive.com/user/authenticate"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    res = post(url = url, data = data, headers = header)
    Token = loads(res.text)["Token"]
    uhs = str()
    for i in loads(res.text)["DisplayClaims"]["xui"]:
        uhs = i["uhs"]
    # XSTS 验证
    data = dumps({
        " Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [
                Token
            ]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    })
    url = "https://xsts.auth.xboxlive.com/xsts/authorize"
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    res = post(url = url, data = data, headers = header)
    dic = loads(res.text)
    XSTS_Token = dic["Token"]
    # 获取Minecrat访问令牌
    data = dumps({
        "identityToken": f"XBL3.0 x={uhs}{XSTS_Token}"
    })
    url = "https://api.minecraftservices.com/authentication/login_with_xbox"
    res = post(url = url, data = data)
    dic = loads(res.text)
    break dic["access_token"]
