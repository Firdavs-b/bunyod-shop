from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Category, Product, Order

def home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    category_name = None
    if selected_category:
        products = Product.objects.filter(category_id=selected_category)
        try:
            category_name = Category.objects.get(id=selected_category).name
        except Category.DoesNotExist:
            category_name = None
    else:
        products = Product.objects.all()
    
    return render(request, 'store/home.html', {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'category_name': category_name
    })


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/products.html', {'products': products})

def about(request):
    return render(request, 'store/about.html')

def contact(request):
    return render(request, 'store/contact.html')

def order_create(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        quantity = int(request.POST.get('quantity', 1))
        payment_method = request.POST.get('payment_method')

        Order.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            product=product,
            quantity=quantity,
            payment_method=payment_method
        )
        messages.success(request, "✅ Закази шумо қабул шуд. Мо ба зудӣ бо шумо тамос мегирем.")
        return redirect('home')

    return render(request, 'store/order_form.html', {'product': product})
# store/views.py
from django.shortcuts import render

def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.sell_price * quantity
        total += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, f"✅ Маҳсулот {product.name} ба сават илова шуд!")
    return redirect('cart')  # <-- ҳаминро тағир додем

from django.contrib import messages

def checkout_view(request):
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        # Мушаххасоти муштарӣ
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        # Барои ҳар як маҳсулот дар сават заказ эҷод мекунем
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            Order.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                address=address,
                product=product,
                quantity=quantity,
                payment_method=payment_method
            )

        # Саватро холӣ мекунем
        request.session['cart'] = {}

        messages.success(request, "✅ Ҳамаи заказҳои шумо қабул шуданд! Мо ба зудӣ бо шумо тамос мегирем.")
        return redirect('home')

    # GET – намоиши сават ва формаи пардохт
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total_price = product.sell_price * quantity
        total += total_price
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': total_price
        })

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })
