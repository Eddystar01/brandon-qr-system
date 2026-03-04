import qrcode
from io import BytesIO
from django.core.files import File
from django.db import models


class Table(models.Model):
    number = models.IntegerField(unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    def save(self, *args, **kwargs):

        if not self.qr_code:
            url = f"https://qr.brandonhotelandapartments.com/table/{self.number}/"

            qr = qrcode.make(url)

            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)
            filename = f"table_{self.number}.png"

            self.qr_code.save(filename, File(buffer), save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Table {self.number}"


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='menu/')
    available = models.BooleanField(default=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = [
        ('pending_payment', 'Pending Payment'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('served', 'Served'),
        ('cancelled', 'Cancelled'),
    ]

    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='pending_payment')
    payment_proof = models.ImageField(upload_to='payments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_confirmed = models.BooleanField(default=False)
    kitchen_message = models.TextField(blank=True, null=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)