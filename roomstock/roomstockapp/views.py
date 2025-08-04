from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout as auth_logout
from django.db.models import Sum, Count, Q
from .forms import ProductForm
from .models import Product, Category

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # Calculate dashboard statistics
        user_products = Product.objects.filter(user=request.user, is_active=True)
        
        total_items = user_products.count()
        low_stock_items = user_products.filter(quantity__lte=10).count()
        total_categories = Category.objects.filter(product__user=request.user).distinct().count()
        total_value = user_products.aggregate(total=Sum('price'))['total'] or 0
        
        context = {
            'total_items': total_items,
            'low_stock_items': low_stock_items,
            'total_categories': total_categories,
            'total_value': total_value,
        }
        
        return render(request, "inventory/dashboard.html", context)
    else:
        return render(request, "inventory/index.html")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully")
            return redirect("login")
        else:
                form = UserCreationForm()
    return render(request,"auth/register.html",{'form':form})

def login_view(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f"Welcome back, {username} !!!!")
                return redirect("index")
            else:
                messages.error(request,"Invalid username or password")
        else:
            messages.error(request,"Invalid username or password")
    return render(request,"auth/login.html",{'form': form})

def logout_view(request):
    auth_logout(request)
    messages.info(request,'Logged out successfully !!!')
    return render(request, "auth/logout.html", {
        'logout_time': 'Just now'
    })

def addnewitem(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('index')
    else:
        form = ProductForm()
    
    return render(request, 'inventory/add_item.html', {'form': form})

def inventory_list(request):
    # Get user's products
    products = Product.objects.filter(user=request.user, is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Calculate statistics
    total_products = products.count()
    low_stock_count = products.filter(quantity__lte=10).count()
    total_value = products.aggregate(total=Sum('price'))['total'] or 0
    
    context = {
        'products': products,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'total_value': total_value,
    }
    
    return render(request, 'inventory/inventory_list.html', context)

def display_item(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, user=request.user)
    return render(request, 'inventory/display.html', {'item': product})

def edit_item(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, user=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('inventory_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/edit.html', {'form': form, 'item': product})

def delete_item(request, product_id):
    product = get_object_or_404(Product, product_id=product_id, user=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('inventory_list')
    
    return render(request, 'inventory/delete.html', {'item': product})
