from database.supabase import supabase


def getUserByDiscord(discordId: int):
    try:
        response = (
            supabase.schema("mccapes").table("users")
            .select("*")
            .eq("discordID", discordId)
            .execute()
        )

        return (True, response.data)

    except Exception as e:
        return (False, e)

def createUser(discordId, discordEmail, discordPFP, discordUsername):
    try:
        response = (
            supabase.schema("mccapes").table("users")
            .insert({
                "email": discordEmail,
                "username": discordUsername,
                "staff": False,
                "mm": False,
                "discordID": discordId,
                "pfp": discordPFP
            })
            .execute()
        )
        return (True, response.data)

    except Exception as e:
        return (False, e)

def createUserSession(userId, ip):
    try:
        response = (
            supabase.schema("mccapes").table("sessions")
            .insert({
                "user_id": userId,
                "ip": ip
            })
            .execute()
        )
        return (True, response.data[0])

    except Exception as e:
        return (False, e)

def checkSession(sessionToken):
    try:
        response = (
            supabase.schema("mccapes").table("sessions")
            .select("*")
            .eq("id", sessionToken)
            .execute()
        )

        return (True, response.data)

    except Exception as e:
        return (False, e)
    
def getUserById(id):
    try:
        response = (
            supabase.schema("mccapes").table("users")
            .select("*")
            .eq("id", id)
            .execute()
        )

        return (True, response.data)

    except Exception as e:
        return (False, e)