from flask import Blueprint, make_response, redirect, request
import requests

from config import BOT_TOKEN, CLIENT_ID, CLIENT_SECRET, GUILD_ID, REDIRECT_URI
from database.user import createUser, createUserSession, getUserByDiscord

login_bp = Blueprint("login", __name__)

@login_bp.route("/login")
def login():
    return redirect(
        f"https://discord.com/oauth2/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=email+identify+guilds.join"
    )

@login_bp.route("/auth/discord/callback")
def callback():
    code = request.args.get("code")

    token_data = requests.post(
        "https://discord.com/api/oauth2/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    ).json()

    access_token = token_data["access_token"]

    user = requests.get(
        "https://discord.com/api/users/@me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    ).json()

    discordId = user["id"]
    discordEmail = user["email"]
    discordPFP = user["avatar"]
    discordUsername = user["username"]

    requests.put(
        f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{discordId}",
        headers={
            "Authorization": f"Bot {BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "access_token": access_token
        }
    )

    user = getUserByDiscord(discordId)
    print(user)
    if user[1] == []:
        print("had to create user")
        user = createUser(discordId, discordEmail, discordPFP, discordUsername)
        print(user)

    if user[0] == False:
        return(f"<h1>500 Internal Server Error</h1> An error ockured while trying to log you in. User error<br> {user[1]}")

    if user[1][0]["staff"] == False:
        print("woops 403")
        return(f"<h1> 403 Forbidden </h1> \n Seems like the user with id of {discordId} has no permision to acces this page")
    
    session = createUserSession(user[1][0]["id"], request.remote_addr)

    if session[0] == False:
        return(f"<h1>500 Internal Server Error</h1> An error ockured while trying to log you in. Session error<br> {session[1]}")

    response = make_response(redirect("/dash"))

    response.set_cookie(
        "session",
        session[1]["id"],
        path="/",
        httponly=True,
        secure=True,
        samesite="Lax",
        max_age=60 * 60 * 24 * 30
    )

    return response

@login_bp.route("/store")
def storeSession():
    sessionId = request.args('sessionId')
    return(f"SessionID: {sessionId}")