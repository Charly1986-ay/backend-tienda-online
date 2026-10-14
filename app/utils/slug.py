import unicodedata


def convert_slug(title: str) -> str:
    normalized = unicodedata.normalize('NFKD', title).encode(
        'ascii', 'ignore').decode('utf-8')
    
    return '-'.join(normalized.lower().split())