def getVouches(userId, supabase):
    try:
        response = (
            supabase.schema("mccapes").table("vouches")
            .select("*")
            .eq("vouchee", userId)
            .execute()
        )

        print("SUCCESS:", response)
        return (True, response)

    except Exception as e:
        # print("ERROR inserting vouch:", e)
        return (False, e)