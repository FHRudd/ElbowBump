import json

from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    items = []
    order = {'get_cart_total': 0}

    for i in cart:
        productString = str(i)
        productString = productString.split()
        print(productString)
        try:
            product = Product.objects.get(id=productString[0])
            total = (product.price * cart[i]["quantity"])

            order['get_cart_total'] += total

            item = {
                'product': {
                    'id': productString[0],
                    'name': product.name,
                    'price': product.price,
                    'imageURL': product.imageURL,
                },
                'size': productString[1],
                'colour': productString[2],
                'printposition': productString[3],
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)

        except:
            pass
    return {'items': items, 'order': order}


def guestOrder(request, data):
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email=email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return customer, order
