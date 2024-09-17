def response_creation(message: str, _id: str) -> dict:
    return {
        "_id": _id,
        "message": message,
    }
