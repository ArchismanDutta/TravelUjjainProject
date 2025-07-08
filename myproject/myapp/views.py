from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from .forms import CustomerSignupForm, CustomerLoginForm
from .models import TravelPackage, Car, Cart, Customer, Addon

import razorpay


# -------------------- Home --------------------
def home(request):
    packages = TravelPackage.objects.all()
    return render(request, 'index.html', {
        'packages': packages,
        'user': request.user
    })


# -------------------- Auth --------------------
def signup_view(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomerSignupForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next', 'home')
    if request.method == 'POST':
        form = CustomerLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(request.POST.get('next', 'home'))
    else:
        form = CustomerLoginForm()
    return render(request, 'login.html', {
        'form': form,
        'next': next_url
    })


def logout_view(request):
    logout(request)
    return redirect('home')


# -------------------- Views --------------------
@login_required
def dashboard_view(request):
    return render(request, 'index.html', {'user': request.user})


def packages_view(request):
    packages = TravelPackage.objects.all()
    return render(request, 'packages.html', {'packages': packages})


def cars_view(request):
    cars = Car.objects.all()
    return render(request, 'cars.html', {'cars': cars})


def addons_view(request):
    addons = Addon.objects.all()
    return render(request, 'addons.html', {'addons': addons})


# -------------------- Cart --------------------
@login_required
def add_to_cart(request, item_type, item_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if item_type == 'package':
            package = get_object_or_404(TravelPackage, id=item_id)
            cart.travel_package = package
        elif item_type == 'car':
            car = get_object_or_404(Car, id=item_id)
            cart.car = car
        elif item_type == 'addon':
            addon = get_object_or_404(Addon, id=item_id)
            cart.addons.add(addon)
        cart.save()
        return redirect('cart')

    return redirect('home')


@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})


# -------------------- About Us --------------------
def aboutus_view(request):
    return render(request, 'aboutus.html')


# -------------------- Contact Us --------------------
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Send email to admin (replace with actual email in production)
        send_mail(
            subject=f"[TravelSphere Contact] {subject}",
            message=f"From: {name} <{email}>\n\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
        )

        return render(request, 'index.html', {'message_sent': True})

    return redirect('home')


# -------------------- Checkout with Razorpay --------------------
@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)

    # Calculate total price
    total_price = 10
    if cart.travel_package:
        total_price += cart.travel_package.price
    if cart.car:
        total_price += cart.car.price
    total_price += sum(addon.total_price() for addon in cart.addons.all())

    # Razorpay amount must be in paisa
    amount_paisa = int(total_price * 100)

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({
        "amount": amount_paisa,
        "currency": "INR",
        "payment_capture": 1
    })

    context = {
        'cart': cart,
        'order': order,
        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'amount': total_price
    }

    return render(request, 'checkout.html', context)
