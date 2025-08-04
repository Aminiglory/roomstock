from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'price', 'quantity', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter product name',
                'required': True
            }),
            'sku': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter SKU (Stock Keeping Unit)',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter product description...',
                'rows': 4
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0',
                'step': '1',
                'min': '0',
                'required': True
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0',
                'min': '0',
                'required': True
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': False
            })
        }
        labels = {
            'name': 'Product Name',
            'sku': 'SKU',
            'description': 'Description',
            'price': 'Price (RWF)',
            'quantity': 'Quantity',
            'category': 'Category'
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make category field optional and add empty choice
        self.fields['category'].empty_label = "Select a category (optional)"
        self.fields['category'].required = False
        
        # Make description field optional
        self.fields['description'].required = False

    def clean_sku(self):
        sku = self.cleaned_data.get('sku')
        if sku:
            # Check if SKU already exists (excluding current instance if editing)
            existing_products = Product.objects.filter(sku=sku)
            if self.instance.pk:
                existing_products = existing_products.exclude(pk=self.instance.pk)
            
            if existing_products.exists():
                raise forms.ValidationError("This SKU already exists. Please choose a unique SKU.")
        return sku

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Price cannot be negative.")
        return price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity