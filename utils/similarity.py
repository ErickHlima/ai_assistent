import difflib
import json


def similaridade(a, b) -> float:
    a_txt = json.dumps(a, ensure_ascii=False, sort_keys=True)
    b_txt = json.dumps(b, ensure_ascii=False, sort_keys=True)
    return difflib.SequenceMatcher(None, a_txt, b_txt).ratio()