# weather_app/views.py
import requests
from django.shortcuts import render, redirect
from .models import City
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    API_KEY = 'e339512a8c96c7d46de19213a4c03368'
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    if request.method == 'POST':
        city = request.POST['city']
        response_data = {}
        
        # Check if city exists
        r = requests.get(url.format(city, API_KEY)).json()
        if r['cod'] == 200:
            if not City.objects.filter(name=city).exists():
                City.objects.create(name=city)
                response_data['status'] = 'success'
                response_data['message'] = f'{city} has been added successfully!'
            else:
                response_data['status'] = 'info'
                response_data['message'] = f'{city} already exists!'
        else:
            response_data['status'] = 'error'
            response_data['message'] = f'{city} not found!'
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(response_data)
        
        return redirect('home')

    cities = City.objects.all()
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name, API_KEY)).json()
        
        city_weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    context = {'weather_data': weather_data}
    return render(request, 'index.html', context)