import re

def is_user_mention(text: str):
    return re.fullmatch(r"<@!?\d+>", text) is not None

def is_user_id(id_str: str) -> bool:
    if not id_str.isdigit():
        return False
    id_int = int(id_str)
    # Discord snowflakes are 64-bit unsigned integers,
    # and the epoch starts 2015-01-01, so anything too small isn't a real snowflake
    return 0 < id_int < 2**63 and id_int > 4194304  # first Discord snowflake ever generated


async def sendDm(client, userId, msg="", embed=""):
    user = await client.fetch_user(userId)
    await user.send(msg, embed=embed)
