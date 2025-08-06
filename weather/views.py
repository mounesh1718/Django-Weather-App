from django.shortcuts import render
import json
import urllib.request
import urllib.error

def index(request):
    city = ''
    data = {}

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        if not city:
            data = {'error': 'City name cannot be empty.'}
        else:
            api_key = 'e7eec55a0ddbb3c8d5edac284e54ddc9'
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
            try:
                res = urllib.request.urlopen(url).read()
                json_data = json.loads(res)
                data = {
                    'country_code': str(json_data['sys']['country']),
                    'coordinate': f"{json_data['coord']['lon']}, {json_data['coord']['lat']}",
                    'temp': str(round(json_data['main']['temp'] - 273.15, 2)) + ' °C',
                    'pressure': str(json_data['main']['pressure']),
                    'humidity': str(json_data['main']['humidity']),
                }
            except urllib.error.HTTPError:
                data = {'error': 'City not found. Please enter a valid city name.'}
            except Exception as e:
                data = {'error': f"Error: {str(e)}"}
            

    return render(request, 'index.html', {'city': city, 'data': data})
