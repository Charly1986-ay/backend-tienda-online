from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.categories.schemas import CategoryCreate
from app.enums.movements import MovementType, TargetType
from app.models.articles import Article
from app.models.categories import Category
from app.models.movements import GenericActivityLog
from app.repositories.article import ArticleRepository
from app.repositories.categories import CategoryRepository
from app.core.exceptions import CategoryNotFound, CategoryExistsException
from app.repositories.movements import ActivityRepository


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.category_repo = CategoryRepository(db=db)
        self.article_repo = ArticleRepository(db=db)
        self.activity_repo = ActivityRepository(db=db)


    async def insert_category(
        self, 
        data: CategoryCreate,             
        user_id: int
    ) -> Category:
        category_db = await self.category_repo.get_category_by_name(
            name=data.name
        )
    
        if category_db:
            raise CategoryExistsException()   

        new_category = Category(
            name=data.name,
            slug=data.slug()
        )              
    
        try:
            category_response = await self.category_repo.create(
                data=new_category                        
            )
    
            log = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.CATEGORY.value,
                target_id=str(category_response.id),
                movement_type=MovementType.CREATED.value,
                details=(
                    f'Se creo la categoría {category_response.name}'                    
                )
            )
            await self.activity_repo.create_movement(log=log)
    
            await self.db.commit()
            await self.db.refresh(category_response)
    
            return category_response
        except Exception as e:
            await self.db.rollback()
            raise e


    async def update_category(
        self, 
        data: CategoryCreate, 
        category_id: int, 
        user_id: int
    ) -> Category:
        category_db = await self.category_repo.get(category_id=category_id)
        
        if not category_db:
            raise CategoryNotFound()

        # Si el nombre cambió, validamos que no pertenezca a OTRO registro
        if data.name != category_db.name:
            existing_name = await self.category_repo.get_category_by_name(
                name=data.name
            )
            if existing_name and existing_name.id != category_id:
                raise CategoryExistsException()        

        category_prev = category_db.name

        updates = data.model_dump(exclude_unset=True)         

        try:
            category_response = await self.category_repo.update(
                data=category_db,  
                updates=updates         
            )

            log = GenericActivityLog(
                user_id=user_id,
                target_type=TargetType.CATEGORY.value,
                target_id=str(category_response.id),
                movement_type=MovementType.CATEGORY_CHANGE.value,
                details=(
                    f'Se modificó la categoría de ' 
                    f'{category_prev} a {category_response.name}'                    
                )
            )
            await self.activity_repo.create_movement(log=log)

            await self.db.commit()
            await self.db.refresh(category_response)

            return category_response
        except Exception as e:
            await self.db.rollback()
            raise e


    async def get_articles_by_category(self, category_id: int) -> list[Article]:
        category_db = await self.category_repo.get(
            category_id=category_id
        )
        if not category_db:
            raise CategoryNotFound()
        return await self.article_repo.get_by_category(
            category_id=category_id
        )