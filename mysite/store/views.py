from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Product, Cart, CartItem, Review, Wishlist, Order
from .forms import UserRegistrationForm, ReviewForm, OrderForm

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

# Other views...

def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
            )
            # Process payment and order here
            return redirect('order_confirmation')
    else:
        form = OrderForm()
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'store/checkout.html', {'form': form, 'cart': cart, 'total': total})


def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
            )
            # Process payment and order here
            return redirect('order_confirmation')
    else:
        form = OrderForm()
    total = sum(item.product.price * item.quantity for item in cart.items.all())
    return render(request, 'store/checkout.html', {'form': form, 'cart': cart, 'total': total})

def product_list(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ReviewForm()
    return render(request, 'store/product_detail.html', {'product': product, 'reviews': reviews, 'form': form})

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id
    return cart

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Product added to cart!'})
    return redirect('cart_detail')

def cart_detail(request):
    cart = get_cart(request)
    cart_items = cart.items.all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'store/cart_detail.html', {'cart': cart, 'cart_items': cart_items, 'total': total})

def update_cart(request, pk):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart_item = get_object_or_404(CartItem, pk=pk)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_detail')

def remove_from_cart(request, pk):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, pk=pk)
        cart_item.delete()
    return redirect('cart_detail')

def checkout(request):
    cart = get_cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            # Process payment and order here
            cart.items.all().delete()  # Clear the cart
            return redirect('order_confirmation')
    else:
        form = OrderForm()
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})

def order_confirmation(request):
    return render(request, 'store/order_confirmation.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            cart = get_cart(request)
            cart.user = user
            cart.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                cart = get_cart(request)
                cart.user = user
                cart.save()
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing')

def wishlist(request):
    if not request.user.is_authenticated:
        return redirect('login')
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})

def add_to_wishlist(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, pk=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Product added to wishlist!'})
    return redirect('wishlist')

def remove_from_wishlist(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    product = get_object_or_404(Product, pk=pk)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.products.remove(product)
    return redirect('wishlist')

def landing(request):
    return render(request, 'store/landing.html')
