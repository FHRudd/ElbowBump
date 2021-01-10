from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import cookieCart


# Create your views here.


def index(request):
    context = {}
    return render(request, 'store/index.html', context)


def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/shop.html', context)


def gallery(request):
    images = GalleryImages.objects.filter(live=True)
    context = {'images': images}
    return render(request, 'store/gallery.html', context)


def team(request):
    context = {}
    return render(request, 'store/team.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'get_shipping': 0, 'get_order_total': 0}

        for i in cart:
            productString = str(i)
            productString = productString.split()
            print(productString)
            try:
                product = Product.objects.get(id=productString[0])
                total = (product.price * cart[i]["quantity"])

                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

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

        if order['get_cart_total'] > 35:
            order['get_shipping'] = 0
        else:
            order['get_shipping'] = order['get_cart_items'] * 0.5

        order['get_order_total'] = order['get_cart_total'] + order['get_shipping']

    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


def productView(request, name):
    product = Product.objects.filter(name=name)
    print(product)
    return render(request, 'store/product.html', {'product': product[0]})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    size = data['size']
    colour = data['colour']
    printposition = data['PrintPosition']
    quantity = data['quantity']

    print('Action:', action)
    print('ProductID:', productId)
    print('Size:', size)
    print('Colour:', colour)
    print('Print:', printposition)
    print('Quantity:', quantity)

    quantityInt = int(quantity)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product, size=size, colour=colour,
                                                         printposition=printposition)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + quantityInt)
        orderItem.size = size
        orderItem.colour = colour
        orderItem.printposition = printposition
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was updated', safe=False)


def removeItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    size = data['size']
    colour = data['colour']
    printposition = data['PrintPosition']

    print('Action:', action)
    print('ProductID:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem = OrderItem.objects.get(order=order, product=product, size=size, colour=colour,
                                      printposition=printposition)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was Removed', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        print("user is not logged in")
        print('Cookies:', request.COOKIES)
        name = data['form']['firstName'] + " " + data['form']['lastName']
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

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.needsShipping:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            county=data['shipping']['county'],
            postcode=data['shipping']['postcode'],
            country=data['shipping']['country'],
        )

    return JsonResponse('Payment Complete', safe=False)
