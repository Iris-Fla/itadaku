from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.MenuListView.as_view(), name='menu_list'),
    path('menu/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu_item_detail'),
    path('menu/<int:pk>/translate/', views.translate_menu_item, name='translate_menu_item'),
    path('pdf_export/', views.pdf_export_view, name='pdf_export'),
]