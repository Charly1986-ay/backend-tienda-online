from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.invoice import Invoice
from .repository import InvoiceRepository

from app.core.exceptions import InvoiceNotFound
from app.core.pagination import get_pagination
from .enums import InvoiceStatus


class InvoiceQueryService:
    def __init__(self, db: AsyncSession):
        self.invoice_repo = InvoiceRepository(db=db)

    async def get_all_pagination(
        self,
        page_size: int,
        page: int,
        status: InvoiceStatus | None = None,
        client_id: int | None = None,
        full_name: str | None = None,
        sort_by: str = 'id',
        sort_order: str = 'asc'
    ) -> dict:

        counter = await self.invoice_repo.count_all(
            status=status,
            client_id=client_id,
            full_name=full_name
        )

        pagination = get_pagination(
            counter=counter,
            page=page,
            page_size=page_size
        )

        rows = await self.invoice_repo.get_all_pagination(
            page_size=pagination['page_size'],
            offset=pagination['offset'],
            status=status,
            client_id=client_id,
            full_name=full_name,
            sort_by=sort_by,
            sort_order=sort_order
        )

        invoice_list = []

        for invoice, user in rows:
            invoice_dict = invoice.model_dump()
            invoice_dict['fullname'] = user.full_name
            invoice_list.append(invoice_dict)

        return {
            'counter': counter,
            'pages': pagination['pages'],
            'offset': pagination['offset'],
            'page': pagination['page'],
            'page_size': pagination['page_size'],
            'invoices': invoice_list
        }

    async def get_invoice(self, invoice_id: int) -> Invoice:
        invoice = await self.invoice_repo.get(invoice_id=invoice_id)

        if not invoice:
            raise InvoiceNotFound()
        return invoice