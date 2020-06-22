from django.shortcuts import render
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

    post_listings = soup.find_all('li', {'class': 'result-row'})

    # final_postings = []

    for post in post_listings:
        post_title = post.find(class_='result-title').text
        post_url = post.find('a').get('href')

        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'

        final_image_url = 'https://pixelz.cc/wp-content/uploads/2019/02/bugatti-chiron-sport-110-ans-uhd-4k-wallpaper.jpg'

        # final_postings.append((post_title, post_url, post_price, final_image_url))

        if models.Product.objects.filter(Name=post_title, Price=post_price, Link=post_url, Image=final_image_url):
            continue
        else:
            models.Product.objects.create(Name=post_title, Price=post_price, Link=post_url, Image=final_image_url)

    final_postings = models.Product.objects.all()

    stuff_for_frontend = {
        'Search': search,
        'final_postings': final_postings,
    }
    return render(request, 'frontend/search.html', stuff_for_frontend)