from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.CharField(max_length=1000, default="No description found")
    image = models.ImageField(null=True, blank=True)
    CarouselImage1 = models.ImageField(null=True, blank=True)
    CarouselImage2 = models.ImageField(null=True, blank=True)
    CarouselImage3 = models.ImageField(null=True, blank=True)
    CarouselImage4 = models.ImageField(null=True, blank=True)
    SmallImage1 = models.ImageField(null=True, blank=True)
    SmallImage2 = models.ImageField(null=True, blank=True)
    SmallImage3 = models.ImageField(null=True, blank=True)
    SmallImage4 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def CI1URL(self):
        try:
            url = self.CarouselImage1.url
        except:
            url = ''
        return url

    @property
    def CI2URL(self):
        try:
            url = self.CarouselImage2.url
        except:
            url = ''
        return url

    @property
    def CI3URL(self):
        try:
            url = self.CarouselImage3.url
        except:
            url = ''
        return url

    @property
    def CI4URL(self):
        try:
            url = self.CarouselImage4.url
        except:
            url = ''
        return url

    @property
    def SI1URL(self):
        try:
            url = self.SmallImage1.url
        except:
            url = ''
        return url

    @property
    def SI2URL(self):
        try:
            url = self.SmallImage2.url
        except:
            url = ''
        return url

    @property
    def SI3URL(self):
        try:
            url = self.SmallImage3.url
        except:
            url = ''
        return url

    @property
    def SI4URL(self):
        try:
            url = self.SmallImage4.url
        except:
            url = ''
        return url


class VariationManager(models.Manager):
    def all(self):
        return super(VariationManager, self).filter(stock=True)

    def sizes(self):
        return self.all().filter(category='size')

    def colour(self):
        return self.all().filter(category='colour')

    def printposition(self):
        return self.all().filter(category='printposition')


VAR_CATEGORIES = (
    ('size', 'size'),
    ('colour', 'colour'),
    ('printposition', 'printposition')
)


class Variation(models.Model):
    name = models.CharField(max_length=100, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=120, choices=VAR_CATEGORIES, default='colour')
    stock = models.BooleanField(default=True)

    objects = VariationManager()

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def needsShipping(self):
        if self.get_cart_items > 0:
            return True
        else:
            return False

    @property
    def get_shipping(self):
        ordertotal = self.get_cart_total
        if ordertotal > 35:
            shipping = 0
        else:
            shipping = 0.5 * self.get_cart_items
        return shipping

    @property
    def get_order_total(self):
        return self.get_cart_total + self.get_shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=50, null=False, default='Not Chosen')
    colour = models.CharField(max_length=50, null=False, default='Not Chosen')
    printposition = models.CharField(max_length=50, null=False, default='Not Chosen')
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=50, null=False)
    county = models.CharField(max_length=100, null=False)
    postcode = models.CharField(max_length=15, null=False)
    country = models.CharField(max_length=100, null=False, default='United Kingdom')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.customer)


class GalleryImages(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    live = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


class ContactUs(models.Model):
    email = models.CharField(max_length=200)
    message = models.CharField(max_length=1000)

    def __str__(self):
        return self.email
