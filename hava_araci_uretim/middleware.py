from django.shortcuts import redirect
from django.conf import settings
from django.urls import resolve

class LoginRequiredMiddleware:
    """
    Bu middleware, kullanıcının oturum açmamışsa belirli sayfalara erişimini engeller.
    Kullanıcı oturum açmadıysa, sadece login ve schema-swagger-ui URL'lerine erişmesine izin verir.
    Diğer tüm sayfalara erişim, kullanıcıyı login sayfasına yönlendirecek şekilde kısıtlanır.
    """

    def __init__(self, get_response): 
        self.get_response = get_response

    def __call__(self, request):
        """
        Her istek geldiğinde çalışacak fonksiyon. 
        """
        # Oturum açmamışsa ve login veya swagger sayfasında değilse
        if not request.user.is_authenticated and resolve(request.path_info).url_name not in ["login", "schema-swagger-ui"]:
            return redirect(settings.LOGOUT_REDIRECT_URL)  # Yönlendirilmesi gereken URL, settings'ten alınır.

        # Eğer oturum açıksa veya geçerli URL login ya da swagger ise, istek normal şekilde işlenir.
        return self.get_response(request)
