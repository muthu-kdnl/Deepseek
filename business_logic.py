import database


def list_items() -> list[dict]:
    return database.list_items()


def create_item(name: str) -> dict:
    cleaned_name = name.strip()
    if not cleaned_name:
        raise ValueError("Item name must not be blank")
    return database.create_item(cleaned_name)
