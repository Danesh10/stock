from django.urls import path
from . import views

urlpatterns = [
    path('stock/', views.stock),
    path('stock/<int:id>', views.stock),
    path('upload_stock/', views.upload_stock_price),
    path('get_stock_price/', views.get_stock_price),
    path('recommendation/', views.recommendation),
    path('recommendation/<int:id>', views.recommendation),
    path('Stock_accuracy/', views.stock_accuracy)
]