from django.db import models
from stockant.models import DateMixin
from django.contrib.auth.models import User

class Stock(DateMixin):
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=10)
    sector = models.CharField(max_length=30)
    bse_script_code = models.CharField(max_length=30)
    bse_house_code = models.CharField(max_length=30)
    stock_flag = models.CharField(max_length=30, blank=True)
    market_cap = models.FloatField(null=True, blank=True)
    market_cap_str = models.CharField(max_length=30, null=True, blank=True)

    def get_json(self):
        return dict(
            id=self.id,
            name=self.name,
            short_name=self.short_name,
            sector=self.sector,
            stock_flag = self.stock_flag,
            bse_script_code=self.bse_script_code,
            bse_house_code=self.bse_house_code,
            market_cap=self.market_cap,
            market_cap_str=self.market_cap_str)
class StockPrice(DateMixin):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    open = models.FloatField(null=True, blank=True)
    close = models.FloatField(null=True, blank=True)
    day_high = models.FloatField(null=True, blank=True)
    day_low = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    def get_json(self):
        return dict(
            id=self.id,
            stock={'id': self.stock.id, 'name': self.stock.name, 'sector': self.stock.sector},
            open=self.open,
            close=self.close,
            day_high=self.day_high,
            day_low=self.day_low,
            date=self.date,
            created=self.created,
            modified=self.modified
        )
class Recommendation(DateMixin):
    HORIZON_CHOICES = (('b', 'Buy'), ('s', 'Sell'), ('h', 'Hold'))
    PERIOD_CHOICES = (('w', 'Week'), ('m', 'Month'), ('q', 'Quarter'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    current_price = models.FloatField()
    target_price = models.FloatField()
    horizon = models.CharField(choices=HORIZON_CHOICES, max_length=30)
    period = models.CharField(choices=PERIOD_CHOICES, max_length=30)
    number = models.IntegerField()
    year = models.IntegerField()
    result_date_time = models.DateTimeField()
    accuracy = models.FloatField(null=True, blank=True)

    def get_json(self):
        return dict(
             id = self.id,
             user = {'id': self.user.id, 'first_name': self.user.first_name, 'last_name': self.user.last_name},
             stock = self.stock.id,
             current_price = self.current_price,
             target_price = self.target_price,
             horizon = self.horizon,
             period = self.period,
             number = self.number,
             year = self.year,
             result_date_time = self.result_date_time,
             accuracy = self.accuracy)