from .db import AsyncSessionLocal  
from app.services import task

async def check_out_job():    
    async with AsyncSessionLocal() as db:
        print('[JOB-CHECK OUT] comienza la rutina PROGRAMADA...!!!')        
        
        await task.check_out(db=db)
        
        print('Ha finalizado la rutina...!!!')