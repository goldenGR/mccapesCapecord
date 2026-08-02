from database.supabase import supabase


def getDynamics():
    try:
        response = (
            supabase.schema("mccapes")
            .table("dynamic")
            .select("url,name,category")
            .execute()
        )

        return (True, response.data)

    except Exception as e:
        return (False, e)

def getDynamicContentById(id: str):
    try:
        response = (
            supabase.schema("mccapes").table("dynamic")
            .select("id,last_editor_id, content, type")
            .eq("id", id)
            .execute()
        )

        return (True, response.data)

    except Exception as e:
        print(e)
        return (False, e)