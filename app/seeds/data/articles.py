from decimal import Decimal

from app.api.v1.articles.models import UnitsType, StatusArticle

ARTICLES = [
    {
        'detail': 'Notebook Lenovo Ideapad 15.6"',
        'slug': 'notebook-lenovo-ideapad-156',
        'stock': 12,
        'stock_min': 2,
        'cost': Decimal('450.00'),
        'price': Decimal('699.99'),
        'brand_id': 11,  # Lenovo
        'category_id': 3,  # PCs, Tablets, Notebooks y Accesorios
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Taladro Percutor DeWalt 13mm',
        'slug': 'taladro-percutor-dewalt-13mm',
        'stock': 8,
        'stock_min': 1,
        'cost': Decimal('120.00'),
        'price': Decimal('199.99'),
        'brand_id': 3,  # DeWalt
        'category_id': 10,  # Herramientas Manuales, Eléctricas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Smartphone Samsung Galaxy A54 128GB',
        'slug': 'smartphone-samsung-galaxy-a54-128gb',
        'stock': 25,
        'stock_min': 5,
        'cost': Decimal('280.00'),
        'price': Decimal('429.99'),
        'brand_id': 5,  # Samsung
        'category_id': 4,  # Teléfonos móviles
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Smart TV 50" 4K UHD JVC',
        'slug': 'smart-tv-50-4k-uhd-jvc',
        'stock': 6,
        'stock_min': 2,
        'cost': Decimal('310.00'),
        'price': Decimal('489.00'),
        'brand_id': 7,  # Jvc
        'category_id': 9,  # TVs, Televisores y plasmas
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Carpa Camping Iglú 4 Personas',
        'slug': 'carpa-camping-iglu-4-personas',
        'stock': 15,
        'stock_min': 3,
        'cost': Decimal('45.00'),
        'price': Decimal('89.50'),
        'brand_id': 2,  # Caterpillar (o genérica)
        'category_id': 2,  # Camping, Gazebos y Aire libre
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Procesador AMD Ryzen 5 5600X',
        'slug': 'procesador-amd-ryzen-5-5600x',
        'stock': 10,
        'stock_min': 2,
        'cost': Decimal('140.00'),
        'price': Decimal('210.00'),
        'brand_id': 8,  # Amd
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Juego de Ollas de Acero Inoxidable 5 Pzs',
        'slug': 'juego-de-ollas-de-acero-inoxidable-5-pzs',
        'stock': 7,
        'stock_min': 2,
        'cost': Decimal('60.00'),
        'price': Decimal('115.00'),
        'brand_id': 1,  # Generica
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Bicicleta Mountain Bike Rodado 29',
        'slug': 'bicicleta-mountain-bike-rodado-29',
        'stock': 4,
        'stock_min': 1,
        'cost': Decimal('220.00'),
        'price': Decimal('350.00'),
        'brand_id': 1,  # Generica
        'category_id': 7,  # Indumentaria, Bicicletas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Monitor Gamer LG 24" Full HD 144Hz',
        'slug': 'monitor-gamer-lg-24-full-hd-144hz',
        'stock': 9,
        'stock_min': 2,
        'cost': Decimal('130.00'),
        'price': Decimal('199.00'),
        'brand_id': 14,  # Lg
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
    {
        'detail': 'Escritorio para Oficina o PC Moderno',
        'slug': 'escritorio-para-oficina-o-pc-moderno',
        'stock': 5,
        'stock_min': 1,
        'cost': Decimal('75.00'),
        'price': Decimal('130.00'),
        'brand_id': 1,  # Generica
        'category_id': 8,  # Mobiliario y muebles para el hogar
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': '/uploads/not-photo_512.png',
    },
]