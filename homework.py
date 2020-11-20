import datetime as dt


class Record:
    FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment  
        if date is None:
            self.date = dt.date.today()            
        else:
            self.date = dt.datetime.strptime(date, self.FORMAT).date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, Record):
        self.records.append(Record)

    def get_today_stats(self):
        today = dt.date.today()     
        return sum(
            record.amount
            for record in self.records
            if record.date == today
        )

    def get_week_stats(self):
        today = dt.date.today()
        start_date = today - dt.timedelta(days=7)
        return sum(
            record.amount
            for record in self.records
            if start_date < record.date <= today
        )


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCIES = {
        'usd': ['USD', USD_RATE],
        'eur': ['Euro', EURO_RATE],
        'rub': ['руб', 1]
        }
    NO_MONEY = 'Денег нет, держись'
    REMAINED = 'На сегодня осталось {remained} {title}'
    DEBT = 'Денег нет, держись: твой долг - {remained} {title}'

    def get_today_cash_remained(self, currency):
        current_limit = self.limit - self.get_today_stats()
        if current_limit == 0:
            return self.NO_MONEY
        title, rate = self.CURRENCIES[currency]
        remained = round(current_limit / rate, 2)    
        if remained > 0:
            return self.REMAINED.format(remained=remained, title=title)
        elif remained < 0:                         
            return self.DEBT.format(remained=abs(remained), title=title)
             
                                           
class CaloriesCalculator(Calculator):
    REMAINED = ('Сегодня можно съесть что-нибудь ещё, но с общей '
                'калорийностью не более {remained} кКал') 
    ENOUGH = 'Хватит есть!'                

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats() 
        if calories_remained > 0:
            return self.REMAINED.format(remained=calories_remained)
        return self.ENOUGH
      

if __name__ == "__main__":

    Cash = CashCalculator(10000)
    Calories = CaloriesCalculator(2600)   
    r1 = Record(amount=9000, comment="Безудержный шопинг")
    r2 = Record(amount=6000, comment="Вино", date="14.11.2020")
    r3 = Record(amount=1000, comment="Конфеты")
    r4 = Record(amount=1000, comment="Тортик")
    r5 = Record(amount=2700, comment="Праздник", date="14.11.2020")
    r6 = Record(amount=700, comment="Пицца", date="16.11.2020")
    Cash.add_record(r1)
    Cash.add_record(r2)
    Cash.add_record(r3)
    Calories.add_record(r4)
    Calories.add_record(r5)
    Calories.add_record(r6)
    print(Cash.get_today_cash_remained('rub'))
    print(Cash.get_today_cash_remained('usd'))
    print(Cash.get_today_cash_remained('eur'))
    print(Calories.get_calories_remained())
