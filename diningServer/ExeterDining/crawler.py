#-*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import datetime

BASE_URL = 'http://www.exeter.edu/student_life/14202_15947.aspx'
restaurants = ['Wetherell','Elm Street']
days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
urlText = []
mealTypes = ['Breakfast','Lunch','Dinner']

#lblBreakfastWednesday
#요일별 상수화hp
#time zone = (UTC/GMT - 5)

class ERestaurantStatus:
    USUAL_BUSINESS = 0
    WEEKEND_BUSINESS = 1
    CLOSE_BUSINESS = 2


class ERestaurant:
    breakfast = []
    lunch = []
    dinner = []
    def __init__(self,br=None,lu=None,di=None):
        self.breakfast = br
        self.lunch = lu
        self.dinner = di

class Crawler:
    weekMeals = []
    wetherell = ERestaurant()
    elmStreet = ERestaurant()
    restaurants = [wetherell,elmStreet]
    todayStatus = ERestaurantStatus.USUAL_BUSINESS
    def raw_html(self):
        try:
            handle = urllib.request.urlopen(BASE_URL)
            html_gunk = handle.read()
        except:
            html_gunk = 'None'
        return html_gunk
    def currentHour(self):
        #데이터받은뒤에푸쉬할때필요
        #보스턴 시간 = UTC/GMT - 5 hours
        return datetime.datetime.utcnow().hour - 5
    def currentMinute(self):
        return datetime.datetime.utcnow().minute
    def currentTime(self):
        return datetime.datetime.utcnow()
    def currentDayOfWeek(self):
        #데이터받아오기전에필요
        #크롤링할 때 가장 먼저 나오는 데이터가 Sunday 값이므로 자체적으로 Sunday를 인덱스 0으로 시작한다
        #그러므로 기존 python API에 +1을 시켜줘서 이를 맞춰준다
        index = datetime.datetime.today().weekday()
        return index
        #return days[datetime.datetime.today().weekday()+1]
    def getWeekendsMeals(self,todayIndex):
        rawBr = self.weekMeals[todayIndex].findChildren('p')
        rawLu = self.weekMeals[todayIndex+1].findChildren('p')
        rawDi = self.weekMeals[todayIndex+2].findChildren('p')
        rawMealTypes = [rawBr,rawLu,rawDi]
        br = []
        lu = []
        di = []
        meals = [br,lu,di]
        for idx , mealType in enumerate(rawMealTypes):
            for meal in mealType:
                current = meal.text
                try:
                    current = str(current)
                except:
                    current = str(current.encode('utf-8'))
                meals[idx].append(current)
        #self.wetherell = ERestaurant(br,lu,di)
        self.wetherell = ERestaurant()
        self.elmStreet = ERestaurant(br,lu,di)
    def getWeekdaysMeals(self,todayIndex):
        we = []
        el = []
        for mealIndex in range(todayIndex,todayIndex+2):
            meals = self.weekMeals[mealIndex].findChildren('p')
            tmpWE = []
            tmpEL = []
            for meal in meals:
                divPoint = False
                current = meal.text
                try:
                    current = str(current)
                except:
                    current = str(current.encode('utf-8'))
                if current == '\xc3\x82':
                    divPoint = True
                    continue
                if divPoint is False:
                    tmpWE.append(current)
                else:
                    tmpEL.append(current)
            if tmpWE[0] == 'Elm Street':
                swap = tmpWE
                tmpWE = tmpEL
                tmpEL = swap
            we.append(tmpWE)
            el.append(tmpEL)
        self.wetherell = ERestaurant(we[0],we[1],we[2])
        self.elmStreet = ERestaurant(el[0],el[1],el[2])

    def getTodayMeals(self):
        print(self.raw_html())
        soup = BeautifulSoup(self.raw_html(),"html.parser")
        self.weekMeals = soup.findAll("td")
        #21개 3끼 x 7일 순서는 일요일아침~토요일저녁
        if len(self.weekMeals) == 0:
            #문닫았을 때 메뉴 리스팅이 없음. 'td' 엘리먼트들이 아예 존재하지 않는다.
            self.todayStatus = ERestaurantStatus.CLOSE_BUSINESS
            self.restaurants = [ERestaurant(),ERestaurant()]
            return self.restaurants

        #일요일아침부터 ~ 토요일저녁까지, 21개의 td오브젝트 --> 한 요일당 3개의 오브젝트라 '*3' 처리
        #todayIndex = Breakfast, todayIndex+1 = Lunch , todayIndex+2 = Dinner
        dayIndex = self.currentDayOfWeek()
        todayIndex = dayIndex * 3
        if dayIndex == 0 or dayIndex == 6:
            self.todayStatus = ERestaurantStatus.WEEKEND_BUSINESS
            self.getWeekendsMeals(todayIndex)
        else:
            self.getWeekdaysMeals(todayIndex)
        self.restaurants = [self.wetherell,self.elmStreet]
        return self.restaurants

"""
def _unpack (row,kind='td'):
    elts = row.findall('.//%s' % kind)
    return [val.text for val in elts]

def parse_options_data (table):
    rows = table.findall('.//tr')
    header = _unpack(rows[0],kind='th')
    data = [_unpack(r) for r in rows[1:]]
    return TextParser(data,names=header).get_chunk()
"""

if __name__ == "__main__":
    crawl = Crawler()
    restaurants = crawl.getTodayMeals()
    status = crawl.todayStatus
    print(restaurants)
    print(restaurants[0])
    print(restaurants[1])
    print('Current number of restaurants is '+str(len(restaurants)))
    print('Current status is '+str(status))