from django.shortcuts import render
from .push import Push
from .crawler import Crawler
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view
from push_notifications.models import APNSDevice

# Create your views here.
def restaurant_list(request, format=None):

    if request.method == 'GET':
        # crawl = Crawler()
        # wetherell = crawl.getTodayMeals()[0]
        # elmStreet = crawl.getTodayMeals()[1]
        # wBreakfast = wetherell.breakfast;
        # wLunch = wetherell.lunch;
        # wDinner = wetherell.dinner;
        # eBreakfast = elmStreet.breakfast;
        # eLunch = elmStreet.lunch;
        # eDinner = elmStreet.dinner;

        wBreakfast = ['Chilled Fruit Juices']
        wLunch = ['Home Fried Potatoes','Yo-nola Bar','Soup du Jour']
        wDinner = ['Steamed Vegetable','Manager Choice Dessert']
        eBreakfast = ['Pete & Gerrys Organic Boiled Eggs','Ham and Cheese Omelet','Corned Beef Hash']
        eLunch = ['Roast Pork Loin','Pepperoni Calzone from the Hearth','Chicken Caesar Salad']
        eDinner = ['Edamame Stir Fry','Sweet Potato Fries','Roasted Vegetable','Homemade Waffles','Steel Cut Oatmeal']
        return JsonResponse(
        {'Restaurants':
             [{'Wetherell':
                  {'breakfast':wBreakfast, 'lunch':wLunch, 'dinner':wDinner}},
             {'Elm Street':
                  {'breakfast':eBreakfast, 'lunch':eLunch, 'dinner':eDinner}}]
         })

def sendPushMessage(request,):
    if request.method == 'GET':
        push = Push()
        crawl = Crawler()
        push.sendMessage(1)
        return JsonResponse({'PUSH':'SUCCESS'})

def getAPNSToken(request):
    if request.method == 'POST':
        APNS = request.POST['APNS_TOKEN']
        APNSDevice(registration_id = APNS).save()
        return JsonResponse({'Token:': APNS})
