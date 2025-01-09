from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .serializers import LoginSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


class LoginView(APIView):
    """
    Login işlemi için kullanılan API View.
    Kullanıcı adı ve şifre doğrulaması yaparak, başarılı login sonrası kullanıcıyı sisteme giriş yapar.
    """

    @swagger_auto_schema(
        request_body=LoginSerializer,  # Login isteği için kullanılacak serializer
        responses={  # İstek sonrası dönecek olası cevaplar
            200: openapi.Response("Login successful!"),  
            400: openapi.Response("Invalid credentials!"),   
        },
    )
    def post(self, request):
        """
        Kullanıcıyı sisteme giriş yapmak için kullanılan POST methodu.
        Kullanıcı adı ve şifreyi alarak doğrulama işlemi gerçekleştirir.
        """
        serializer = LoginSerializer(data=request.data)
        
        # Serializer verisi geçerli mi kontrol edilir
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if validated_data:
                username = validated_data["username"]  
                password = validated_data["password"]   
            else:
                return Response(
                    {"error": "Invalid data!"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Kullanıcı adı ve şifre ile doğrulama yapılır
            user = authenticate(request, username=username, password=password)
            if user is not None:  # Eğer kullanıcı doğrulandıysa giriş yapılır
                login(request, user)
                return Response(
                    {"message": "Login successful!"}, status=status.HTTP_200_OK
                )
            # Kullanıcı doğrulanamazsa hata mesajı döndürülür
            return Response(
                {"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        # Eğer serializer hatalıysa, hata mesajları döndürülür
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Logout işlemi için kullanılan API View.
    Kullanıcıyı sistemden çıkararak oturumu sonlandırır.
    """

    @swagger_auto_schema(
        responses={  
            200: openapi.Response("Logout successful!"),  
        },
    )
    def get(self, request):
        """
        Kullanıcıyı sistemden çıkartmak için kullanılan GET methodu.
        Kullanıcıyı oturumdan çıkarır ve başarı mesajı döndürür.
        """
        logout(request) 
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)


@login_required
def get_user_info(request):
    """
    Giriş yapmış olan kullanıcının bilgilerini döndüren view.
    Sadece oturum açmış kullanıcılar bu veriye erişebilir.
    """

    user = request.user  # Oturum açmış kullanıcı bilgisi alınır
    return JsonResponse(
        {
            "username": user.username, 
            "first_name": user.first_name, 
            "last_name": user.last_name, 
        }
    )
