import re

def is_user_mention(text: str):
    return re.fullmatch(r"<@!?\d+>", text) is not None

async def sendDm(client, userId, msg="", embed=""):
    user = await client.fetch_user(userId)
    await user.send(msg, embed=embed)
