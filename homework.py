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
        today_stats = []
        today = dt.date.today()
        for record in self.records:
            if record.date == today:
                today_stats.append(record.amount)      
        return sum(today_stats)

    def get_week_stats(self):
        week_stats = []
        today = dt.date.today()
        week = dt.timedelta(days=7)
        start_date = today - week
        for record in self.records:
            if start_date < record.date <= today:
                week_stats.append(record.amount)
        return sum(week_stats)


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    CURRENCIES = {
        'usd': ['USD', USD_RATE],
        'eur': ['Euro', EURO_RATE],
        'rub': ['руб', 1]
        }

    def get_today_cash_remained(self, currency):
        currency_title, currency_rate = self.CURRENCIES[currency]
        today_remained = (round(((self.limit - self.get_today_stats())/currency_rate), 2))
        if today_remained == 0:
            return "Денег нет, держись"
        elif today_remained > 0:
            return f'На сегодня осталось {today_remained} {currency_title}'                 
        
        return f'Денег нет, держись: твой долг - {abs(today_remained)} {currency_title}' 

        
class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        today_calories = self.get_today_stats()
        calories_remained = self.limit - today_calories
        answer_remained = (f'Сегодня можно съесть что-нибудь ещё, ' 
                f'но с общей калорийностью не более {calories_remained} кКал')
        if calories_remained > 0:
            return answer_remained
        
        return f'Хватит есть!'
      

if __name__ == "__main__":

    Cash = CashCalculator(10000)
    Calories = CaloriesCalculator(2600)   
    r1 = Record(amount=10000, comment="Безудержный шопинг")
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
