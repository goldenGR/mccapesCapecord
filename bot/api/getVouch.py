def getVoucheByID(ID, supabase):
    try:
        response = (
            supabase.schema("mccapes").table("vouches")
            .select("*")
            .eq("id", ID)
            .execute()
        )

        print("SUCCESS:", response)
        return (True, response)

    except Exception as e:
        # print("ERROR inserting vouch:", e)
        return (False, e)