from flask import Blueprint, redirect, render_template, request, g

from database.getDynamicById import getDynamicById
from database.user import checkSession, getUserById
pages_bp = Blueprint("pages", __name__)

@pages_bp.before_request
def require_login():
    if request.endpoint in ("pages.login", "pages.discord_callback"):
        return

    session = request.cookies.get("session")
    if not session:
        return redirect("/login")

    session = checkSession(session)
    if not session[0] or not session[1]:
        return redirect("/login")

    session = session[1][0]

    user = getUserById(session["user_id"])
    if not user[0] or not user[1] or not user[1][0]["staff"]:
        return redirect("/login")

    g.user = user[1][0]

@pages_bp.route("/dash")
def dashboard():

    return render_template(
        "dash.html",
        page_title="Dashboard",
        user_id=g.user["discordID"],
        username=g.user["username"]
    )

@pages_bp.route("/dash/tickets")
def tickets():

    MMACM = getDynamicById("MMACM")[1]["content"]
    print(MMACM)

    return render_template(
        "tickets.html",
        page_title="Tickets",
        MMACM=MMACM
    )