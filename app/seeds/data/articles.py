from decimal import Decimal

from app.models.articles import UnitsType, StatusArticle

ARTICLES = [
    {
        'title': 'Notebook Lenovo Ideapad 15.6"',
        'slug': 'notebook-lenovo-ideapad-156',
        'stock': 12,        
        'cost': Decimal('450.00'),
        'price': Decimal('699.99'),
        'brand_id': 11,  # Lenovo
        'category_id': 3,  # PCs, Tablets, Notebooks y Accesorios
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Taladro Percutor DeWalt 13mm',
        'slug': 'taladro-percutor-dewalt-13mm',
        'stock': 8,        
        'cost': Decimal('120.00'),
        'price': Decimal('199.99'),
        'brand_id': 3,  # DeWalt
        'category_id': 10,  # Herramientas Manuales, Eléctricas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Smartphone Samsung Galaxy A54 128GB',
        'slug': 'smartphone-samsung-galaxy-a54-128gb',
        'stock': 25,        
        'cost': Decimal('280.00'),
        'price': Decimal('429.99'),
        'brand_id': 5,  # Samsung
        'category_id': 4,  # Teléfonos móviles
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Smart TV 50" 4K UHD JVC',
        'slug': 'smart-tv-50-4k-uhd-jvc',
        'stock': 6,        
        'cost': Decimal('310.00'),
        'price': Decimal('489.00'),
        'brand_id': 7,  # Jvc
        'category_id': 9,  # TVs, Televisores y plasmas
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Carpa Camping Iglú 4 Personas',
        'slug': 'carpa-camping-iglu-4-personas',
        'stock': 15,        
        'cost': Decimal('45.00'),
        'price': Decimal('89.50'),
        'brand_id': 2,  # Caterpillar
        'category_id': 2,  # Camping, Gazebos y Aire libre
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Procesador AMD Ryzen 5 5600X',
        'slug': 'procesador-amd-ryzen-5-5600x',
        'stock': 10,        
        'cost': Decimal('140.00'),
        'price': Decimal('210.00'),
        'brand_id': 8,  # Amd
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Juego de Ollas de Acero Inoxidable 5 Pzs',
        'slug': 'juego-de-ollas-de-acero-inoxidable-5-pzs',
        'stock': 7,        
        'cost': Decimal('60.00'),
        'price': Decimal('115.00'),
        'brand_id': 1,  # Generica
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Bicicleta Mountain Bike Rodado 29',
        'slug': 'bicicleta-mountain-bike-rodado-29',
        'stock': 4,        
        'cost': Decimal('220.00'),
        'price': Decimal('350.00'),
        'brand_id': 1,  # Generica
        'category_id': 7,  # Indumentaria, Bicicletas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Monitor Gamer LG 24" Full HD 144Hz',
        'slug': 'monitor-gamer-lg-24-full-hd-144hz',
        'stock': 9,        
        'cost': Decimal('130.00'),
        'price': Decimal('199.00'),
        'brand_id': 14,  # Lg
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Escritorio para Oficina o PC Moderno',
        'slug': 'escritorio-para-oficina-o-pc-moderno',
        'stock': 5,        
        'cost': Decimal('75.00'),
        'price': Decimal('130.00'),
        'brand_id': 1,  # Generica
        'category_id': 8,  # Mobiliario y muebles para el hogar
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },

    # --- 25 Nuevos Artículos añadidos ---
    {
        'title': 'Alfombra de Baño Antideslizante',
        'slug': 'alfombra-de-bano-antideslizante',
        'stock': 15,
        'cost': Decimal('8.00'),
        'price': Decimal('18.50'),
        'brand_id': 1,  # Generica
        'category_id': 6,  # Artículos de baño y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Set de Toallas y Toallones 4 Pzs',
        'slug': 'set-de-toallas-y-toallones-4-pzs',
        'stock': 0,  # <-- STOCK 0 para probar el Job
        'cost': Decimal('15.00'),
        'price': Decimal('32.00'),
        'brand_id': 1,  # Generica
        'category_id': 6,  # Artículos de baño y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Microondas Panasonic 20L',
        'slug': 'microondas-panasonic-20l',
        'stock': 5,
        'cost': Decimal('95.00'),
        'price': Decimal('159.99'),
        'brand_id': 10,  # Panasonic
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Smart TV 55" 4K Samsung',
        'slug': 'smart-tv-55-4k-samsung',
        'stock': 3,
        'cost': Decimal('420.00'),
        'price': Decimal('649.00'),
        'brand_id': 5,  # Samsung
        'category_id': 9,  # TVs, Televisores y plasmas
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Notebook HP Pavilion 14"',
        'slug': 'notebook-hp-pavilion-14',
        'stock': 0,  # <-- STOCK 0 para probar el Job
        'cost': Decimal('520.00'),
        'price': Decimal('799.00'),
        'brand_id': 12,  # Hewlett Packard
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Tablet Acer Iconia 10"',
        'slug': 'tablet-acer-iconia-10',
        'stock': 14,
        'cost': Decimal('110.00'),
        'price': Decimal('179.99'),
        'brand_id': 13,  # Acer
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Plancha a Vapor Panasonic',
        'slug': 'plancha-a-vapor-panasonic',
        'stock': 20,
        'cost': Decimal('22.00'),
        'price': Decimal('45.00'),
        'brand_id': 10,  # Panasonic
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Aspiradora Robot LG',
        'slug': 'aspiradora-robot-lg',
        'stock': 6,
        'cost': Decimal('180.00'),
        'price': Decimal('299.99'),
        'brand_id': 14,  # LG
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Placa de Video Gigabyte RTX 3060',
        'slug': 'placa-de-video-gigabyte-rtx-3060',
        'stock': 0,  # <-- STOCK 0 para probar el Job
        'cost': Decimal('250.00'),
        'price': Decimal('380.00'),
        'brand_id': 15,  # Gigabyte
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Procesador Intel Core i7 12700K',
        'slug': 'procesador-intel-core-i7-12700k',
        'stock': 11,
        'cost': Decimal('230.00'),
        'price': Decimal('340.00'),
        'brand_id': 9,  # Intel
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Radio Portátil Noblex AM/FM',
        'slug': 'radio-portatil-noblex-am-fm',
        'stock': 18,
        'cost': Decimal('15.00'),
        'price': Decimal('29.99'),
        'brand_id': 4,  # Noblex
        'category_id': 9,  # TVs, Televisores y plasmas
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Barra de Sonido LG con Subwoofer',
        'slug': 'barra-de-sonido-lg-con-subwoofer',
        'stock': 7,
        'cost': Decimal('140.00'),
        'price': Decimal('229.00'),
        'brand_id': 14,  # LG
        'category_id': 9,  # TVs, Televisores y plasmas
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Linterna LED Recargable Caterpillar',
        'slug': 'linterna-led-recargable-caterpillar',
        'stock': 25,
        'cost': Decimal('12.00'),
        'price': Decimal('25.00'),
        'brand_id': 2,  # Caterpillar
        'category_id': 2,  # Camping, Gazebos y Aire libre
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Mochila Táctica Caterpillar 30L',
        'slug': 'mochila-tactica-caterpillar-30l',
        'stock': 12,
        'cost': Decimal('35.00'),
        'price': Decimal('65.00'),
        'brand_id': 2,  # Caterpillar
        'category_id': 7,  # Indumentaria, Bicicletas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Soldadora Inverter DeWalt 200A',
        'slug': 'soldadora-inverter-dewalt-200a',
        'stock': 4,
        'cost': Decimal('180.00'),
        'price': Decimal('289.00'),
        'brand_id': 3,  # DeWalt
        'category_id': 10,  # Herramientas Manuales...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Amoladora Angular DeWalt 4-1/2"',
        'slug': 'amoladora-angular-dewalt-4-12',
        'stock': 0,  # <-- STOCK 0 para probar el Job
        'cost': Decimal('65.00'),
        'price': Decimal('109.99'),
        'brand_id': 3,  # DeWalt
        'category_id': 10,  # Herramientas Manuales...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Colchón 2 Plazas Alta Densidad',
        'slug': 'colchon-2-plazas-alta-densidad',
        'stock': 3,
        'cost': Decimal('150.00'),
        'price': Decimal('250.00'),
        'brand_id': 1,  # Generica
        'category_id': 8,  # Mobiliario y muebles para el hogar
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Silla de Escritorio Ergonomica',
        'slug': 'silla-de-escritorio-ergonomica',
        'stock': 8,
        'cost': Decimal('70.00'),
        'price': Decimal('125.00'),
        'brand_id': 1,  # Generica
        'category_id': 8,  # Mobiliario y muebles para el hogar
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Cafetera de Filtro Panasonic',
        'slug': 'cafetera-de-filtro-panasonic',
        'stock': 10,
        'cost': Decimal('30.00'),
        'price': Decimal('59.99'),
        'brand_id': 10,  # Panasonic
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Parlante Bluetooth Noblex Resistente al Agua',
        'slug': 'parlante-bluetooth-noblex-resistente-al-agua',
        'stock': 14,
        'cost': Decimal('25.00'),
        'price': Decimal('49.99'),
        'brand_id': 4,  # Noblex
        'category_id': 9,  # TVs, Televisores y plasmas
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Auriculares Gamer Lenovo Legion',
        'slug': 'auriculares-gamer-lenovo-legion',
        'stock': 0,  # <-- STOCK 0 para probar el Job
        'cost': Decimal('40.00'),
        'price': Decimal('79.99'),
        'brand_id': 11,  # Lenovo
        'category_id': 3,  # PCs, Tablets...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Remera Deportiva Secado Rápido',
        'slug': 'remera-deportiva-secado-rapido',
        'stock': 30,
        'cost': Decimal('8.00'),
        'price': Decimal('19.99'),
        'brand_id': 1,  # Generica
        'category_id': 7,  # Indumentaria, Bicicletas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Pelota de Fútbol Profesional',
        'slug': 'pelota-de-futbol-profesional',
        'stock': 22,
        'cost': Decimal('18.00'),
        'price': Decimal('39.99'),
        'brand_id': 1,  # Generica
        'category_id': 7,  # Indumentaria, Bicicletas...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Estufa Halógena de Pie Noblex',
        'slug': 'estufa-halogenana-de-pie-noblex',
        'stock': 5,
        'cost': Decimal('20.00'),
        'price': Decimal('42.50'),
        'brand_id': 4,  # Noblex
        'category_id': 5,  # Artículos de cocinas y deco
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
    {
        'title': 'Kit de Destornilladores de Precisión',
        'slug': 'kit-de-destornilladores-de-precision',
        'stock': 15,
        'cost': Decimal('9.00'),
        'price': Decimal('21.00'),
        'brand_id': 2,  # Caterpillar
        'category_id': 10,  # Herramientas Manuales...
        'units_type': UnitsType.UNITS.value,
        'status': StatusArticle.AVAILABLE.value,
        'image_url': 'not-photo_512.png',
    },
]