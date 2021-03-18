from pydantic.main import BaseModel


class OrderComplete(BaseModel):
    courier_id: int
    order_id: int
    complete_time: str
