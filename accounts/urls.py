from django.urls import path
from .views import LoginView, LogoutView, get_user_info

# URL yönlendirmeleri, her endpoint için ilgili view'a yönlendirme yapılır.
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),  # Kullanıcı giriş işlemi
    path("logout/", LogoutView.as_view(), name="logout"),  # Kullanıcı çıkış işlemi
    path("user-info/", get_user_info, name="user-info"),  # Kullanıcı bilgilerini getirir
]
