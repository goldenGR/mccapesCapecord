import os
import secrets
import urllib.parse

import requests

from dotenv import load_dotenv

load_dotenv()


class MicrosoftAuthError(Exception):
    pass


class XboxAuthError(Exception):
    pass


class XSTSError(Exception):
    pass


class MinecraftAuthError(Exception):
    pass


class NoMinecraftLicense(Exception):
    pass


class MicrosoftMinecraftAuth:

    AUTHORITY = "https://login.microsoftonline.com/consumers/oauth2/v2.0"

    def __init__(self):

        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.redirect_uri = os.getenv("REDIRECT_URI")

        if not self.client_id:
            raise ValueError("CLIENT_ID missing")

        if not self.client_secret:
            raise ValueError("CLIENT_SECRET missing")

        if not self.redirect_uri:
            raise ValueError("REDIRECT_URI missing")

    def get_login_url(self):

        state = secrets.token_urlsafe(32)

        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "response_mode": "query",
            "scope": "XboxLive.signin offline_access",
            "state": state,
        }

        url = (
            self.AUTHORITY
            + "/authorize?"
            + urllib.parse.urlencode(params)
        )

        return {
            "url": url,
            "state": state,
        }

    def finish_login(self, code):

        ###########################################################
        # Microsoft Token
        ###########################################################

        token = requests.post(
            self.AUTHORITY + "/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": self.redirect_uri,
            },
        ).json()

        if "access_token" not in token:
            raise MicrosoftAuthError(token)

        ms_access = token["access_token"]
        refresh_token = token.get("refresh_token")

        ###########################################################
        # Xbox Live
        ###########################################################

        xbl = requests.post(
            "https://user.auth.xboxlive.com/user/authenticate",
            json={
                "Properties": {
                    "AuthMethod": "RPS",
                    "SiteName": "user.auth.xboxlive.com",
                    "RpsTicket": f"d={ms_access}",
                },
                "RelyingParty": "http://auth.xboxlive.com",
                "TokenType": "JWT",
            },
        ).json()

        if "Token" not in xbl:
            raise XboxAuthError(xbl)

        xbl_token = xbl["Token"]
        uhs = xbl["DisplayClaims"]["xui"][0]["uhs"]

        ###########################################################
        # XSTS
        ###########################################################

        xsts = requests.post(
            "https://xsts.auth.xboxlive.com/xsts/authorize",
            json={
                "Properties": {
                    "SandboxId": "RETAIL",
                    "UserTokens": [xbl_token],
                },
                "RelyingParty": "rp://api.minecraftservices.com/",
                "TokenType": "JWT",
            },
        ).json()

        if "Token" not in xsts:
            raise XSTSError(xsts)

        xsts_token = xsts["Token"]

        ###########################################################
        # Minecraft
        ###########################################################

        mc = requests.post(
            "https://api.minecraftservices.com/authentication/login_with_xbox",
            json={
                "identityToken": f"XBL3.0 x={uhs};{xsts_token}"
            },
        ).json()

        if "access_token" not in mc:
            raise MinecraftAuthError(mc)

        mc_token = mc["access_token"]

        ###########################################################
        # Profile
        ###########################################################

        profile = requests.get(
            "https://api.minecraftservices.com/minecraft/profile",
            headers={
                "Authorization": f"Bearer {mc_token}"
            },
        )

        if profile.status_code == 404:
            raise NoMinecraftLicense(
                "Account does not own Minecraft."
            )

        profile.raise_for_status()

        profile = profile.json()

        return {
            "minecraft_access_token": mc_token,
            "refresh_token": refresh_token,
            "expires_in": mc["expires_in"],
            "profile": {
                "uuid": profile["id"],
                "name": profile["name"],
            },
        }

    def refresh(self, refresh_token):

        token = requests.post(
            self.AUTHORITY + "/token",
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "refresh_token": refresh_token,
                "grant_type": "refresh_token",
                "redirect_uri": self.redirect_uri,
            },
        ).json()

        if "access_token" not in token:
            raise MicrosoftAuthError(token)

        return self.finish_microsoft_access(
            token["access_token"],
            token.get("refresh_token", refresh_token),
        )

    def finish_microsoft_access(self, microsoft_access, refresh_token):
        """
        Optional helper if you already have a Microsoft access token.
        Implement the Xbox → XSTS → Minecraft flow here to avoid duplicating
        code between finish_login() and refresh().
        """
        raise NotImplementedError