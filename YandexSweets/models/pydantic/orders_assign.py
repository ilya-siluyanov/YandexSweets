from pydantic.main import BaseModel


class OrdersAssign(BaseModel):
    courier_id: int
