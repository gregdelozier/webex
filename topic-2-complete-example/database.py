from bson.objectid import ObjectId
from mongita import MongitaClientDisk

client = None
db = None
pets_collection = None


class NotFoundError(LookupError):
    pass


class ConstraintError(ValueError):
    pass


def initialize(database_name="pets", client_factory=MongitaClientDisk):
    global client, db, pets_collection

    close_connection()

    client = client_factory()
    db = client[database_name]
    pets_collection = db.pets


def setup_database(database_name="pets", client_factory=MongitaClientDisk):
    initialize(database_name, client_factory=client_factory)
    pets_collection.count_documents({})


def close_connection():
    global client, db, pets_collection

    if client is not None:
        try:
            client.close()
        except Exception:
            pass
    client = None
    db = None
    pets_collection = None


def _normalize_age(value):
    try:
        return int(value)
    except Exception:
        return 0


def _require_text(value, field_name):
    text = (value or "").strip()
    if text == "":
        raise ValueError(f"{field_name} is required.")
    return text


def _to_object_id(value, field_name="id"):
    try:
        return ObjectId(str(value))
    except Exception as exc:
        raise ValueError(f"{field_name} must be a valid ObjectId string.") from exc


def _require_existing_pet(id):
    object_id = _to_object_id(id, "pet id")
    pet = pets_collection.find_one({"_id": object_id})
    if pet is None:
        raise NotFoundError("pet not found.")
    return object_id, pet


def _normalize_pet_data(data):
    return {
        "name": _require_text(data.get("name"), "name"),
        "type": _require_text(data.get("type"), "type"),
        "age": _normalize_age(data.get("age")),
        "owner": _require_text(data.get("owner"), "owner"),
    }


def _ensure_unique_pet_owner(name, owner, exclude_id=None):
    query = {"name": name, "owner": owner}
    existing_pet = pets_collection.find_one(query)

    if existing_pet is None:
        return

    existing_id = str(existing_pet["_id"])
    if exclude_id is not None and existing_id == str(exclude_id):
        return

    raise ConstraintError("a pet with this name already exists for this owner.")


def pet_to_dict(pet):
    return {
        "id": str(pet["_id"]),
        "name": pet["name"],
        "type": pet["type"],
        "age": pet["age"],
        "owner": pet["owner"],
    }


def get_pets():
    return [pet_to_dict(pet) for pet in pets_collection.find()]


def get_pet(id):
    object_id = _to_object_id(id, "pet id")
    pet = pets_collection.find_one({"_id": object_id})
    if pet is None:
        return None
    return pet_to_dict(pet)


def create_pet(data):
    pet = _normalize_pet_data(data)
    _ensure_unique_pet_owner(pet["name"], pet["owner"])
    result = pets_collection.insert_one(pet)
    return str(result.inserted_id)


def update_pet(id, data):
    object_id, _ = _require_existing_pet(id)
    pet = _normalize_pet_data(data)
    _ensure_unique_pet_owner(pet["name"], pet["owner"], exclude_id=object_id)
    pets_collection.update_one({"_id": object_id}, {"$set": pet})


def delete_pet(id):
    object_id, _ = _require_existing_pet(id)
    pets_collection.delete_one({"_id": object_id})


def reset():
    pets_collection.delete_many({})

    sample_pets = [
        {"name": "Dorothy", "type": "dog", "age": 9, "owner": "Greg"},
        {"name": "Heidi", "type": "dog", "age": 15, "owner": "David"},
        {"name": "Sandy", "type": "cat", "age": 2, "owner": "Janet"},
        {"name": "Suzy", "type": "dog", "age": 2, "owner": "Greg"},
        {"name": "Squeakers", "type": "hamster", "age": 1, "owner": "Christopher"},
    ]

    for pet in sample_pets:
        create_pet(pet)
