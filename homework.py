import datetime as dt

class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        format = '%d.%m.%Y'  
        if date is None:
            self.date = dt.datetime.now().date()            
        else:
            self.date = dt.datetime.strptime(date, format).date()

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = [] 
    def add_record(self, Record):
        self.records.append(Record)
    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if record.date == dt.datetime.now().date():
                today_stats += record.amount       
        return today_stats
    def get_week_stats(self):
        week_stats = 0
        today = dt.datetime.now().date()
        week = dt.timedelta(days=7)
        start_date = today - week
        for record in self.records:
            if start_date < record.date <= today:
                week_stats += record.amount
        return week_stats
 

class CashCalculator(Calculator):
    USD_RATE = 77.33
    EURO_RATE = 91.23

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()

        today_remained = self.limit - today_stats
        cash_currency = 'руб'
               
        if currency == 'usd':
            today_remained = today_remained / CashCalculator.USD_RATE
            cash_currency = 'USD'
        elif currency == 'eur':
            today_remained = today_remained / CashCalculator.EURO_RATE
            cash_currency = 'Euro'

        today_remained = round(today_remained, 2)    

        if today_remained > 0:
            return f'На сегодня осталось {today_remained} {cash_currency}'
        elif today_remained == 0:
            return "Денег нет, держись"                 
        else:
            return f'Денег нет, держись: твой долг - {abs(today_remained)} {cash_currency}' 

        

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_calories = self.get_today_stats()
        calories_remained = self.limit - today_calories
        if calories_remained > 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_remained} кКал'
        
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