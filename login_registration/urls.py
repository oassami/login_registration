from django.urls import path, include

urlpatterns = [
    path('', include('log_reg_app.urls')),
]
