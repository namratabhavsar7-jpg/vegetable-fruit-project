from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Category, Product, CartItem, WishlistItem
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# ----------------------- Helper: get categories -----------------------
def get_categories():
    return Category.objects.all()

# ----------------------- Register ---------------------------
def user_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        # Email as username
        user = User.objects.create_user(username=email, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        user.save()
        messages.success(request, 'Registration successful!')
        return redirect('login')

    return render(request, 'register.html', {'categories': get_categories()})

# ----------------------- Login ---------------------------
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'login.html', {'categories': get_categories()})

# ---------------------- Logout -----------------------------
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

# ---------------------- Dashboard/Home -----------------------------
@login_required
def dashboard(request):
    return redirect('home')

def home(request):
    categories = get_categories()
    products = Product.objects.all()
    return render(request, 'home.html', {
        'categories': categories,
        'products': products
    })

# ---------------------- Category Products -----------------------------
def category_products(request, category_id):
    categories = get_categories()
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'product.html', {
        'categories': categories,
        'category': category,
        'products': products
    })

# ---------------------- Product Detail -----------------------------
def product_detail(request, product_id):
    categories = get_categories()
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {
        'categories': categories,
        'product': product
    })

# ---------------------- Add to Cart -----------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return redirect('cart')

# ---------------------- Add to Wishlist -----------------------------
@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishlistItem.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

# ---------------------- Cart Page -----------------------------
@login_required
def cart_view(request):
    categories = get_categories()
    cart_items = CartItem.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    return render(request, 'cart.html', {
        'categories': categories,
        'cart_items': cart_items,
        'total': total
    })

# ---------------------- Wishlist Page -----------------------------
@login_required
def wishlist_view(request):
    categories = get_categories()
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {
        'categories': categories,
        'wishlist_items': wishlist_items
    })

# ---------------------- Checkout Page -----------------------------
@login_required
def checkout_view(request):
    categories = get_categories()
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'checkout.html', {
        'categories': categories,
        'cart_items': cart_items,
        'total': total
    })

# ---------------------- Remove from Cart -----------------------------
@login_required
def remove_from_cart(request, product_id):
    CartItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')

# ---------------------- Remove from Wishlist -----------------------------
@login_required
def remove_from_wishlist(request, product_id):
    WishlistItem.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('wishlist')

# ---------------------- Search -----------------------------
def search(request):
    categories = get_categories()
    query = request.GET.get('q', '')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, "search.html", {
        "categories": categories,
        "query": query,
        "results": results
    })
