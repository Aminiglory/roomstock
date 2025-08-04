from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("register",views.register,name="register"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("additem",views.addnewitem,name="add_item"),
    path("inventory",views.inventory_list,name="inventory_list"),
    path("item/<int:product_id>",views.display_item,name="display_item"),
    path("item/<int:product_id>/edit",views.edit_item,name="edit_item"),
    path("item/<int:product_id>/delete",views.delete_item,name="delete_item"),
    path("profile",views.view_profile,name='profile')
]
