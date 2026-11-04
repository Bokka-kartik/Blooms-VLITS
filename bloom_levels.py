_BLOOM_LEVEL_ALIASES = {
    "remember": "remember",
    "remembering": "remember",
    "understand": "understand",
    "understanding": "understand",
    "understandinging": "understand",
    "apply": "apply",
    "applying": "apply",
    "analyze": "analyze",
    "analyzing": "analyze",
    "evaluate": "evaluate",
    "evaluating": "evaluate",
    "create": "create",
    "creating": "create",
}


def normalize_bloom_level(value: object) -> str:
    if not isinstance(value, str):
        return ""
    normalized = " ".join(value.split()).casefold()
    return _BLOOM_LEVEL_ALIASES.get(normalized, normalized)
