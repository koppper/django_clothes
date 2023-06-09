from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from .forms import CartAddShoesForm
from django.contrib.auth import authenticate, login
from shop.models import Clothes, Order, Category
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Feedback
from django.db.models import Q

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('products')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('products')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        user = authenticate(request, username=username, password=password)
        login(request, user)

        return redirect('products')
    else:
        return render(request, 'register.html')


def clothes(request):
    results = request.GET.get('q')
    category = request.GET.get('category')

    if results:
        clothes = Clothes.objects.filter(Q(title__icontains=results) | Q(description__icontains=results) | Q(price__icontains=results) | Q(region__icontains=results) | Q(phone_number__icontains=results))
    else:
        clothes = Clothes.objects.all()
    if category:
        clothes = clothes.filter(category__id=category)
    categories = Category.objects.all()
    return render(request, 'products.html', {'results': results, 'clothes': clothes, 'categories': categories})


def calculate_total(cart):
    total = 0
    for shoe in cart.shoes.all():
        total += shoe.price
    cart.total = total
    cart.save()


@login_required
def add_to_cart(request, id):
    clothes = get_object_or_404(Clothes, pk=id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart.shoes.add(clothes)
    cart.calculate_total() 
    return redirect('cart')

@login_required
def remove_from_cart(request, id):
    shoe = get_object_or_404(Clothes, pk=id)
    cart = get_object_or_404(Cart, user=request.user)
    cart.shoes.remove(shoe)
    cart.calculate_total() 
    messages.success(request, f"{shoe.title} has been removed from your cart.")
    return redirect('cart')
    

@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        clothes_id = request.POST.get('id')
        if clothes_id:
            shoe = get_object_or_404(Clothes, pk=clothes_id)
            cart.shoes.remove(shoe)
            cart.calculate_total() 
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)


def buy(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        order = Order.objects.create(name=name, email=email, phone=phone, user=request.user, cart=Cart.objects.get(user=request.user))
        print(order)
        return redirect('processed')

    return render(request, "buy.html")


def processed(request):
    return render(request, "processed.html")


def about(request):
    return render(request, "about.html")

def feedback(request, id): 
    clothes = get_object_or_404(Clothes, pk=id)

    if request.method == "POST":
        feed = request.POST.get("feedback")
        feedback = Feedback.objects.create(clothes=clothes, text=feed)
        feedback.save()
        return redirect("thanks")
    return render(request, "feedback.html")

def thanks(request):
    return render(request, 'thanks.html')


def add_clothes(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        phone_number = request.POST.get("phone_number")
        region = request.POST.get("region")
        archived = request.POST.get("archived") == "on"
        category_id = request.POST.get("category")
        new_category = request.POST.get("new_category")  
        
        clothes = Clothes.objects.create(
            title=title,
            description=description,
            price=price,
            image=image,
            phone_number=phone_number,
            region=region,
            archived=archived
        )
        
        if category_id:
            category = Category.objects.get(id=category_id)
            clothes.category = category
        elif new_category:
            category = Category.objects.create(title=new_category)
            clothes.category = category
        
        clothes.save()
        
        return redirect("products")
    
    categories = Category.objects.all()
    
    return render(request, "add_clothes.html", {"categories": categories})

