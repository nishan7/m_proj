# import pytz
# from datetime import datetime
# from accounts.models import *
# a= CustomUser.objects.get(pk=1)
# a.get_dates()
#
# india = pytz.timezone('Asia/Kolkata')
# current = india.localize(datetime.now())
# # current_hour = int(current.strftime('%H'))
#
# booked_dates = [d for d in a.dates_booked.all() if d.date > current]
#
# available_dates = []
# start_date = datetime(year=current.year, month=current.month, day=current.day, hour=9)
# available_dates.append(start_date)
# for i in range(7):
#     available_dates.append(start_date + timedelta(hours=5))
#     available_dates.append(start_date + timedelta(hours=19))
# # return avaiable_dates


from mapp.models import *

a = Chat.objects.get(pk=1)

for message_obj in a.message.all():
    print(message_obj.text, message_obj.sender_id)