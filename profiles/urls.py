from django.urls import path, include
from profiles import views

urlpatterns = [
    path('profiles/', views.ProfileList.as_view()),
    path('api-auth/', include('rest_framework.urls')),
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),
]
