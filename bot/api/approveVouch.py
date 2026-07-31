def approveVouchById(ID, supabase, aproove=True):
    try:
        response = (
            supabase.schema("mccapes").table("vouches")
            .update({"verified": aproove})
            .eq("id", ID)
            .execute()
        )

        print("SUCCESS:", response)
        return (True, response)

    except Exception as e:
        return (False, e)