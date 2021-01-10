var updateBtns = document.getElementsByClassName('update-cart')
var removeBtns = document.getElementsByClassName('remove-cart')


for (i=0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    var sizeDD = document.getElementById('productsSizeDD')
    var size = sizeDD.value
    var colourDD = document.getElementById('productsColourDD')
    var colour = colourDD.value
    var PrintPositionDD = document.getElementById('productsPrintPositionDD')
    var PrintPosition = PrintPositionDD.value
    var quantityForm = document.getElementById('productQuantity')
    var quantity = quantityForm.value

    if (user == 'AnonymousUser'){
        console.log('User is not authenticated')
        addCookieItem(productId, action, size, colour, PrintPosition, quantity)
    }
    else{
    updateUserOrder(productId, action, size, colour, PrintPosition, quantity)
    }
    console.log(size,colour,PrintPosition,quantity)
    })
}

function addCookieItem(productId, action, size, colour, PrintPosition, quantity){
    console.log('User is not logged in')
    quantityInt = Number(quantity)

    if(action == 'add'){
        if(cart[productId + " " + size + " " + colour + " " + PrintPosition] == undefined){
            cart[productId + " " + size + " " + colour + " " + PrintPosition] = {'quantity': quantityInt}
            console.log(cart)
        }
        else{
            cart[productId + " " + size + " " + colour + " " + PrintPosition]['quantity'] += quantityInt
            console.log(cart)
        }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}

function updateUserOrder(productId, action, size, colour, PrintPosition, quantity){
    console.log('User is authenticated')

    var url = '/update_item/'

    fetch(url, {
    method:'POST',
    headers:{
        'Content-Type' : 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body:JSON.stringify({'productId': productId, 'action': action, 'size': size, 'colour': colour, 'PrintPosition': PrintPosition, 'quantity': quantity})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}

for (i=0; i < removeBtns.length; i++) {
    removeBtns[i].addEventListener('click',function(){
    var productId = this.dataset.product
    var action = this.dataset.action
    var size = this.dataset.itemsize
    var colour = this.dataset.itemcolour
    var PrintPosition = this.dataset.itemprint

    if (user == 'AnonymousUser'){
    console.log('User is not authenticated')
    console.log(productId, action, size, colour, PrintPosition)
    removeCookieItem(productId, action, size, colour, PrintPosition)
    }
    else{
    removeUserOrder(productId, action, size, colour, PrintPosition)
    }
    console.log(productId,action,size)
    })
}

function removeCookieItem(productId, action, size, colour, PrintPosition){
    console.log('User is not logged in')

    if(action == 'remove'){
            console.log(cart[productId + size + colour + PrintPosition])
            cart[productId + " " + size + " " + colour + " " + PrintPosition]['quantity'] -= 1

            if(cart[productId + " " + size + " " + colour + " " + PrintPosition]['quantity'] <=0){
                console.log('Remove Item')
                delete cart[productId + " " + size + " " + colour + " " + PrintPosition];
            }
    }
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function removeUserOrder(productId, action, size, colour, PrintPosition){

    var url = '/remove_item/'
    console.log(JSON.stringify({'productId': productId, 'action': action, 'size': size, 'colour': colour, 'PrintPosition': PrintPosition}))

    fetch(url, {
    method:'POST',
    headers:{
        'Content-Type' : 'application/json',
        'X-CSRFToken': csrftoken,
    },
    body:JSON.stringify({'productId': productId, 'action': action, 'size': size, 'colour': colour, 'PrintPosition': PrintPosition})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}