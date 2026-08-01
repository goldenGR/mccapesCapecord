from database.supabase import supabase


def getDynamicById(id: str):
    try:
        response = (
            supabase.schema("mccapes").table("dynamic")
            .select("*")
            .eq("id", id)
            .execute()
        )

        return (True, response.data[0])

    except Exception as e:
        return (False, e)