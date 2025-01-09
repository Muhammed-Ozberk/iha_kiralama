from django.shortcuts import render

# Ana sayfa için view
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def list_part(request):
    return render(request, "list-part.html")

def create_part(request):
    return render(request, "creat-part.html")

def create_air_vehicle(request):
    return render(request, "create-air-vehicle.html")

def list_air_vehicle(request):
    return render(request, "list-air-vehicle.html")
