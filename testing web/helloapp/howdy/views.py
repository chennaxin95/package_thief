from django.shortcuts import render
from django.views.generic import TemplateView
import requests
from PIL import Image
import numpy as np
import os

# Create your views here.


class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://cnx.ddns.net'
        port = '8000/'

        path = str(request.get_full_path())
        print(path)
        hid = path[path.index('=')+len('='):]
        # address = url+':'+port+'house_id='+str(hid)
        address = url+':'+port+"info?house_id=" + hid
        response = requests.get(address)
        data = response.json()
        # print(response)
        print(data)
        # array = np.fromstring(data['last_img'], dtype=np.uint8)
        # img = Image.fromarray(array, 'RGB')
        # img.save('image/'+'house_id_'+hid+'.png')
        cwd = os.getcwd()+"/howdy/static/images/"
        address = url+':'+port+"last_image?house_id=" + hid
        response = requests.get(address)
        if response.status_code ==200:
            name = cwd+hid+".png"

            with open(name, 'wb') as f:
                f.write(response.content)


        if data is None:
            return render(request, 'index.html')
        else:
            return render(request, 'index.html', {
                'house_id': data['house_id'],
                'img_id': data['img_id'],
                'status': data['house_status']
                })
    

class AboutPageView(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://cnx.ddns.net'
        port = '8000/'
        address = url+':'+port+'all_house'
        print(address)
        # address = url+':'+port
        # response = requests.get('http://freegeoip.net/json/')
        response = requests.get(address)
        data = response.json()
        lst = data['all']
        output = set()
        for x in lst:
            output.add(x)
        output = list(output)
        
        print(address)
        if data is None:
            return render(request, 'about.html')
        else:
            return render(request, 'about.html', {
                'all': output,
                })


class ReportPageView(TemplateView):
    def get(self, request, **kwargs):
        url = 'http://cnx.ddns.net'
        port = '8000/'

        path = str(request.get_full_path())
        print(path)
        hid = path[path.index('house_id=')+len('house_id='):]
        # address = url+':'+port+'house_id='+str(hid)
        address = url+':'+port+"change_status?house_id="+hid
        # response = requests.get('http://freegeoip.net/json/')
        print(address)
        response = requests.post(address)
        data = response.json()
        # print(data)
        return render(request, 'report.html', {'house_id':hid})
        
