import json


def tentar_json(texto: str):
    try:
        return json.loads(texto)
    except Exception:
        return None