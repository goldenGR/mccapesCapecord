def deleteVouchById(ID, supabase):
    try:
        response = (
            supabase.schema("mccapes").table("vouches")
            .delete()
            .eq("id", ID)
            .execute()
        )

        print("SUCCESS:", response)
        return (True, response)

    except Exception as e:
        return (False, e)
    

# DELETED ALL USERS VOUCH, KINDA DANGEROUS
def deleteVouchesByUserId(userId, supabase):
    try:
        response = (
            supabase.schema("mccapes").table("vouches")
            .delete()
            .eq("vouchee", userId)
            .execute()
        )

        print("SUCCESS:", response)
        return (True, response)

    except Exception as e:
        return (False, e)