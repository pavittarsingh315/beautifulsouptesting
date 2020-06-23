from django.shortcuts import render
from django.views.generic import ListView
from . import models
import requests
from requests.compat import quote_plus
from bs4 import BeautifulSoup


def home(request):
    return render(request, 'frontend/base.html')

def new_search(request):
    search = request.POST.get('Search')
    models.Search.objects.create(Search_value=search)

    BASE_CRAIGSLIST_URL = 'https://sacramento.craigslist.org/search/?query={}'
    BASE_IMAGE_URL = 'https://images.craigslist.org/{}_300x300.jpg>'
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    response = requests.get(final_url)
    data = response.text
    soup = BeautifulSoup(data, features='html.parser')

    objs = soup.find_all('li', {'class': 'result-row'})

    for obj in objs:
        title = obj.find(class_='result-title').text
        url = obj.find('a').get('href')

        if obj.find(class_='result-price'):
            price = obj.find(class_='result-price').text
        else:
            price = 'N/A'

        image_url = 'https://i.pinimg.com/originals/09/6a/35/096a35453660aa9b83ba4ab6d9182d61.jpg'
        # image_url = 'https://pixelz.cc/wp-content/uploads/2019/02/bugatti-chiron-sport-110-ans-uhd-4k-wallpaper.jpg'

        # this loop is what updates the field if it needs to be uodated. It also creates the object if the object isnt already there.
        if models.Product.objects.filter(Name=title, Price=price, Link=url):
            if models.Product.objects.filter(Name=title, Price=price, Link=url, Image=image_url):
                continue
            else:
                models.Product.objects.filter(Name=title, Price=price, Link=url).update(Name=title, Price=price, Link=url, Image=image_url)
        else:
            models.Product.objects.update_or_create(Name=title, Price=price, Link=url, Image=image_url)

    final_postings = models.Product.objects.all()


    stuff_for_frontend = {
        'Search': search,
        'final_postings': final_postings,
    }
    return render(request, 'frontend/search.html', stuff_for_frontend)


class SearchList(ListView):
    model = models.Product
    template_name = 'frontend/classSearch.html'
    context_object_name = 'final_postings'
    paginate_by = 21

    # def get_queryset(self):
    #     search = request.POST.get('Search')
    #     return models.Product.objects.filter(Name=search)