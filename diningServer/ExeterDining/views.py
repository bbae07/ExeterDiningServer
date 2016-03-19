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
        crawl = Crawler()
        crawl.getgetTodayMeals()[0].breakfast
        wBreakfast = crawl.getgetTodayMeals()[0].breakfast
        wLunch = crawl.getgetTodayMeals()[0].lunch
        wDinner = crawl.getgetTodayMeals()[0].dinner
        eBreakfast = crawl.getgetTodayMeals()[1].breakfast
        eLunch = crawl.getgetTodayMeals()[1].lunch
        eDinner = crawl.getgetTodayMeals()[1].dinner
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
        push.sendMessage(crawl.todayStatus)
        return JsonResponse({'PUSH':'SUCCESS'})

def getAPNSToken(request):
    if request.method == 'POST':
        APNS = request.POST['APNS_TOKEN']
        APNSDevice(registration_id = APNS).save()
        return JsonResponse({'Token:': APNS})
