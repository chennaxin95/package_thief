from django.shortcuts import render
from django.views.generic import TemplateView
import requests

# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://cnx.ddns.net'
        port = '8000/info?'
        path = str(request.get_full_path())
        hid = path[path.index('/')+1:]
        address = url+':'+port+'house_id='+str(hid)
        # response = requests.get('http://freegeoip.net/json/')
        response = requests.get(address)
        geodata = response.json()
        print(geodata)
        if geodata is None:
            return render(request, 'index.html')
        else:
            return render(request, 'index.html', {
                'ip': geodata['house_id'],
                'country': geodata['img_id']
                })


class AboutPageView(TemplateView):
    template_name = "about.html"
