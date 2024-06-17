import datetime


class DateHelper:
    @staticmethod
    def get_extended_start_date(start_date, years=10):
        return ((datetime.datetime
                 .strptime(start_date, "%Y-%m-%d") - datetime.timedelta(days=years * 365)
                 ).strftime("%Y-%m-%d"))
