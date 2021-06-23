#!/usr/bin/env python3
from datetime import datetime, timedelta, date
from calendar import monthrange
from .http_service import HTTP


def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]


class PyBob:
    WEEKEND_SET = {4, 5}

    def __init__(self, email, password, start_hour=9, end_hour=18, month_starts=25):
        self.greet()

        start_hour = start_hour if 5 <= start_hour <= 13 else 9
        end_hour = end_hour if 13 <= end_hour <= 24 else 18

        self.http_service = HTTP(debug=True)
        self.email = email
        self.password = password
        self.start_hour = datetime.now().replace(hour=start_hour).strftime('%H')
        self.end_hour = datetime.now().replace(hour=end_hour).strftime('%H')
        self.month_starts = month_starts if 1 <= month_starts <= 31 else 25

        self.login()

        self.user = self.get_user()

    def greet(self):
        print("-- BOB is starting --\n")

    def create_attendance(self, date):
        path = f'/employees/attendance/my'
        payload = {
            "start": f"{date.strftime('%Y-%m-%d')}T{self.start_hour}:00",
            "end": f"{date.strftime('%Y-%m-%d')}T{self.end_hour}:00", "offset": -180
        }

        response = self.http_service.POST(path, payload=payload)

        if response.status_code != 200:
            raise Exception(f"Couldn't create attendance at {date.strftime('%Y-%m-%d')}, \n\t{response.json()['error']}")
        else:
            print(f"-- Created attendance at {date.strftime('%Y-%m-%d')} --")

        return response.json()

    def get_user(self):
        path = '/user'

        response = self.http_service.GET(path)

        if response.status_code != 200:
            raise Exception("Couldn't get user :(")

        return response.json()

    def login(self):
        path = '/login'

        payload = {
            "email": self.email,
            "password": self.password
        }

        response = self.http_service.POST(path, payload=payload)

        if response.status_code != 200:
            print(response.text)
            raise Exception("Bob couldn't login :(")

        return response.json()

    def _generate_monthly_dates(self):
        now = datetime.now()
        first = now.replace(day=1)
        last_month = first - timedelta(days=1)

        previous_month = [date(now.year, last_month.month, day+1)
                          for day in range(number_of_days_in_month(now.year, last_month.month))
                            if date(now.year, last_month.month, day+1).weekday() not in self.WEEKEND_SET and day+1 >= self.month_starts]

        current_month = [date(now.year, now.month, day+1)
                         for day in range(number_of_days_in_month(now.year, now.month)) 
                            if date(now.year, now.month, day+1).weekday() not in self.WEEKEND_SET and day+1 <= self.month_starts]

        return previous_month + current_month

    def fill_monthly_attendance(self):
        dates = self._generate_monthly_dates()
        for day in dates:
            try:
                self.create_attendance(day)
            except Exception as e:
                print(e)
