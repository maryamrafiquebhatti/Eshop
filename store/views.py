from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Category, Cart, CartItem, Order
from .forms import SignUpForm, LoginForm, CheckoutForm

def index(request):
    categories = Category.get_all_categories()
        
    category_id = request.GET.get('category')

    if category_id:
        products = Product.get_all_products_by_categoryid(category_id)
    else:
        products = Product.get_all_products()

    data = {
        'products': products,
        'categories': categories
    }

    return render(request, 'store/index.html', data)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'store/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                request.session['customer_id'] = user.id
                request.session['email'] = user.email
                return redirect('index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create
    Q(cart=cart product=product)
    if not created:
        cart_item.quantity += 1 
        cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'message': 'Product added to cart successfully!'})

    return redirect('cart')

@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'store/cart.html', {'cart_items': cart_items})

def all_products(request):
    products = Product.objects.all()
    return render(request, 'store/all_products.html', {'products': products})

@login_required
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order(
                user=request.user,
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number'],
            )
            order.save()
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('index')
    else:
        form = CheckoutForm()
    return render(request, 'store/checkout.html', {'form': form}) 
