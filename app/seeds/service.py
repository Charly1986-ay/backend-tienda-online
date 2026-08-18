from contextlib import asynccontextmanager
from pwdlib import PasswordHash
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.api.v1.brands.models import Brand
from app.core.db import engine, init_db
from app.api.v1.users.models import User
from app.api.v1.categories.models import Category
from app.api.v1.articles.models import Article

from app.seeds.data.users import USERS
from app.seeds.data.brands import BRANDS
from app.seeds.data.categories import CATEGORIES
from app.seeds.data.articles import ARTICLES

@asynccontextmanager
async def atomic(db: AsyncSession):
    try:
        yield
        await db.commit()
    except Exception:
        await db.rollback()
        raise


def get_hex(name: str) -> str:
    return hex(id(name))


def hash_password(plain: str) -> str:
    return PasswordHash.recommended().hash(plain)


async def _user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.exec(select(User).where(User.email == email))
    return result.first()


async def _category_by_id(db: AsyncSession, category_id: int) -> Category | None:
    return await db.get(Category, category_id)


async def _brand_by_id(db: AsyncSession, brand_id: int) -> Brand | None:
    return await db.get(Brand, brand_id)


async def _category_by_slug(db: AsyncSession, slug: str) -> Category | None:
    result = await db.exec(select(Category).where(Category.slug == slug))        
    return result.first()


async def _brand_by_slug(db: AsyncSession, slug: str) -> Brand | None:
    result = await db.exec(select(Brand).where(Brand.slug == slug))        
    return result.first()


async def seed_users(db: AsyncSession) -> None:
    async with atomic(db):
        for data in USERS:
            obj = await _user_by_email(db, data['email'])
            if obj:
                changed = False
                if obj.full_name != data.get('full_name'):
                    obj.full_name = data.get('full_name')
                    changed = True
                if data.get('password'):
                    obj.hashed_password = hash_password(data['password'])
                    changed = True
                if data.get('role'):
                    obj.role = data.get('role')
                    changed = True
                if changed:
                    db.add(obj)
            else:
                db.add(User(
                    email=data['email'],
                    full_name=data.get('full_name'),
                    role=data.get('role'),
                    hashed_password=hash_password(data['password'])
                ))


async def seed_categories(db: AsyncSession) -> None:
    async with atomic(db):
        for data in CATEGORIES:
            # Corregido: se agregó 'await' porque es una función async
            obj = await _category_by_slug(db=db, slug=data['slug'])
            if obj:                
                if obj.name != data.get('name'):
                    obj.name = data.get('name') 
                    db.add(obj)  
            else:
                db.add(Category(
                    name=data.get('name'),
                    slug=data['slug']
                ))   


async def seed_brands(db: AsyncSession) -> None:
    async with atomic(db):
        for data in BRANDS:
            # Corregido: se agregó 'await' porque es una función async
            obj = await _brand_by_slug(db=db, slug=data['slug'])
            if obj:                
                if obj.name != data.get('name'):
                    obj.name = data.get('name') 
                    db.add(obj)  
            else:
                db.add(Brand(
                    name=data.get('name'),
                    slug=data['slug']
                ))


async def seed_articles(db: AsyncSession) -> None:
    async with atomic(db):
        for data in ARTICLES:
            category_id = data.get('category_id')
            brand_id = data.get('brand_id')

            if not category_id or not brand_id:
                continue

            # Corregido: se agregó 'await' y se pasó 'db' como primer parámetro
            category = await _category_by_id(db=db, category_id=category_id)
            brand = await _brand_by_id(db=db, brand_id=brand_id)

            if category and brand:                    
                db.add(Article(
                    detail=data.get('detail'),
                    slug=data.get('slug'),  # <--- Añadido el slug del artículo que creamos antes
                    stock=data.get('stock'),
                    stock_min=data.get('stock_min'),
                    cost=data.get('cost'),
                    price=data.get('price'),
                    brand_id=brand_id,
                    category_id=category_id,
                    units_type=data.get('units_type'),
                    status=data.get('status'),
                    image_url=data.get('image_url')
                ))
            

async def run_all() -> None:
    await init_db()  
    async with AsyncSession(engine) as db:
        await seed_users(db)
        await seed_brands(db)
        await seed_categories(db)
        await seed_articles(db)        

async def run_users() -> None:
    async with AsyncSession(engine) as db:
        await seed_users(db)

async def run_brands() -> None:
    async with AsyncSession(engine) as db:
        await seed_brands(db)

async def run_categories() -> None:
    async with AsyncSession(engine) as db:
        await seed_categories(db)

async def run_articles() -> None:
    async with AsyncSession(engine) as db:
        await seed_articles(db)