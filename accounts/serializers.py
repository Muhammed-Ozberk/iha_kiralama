from rest_framework import serializers

# Kullanıcı girişi için gerekli veriyi doğrular
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)  # Kullanıcı adı
    password = serializers.CharField(required=True, write_only=True)  # Şifre (sadece yazma izni)
