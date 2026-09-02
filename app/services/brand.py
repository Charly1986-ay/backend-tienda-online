from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.brands.schemas import BrandCreate
from app.enums.movements import MovementType, TargetType
from app.models.articles import Article
from app.models.brands import Brand
from app.models.movements import GenericActivityLog
from app.repositories.article import ArticleRepository
from app.repositories.brands import BrandRepository
from app.core.exceptions import BrandExistsException, BrandNotFound
from app.repositories.movements import ActivityRepository


class BrandService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.brand_repo = BrandRepository(db=db)
        self.article_repo = ArticleRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)


    async def insert_brand(
        self, 
        data: BrandCreate,             
        user_id: int
    ) -> Brand:
        brand_db = await self.brand_repo.get_brand_by_name(
            name=data.name
        )
        
        if brand_db:
            raise BrandExistsException()   
    
        new_brand = Brand(
            name=data.name,
            slug=data.slug()
        )              
        
        try:
            brand_response = await self.brand_repo.create(
                data=new_brand                        
            )
        
            log = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.BRAND.value,
                target_id=str(brand_response.id),
                movement_type=MovementType.CREATED.value,
                details=(
                    f'Se creo la marca {brand_response.name}'                    
                )
            )
            await self.activity_repo.create_movement(log=log)
        
            await self.db.commit()
            await self.db.refresh(brand_response)
        
            return brand_response
        except Exception as e:
            await self.db.rollback()
            raise e


    async def update_brand(
        self, 
        data: BrandCreate, 
        brand_id: int, 
        user_id: int
    ) -> Brand:
        brand_db = await self.brand_repo.get(brand_id=brand_id)
            
        if not brand_db:
            raise BrandNotFound()
    
        # Si el nombre cambió, validamos que no pertenezca a OTRO registro
        if data.name != brand_db.name:
            existing_name = await self.brand_repo.get_brand_by_name(
                name=data.name
            )
            if existing_name and existing_name.id != brand_id:
                raise BrandExistsException()        
    
        brand_prev = brand_db.name
    
        updates = data.model_dump(exclude_unset=True)         
    
        try:
            brand_response = await self.brand_repo.update(
                data=brand_db,  
                updates=updates         
            )
    
            log = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.BRAND.value,
                target_id=str(brand_response.id),
                movement_type=MovementType.BRAND_CHANGE.value,
                details=(
                    f'Se modificó la marca de ' 
                    f'{brand_prev} a {brand_response.name}'                    
                )
            )
            await self.activity_repo.create_movement(log=log)
    
            await self.db.commit()
            await self.db.refresh(brand_response)
    
            return brand_response
        except Exception as e:
            await self.db.rollback()
            raise e
        

    async def get_articles_by_brand(self, brand_id: int) -> list[Article]:
        brand_db = await self.brand_repo.get(brand_id=brand_id)
        if not brand_db:
            raise BrandNotFound()
        return await self.article_repo.get_by_brand(
            brand_id=brand_id
        )