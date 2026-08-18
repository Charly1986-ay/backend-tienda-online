from math import ceil


def get_pagination(counter: int, page: int = 1, page_size: int = 10) -> dict:
    # Evitar división por cero si page_size llega corrupto o en 0
    if page_size <= 0:
        page_size = 10

    offset = (page - 1) * page_size
    
    return {
        'counter': counter,
        'pages': ceil(counter / page_size) if counter > 0 else 0,
        'offset': offset,
        'page': page,
        'page_size': page_size,
    }