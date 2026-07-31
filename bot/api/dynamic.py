def getDynamic(ID, supabase, key):
    try:
        response = (
            supabase.schema("mccapes").table("dynamic")
            .select("*")
            .eq("id", ID)
            .execute()
            .single()
        )

        keyValue = response.data["content"][key]
        return (True, keyValue)

    except Exception as e:
        return (False, e)