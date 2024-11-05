from datetime import date
import calendar
from functools import reduce
import json
import requests

headers = {
  'Content-Type': 'application/json',
  'X-Master-Key': '$2a$10$/TWDsCEqojtm0RRDIPr9hOCk1VPUamHb0rzrn8z.tnNYPkYr1EPNK',
  'X-Bin-Meta' : 'false'
}

url_plants = 'https://api.jsonbin.io/v3/b/65f88285266cfc3fde9a434f'
url_days = 'https://api.jsonbin.io/v3/b/66054bd2acd3cb34a82f91cc'


def numOfDays(date1, date2):
    return reduce(lambda x, y: (y-x).days, [date1, date2])


def calendar_manager(num_of_waterings, num_of_days):
    date_of_watering = []
    prev_date = [0, 0, 0]
    prev_day = prev_date[0]
    prev_month = prev_date[1]
    prev_year = prev_date[2]

    d = round(30 / num_of_days)

    num_of_days = 30
    num_of_waterings *= d

    num = round(num_of_days / num_of_waterings)
    today = date.today()
    t_date = str(today).split('-')
    t_day = int(t_date[2])
    t_month = int(t_date[1])
    t_year = int(t_date[0])
    if prev_date[0] == 0 or numOfDays(date(prev_year, prev_month, prev_day), date(t_year, t_month, t_day)) > num:
        day, month, year = t_day, t_month, t_year
        date_of_watering.append(str(day)+ '.' + str(month) + '.' + str(year))
    else:
        day, month, year = prev_day, prev_month, prev_year

    num_of_days_in_month = int(str(calendar.monthrange(year, month)[1]))

    new_day = day
    new_month = month
    new_year = year

    while (len(date_of_watering)) != num_of_waterings:
        new_day += num
        if new_day > num_of_days_in_month:
            new_month += 1
            new_day = new_day - num_of_days_in_month
            if new_month > 12:
                new_year += 1
                new_month = 1
            num_of_days_in_month = int(str(calendar.monthrange(new_year, new_month)[1]))
        date_of_watering.append(str(new_day)+ '.' + str(new_month) + '.' + str(new_year))
    
    return date_of_watering


def json_put(plants, dates):
    data = {"watering":{}}
    for i in range(len(plants)):
        data["watering"][str(plants[i])] = dates[i]
    
    req = requests.put(url_days, json=data, headers=headers)
    
    
def calculate_days_of_watering(data):
    global headers, url_plants
    
    req = requests.get(url_plants, json=None, headers=headers)
    plants = json.loads(req.text)['plants_list']
    days_of_watering = []
    
    nums_of_waterings = [x[0] for x in data]
    nums_of_days = [x[1] for x in data]
    
    for i in range(len(plants)):
        days_of_watering.append(calendar_manager(nums_of_waterings[i], nums_of_days[i]))
        
    json_put(plants, days_of_watering)    

data = [[1,7], [2,7], [3,15]]
calculate_days_of_watering(data)