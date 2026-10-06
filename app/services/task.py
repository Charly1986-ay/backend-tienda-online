from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.admin.articles.schemas import UpdateStatus
from app.enums.articles import StatusArticle
from app.repositories.article import ArticleRepository

async def check_out(db: AsyncSession) -> None:
    article_repo = ArticleRepository(db=db)   
    try:
        articles = await article_repo.get_zero_stock_items()

        if articles:   
            for article in articles:
                previous_state = article.status

                article_status = UpdateStatus(
                    status=StatusArticle.UNAVAILABLE.value
                )
                            
                update_dict = article_status.model_dump(
                    exclude_unset=True
                )   
                
                article_update = await article_repo.update(
                    article=article, 
                    updates=update_dict
                )  

                mensaje = (
                    f"Se modifico el estado del artículo NRO: {article_update.id} "
                    f"de {previous_state} a {article_update.status}"
                )
                print(mensaje)
            
            await db.commit()

        print("*** Auditoría finalizada! ***")
    except Exception as e:
        print(f"Error en el job OUT: {e}")
        await db.rollback()