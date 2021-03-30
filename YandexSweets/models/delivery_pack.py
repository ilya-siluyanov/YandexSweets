from django.db.models import Model, fields, ForeignKey, CASCADE

from YandexSweets.models import Courier


class DeliveryPack(Model):
    pack_id = fields.AutoField(primary_key=True)
    courier = ForeignKey(Courier, on_delete=CASCADE, default=None, blank=True, null=True)
    assign_time = fields.DateTimeField()
    delivery_type = fields.CharField(max_length=4, choices=Courier.COURIER_TYPE_CHOICES, default='foot')
    delivery_ended = fields.BooleanField(default=False)
    last_complete_time = fields.DateTimeField()

    def orders(self):
        return self.order_set.all()

    def assign_order(self, order):
        order.delivery_pack = self
        order.save()

    def make_order_free(self, order):
        if order not in self.orders():
            return
        order.delivery_pack = None
        order.delivery_time = None
        order.save()
