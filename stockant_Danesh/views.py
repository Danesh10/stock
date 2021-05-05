import json
from .models import *
from django.http import JsonResponse
import pandas as pd
import requests as req
from django.core.exceptions import ObjectDoesNotExist
from .last_date import *
from datetime import date, datetime, timedelta
from django.db.models import Avg

def stock(request, id=None):
    response = []

    if request.method == "POST":
        params = json.loads(request.body)
        instance = Stock.objects.create(**params)
        return JsonResponse(dict(validation="", status=True, data=[instance.get_json()]))

    if request.method == "GET":
        name = request.GET.get('name')
        kwargs = {}
        if id:
            kwargs['id'] = id
        if name:
            kwargs['name'] = name

        queryset = Stock.objects.filter(**kwargs)

        for instance in queryset:
            response.append(instance.get_json())

        return JsonResponse(dict(validation="", status=True, data=response))


    if request.method == "PUT":
        params = json.loads(request.body)
        queryset = Stock.objects.get(id=id)
        instance = queryset.update(params)
        instance.save()
        return JsonResponse(dict(validation="", status=True, data=[instance.get_json()]))

    if request.method == "PATCH":
        params = json.loads(request.body)
        queryset = Stock.objects.filter(id=id)
        print("params", params)
        queryset.filter(id=id).update(**params)
        return JsonResponse(dict(validation="", status=True, data=[queryset.last().get_json()]))

    if request.method == "DELETE":
        Stock.objects.filter(id=id).delete()
        return JsonResponse(dict(validation="Deleted Successfully.", status=True))

def upload_stock(request):
    file = request.FILES.get('file')
    df = pd.read_csv(file)
    df = df[['StockName', 'stock_short_name', 'bse_code', 'house_code', 'StockSector', 'stock_flag']]

    df = df.rename(columns={"StockName": "name", "stock_short_name": "short_name",
                            "bse_code": "bse_script_code", "house_code": "bse_house_code",
                            "StockSector": "sector"})
    data = df.to_dict(orient='records')[5:10]

    for instance in data:
        Stock.objects.create(**instance)

    return JsonResponse(dict(validation="Uploaded successfully.", status=True))

def get_stock_price(request):
    stock_price = [{'stock_id': 6, 'open': 10.0, 'close': 15.0, 'day_high': 16.0, 'day_low': 10.0},
                   {'stock_id': 7, 'open': 10.0, 'close': 15.0, 'day_high': 17.0, 'day_low': 10.0},
                   {'stock_id': 8, 'open': 10.0, 'close': 15.0, 'day_high': 18.0, 'day_low': 10.0},
                   {'stock_id': 9, 'open': 10.0, 'close': 15.0, 'day_high': 19.0, 'day_low': 10.0},
                   {'stock_id': 10, 'open': 10.0, 'close': 15.0, 'day_high': 25.0, 'day_low': 10.0}]

    return JsonResponse(dict(validation="success", status=True, data=stock_price))


def upload_stock_price(request):
    url = 'http://127.0.0.1:7000/base/get_stock_price/'
    response = req.get(url).json().get('data')
    print("response", response)
    for stock_price in response:
        print(stock_price)
        try:
            instance = StockPrice.objects.get(stock__id=stock_price['stock_id'], date='2021-04-23')
            print("Exist")
        except ObjectDoesNotExist:
            print("Not Exist")
            stock_instance = Stock.objects.get(id=stock_price['stock_id'])
            instance = StockPrice.objects.create(stock=stock_instance,
                                                 date='2021-04-23')
        instance.open = stock_price['open']
        instance.close = stock_price['close']
        instance.day_high = stock_price['day_high']
        instance.day_low = stock_price['day_low']
        instance.save()

    return JsonResponse(dict(validation="Uploaded successfully.", status=True, data=response))

def recommendation(request, id=None):
    recommendation_list = []
    if request.method == "POST":
        param = json.loads(request.body)
        param['user'] = User.objects.get(id=param['user'])
        param['stock'] = Stock.objects.get(id=param['stock'])
        today = date.today()
        if param['period'] == "w":
            year, week_num, day_of_week = datetime.now().isocalendar()
            param['number'] = week_num
            param['result_date_time'] = date.today() + timedelta((4 - today.weekday()) % 7)
        if param['period'] == "m":
            param['number'] = datetime.now().month
            param['result_date_time'] = LastFriday()
        if param['period'] == "q":
            param['number'] = (datetime.now().month-1)//3+1
            param['result_date_time'] = get_last_friday_of_the_quarter(today)
        param['year'] = datetime.now().year
        instance = Recommendation.objects.create(**param)
        return JsonResponse(dict(validation="data saved", status=True, data=[instance.get_json()]))

    if request.method == "GET":
        kwarg = {}
        if id:
            kwarg['id'] = id
        queryset = Recommendation.objects.filter(**kwarg)
        for recommendations in queryset:
            recommendation_list.append(recommendations.get_json())
        print(recommendation_list)
        return JsonResponse(dict(valdation="success", status=True, data=recommendation_list))

    if request.method == "PATCH":
        params = json.loads(request.body)
        queryset = Recommendation.objects.filter(id=id)
        print("params", params)
        queryset.filter(id=id).update(**params)
        return JsonResponse(dict(validation="", status=True, data=[queryset.last().get_json()]))

    if request.method == "DELETE":
        param = json.loads(request.body)
        Recommendation.objects.get(id=id).delete()
        return JsonResponse(dict(validation="data deleted", status=True))

#def stock_accuracy(request, id=None):
   # stock_list = []
    #Accuracy_list = []
   # kwarg = {}
  #  #if id :
    #    kwarg['stock_id'] = id
   # queryset = Recommendation.objects.filter(**kwarg).\
  #      values('stock_id', 'accuracy').annotate(Avg('accuracy'))
 #   print(queryset)
  #       Accuracy_list.append(list(recommendations.values()))
#        stock_list.append(list(recommendations.values()))
#        plt.plot.scatter(Accuracy_list, stock_list)
 #       matplotlib.pyplot.show()
    return JsonResponse(dict(validation="success", status=True, x_axis=stock_list, y_axis=Accuracy_list))


# """
# step1:- Find unique stock
# step2:- Fetch accuracy
# step3:- if unique_stock then find average
# """
def stock_accuracy(request):
    x_axis = []
    y_axis = []

    queryset = Recommendation.objects.all()
    stock_list =list(set([x.stock.short_name for x in queryset]))


    for short_name in stock_list:
        temp_queryset = queryset.filter(stock__short_name=short_name)
        if temp_queryset.count()>1:
            accuracy = temp_queryset.aggregate(accuracy=Avg('accuracy'))['accuracy']
        else:
            print("temp_queryset.last()", temp_queryset.last().id)
            accuracy = temp_queryset.last().accuracy
        x_axis.append(short_name)
        y_axis.append(accuracy)
        return JsonResponse(dict(validation="success", status=True, x_axis=x_axis, y_axis=y_axis))
