from email.mime.text import MIMEText
import requests
import datetime
import hashlib
import json
import time
import smtplib

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")
        
def main():
    password = open("password.txt", "r").read()
    while True:
        try:
            appointments = fetchAll()
            filter = AppointmentFilter(datetime.datetime(2000, month=8, day=8), datetime.datetime(2024, month=5, day=1))
            filtered_appointments = filter_appointments(appointments, filter)
            for appointment in filtered_appointments:
                print(f"FOUND! {appointment.date} at: {datetime.datetime.now()}")
                send_email(f"New Appoitment available at! {appointment.date}", f"New Appoitment available at! {appointment.date} \
                    https://maccabi-dent.com/%D7%AA%D7%95%D7%A8-%D7%9C%D7%9C%D7%90-%D7%A1%D7%99%D7%A1%D7%9E%D7%90/",  "noamkautomail@gmail.com", ["glevy2012@gmail.com", "noamko25@gmail.com"], password)

        except Exception as e:
            print("Error: ", e)
        finally:
            time.sleep(10)

def fetchAll():
    url = "https://maccabi-dent.com/wp-admin/admin-ajax.php"

    data = "action=get_lines&data%5Bmacabi_id%5D=1&data%5Bservice_type%5D=hygenist&data%5Bage%5D=Y&paged=1&selecteddoc=&getnearby=true&updateminicalander=true&specificdate=&bday=1995-10-26&show_video="
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.9,he;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://maccabi-dent.com',
        'Referer': 'https://maccabi-dent.com/%D7%AA%D7%95%D7%A8-%D7%9C%D7%9C%D7%90-%D7%A1%D7%99%D7%A1%D7%9E%D7%90/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Not(A:Brand";v="24", "Chromium";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'}
    
    appointments = []
    try:
        res = requests.post(url, headers=headers, data=data)
        if res.status_code == 200:
            result = json.loads(res.text)
            if result['status'] == "success":
                for key in result['lines']:
                    for line in result['lines'][key]:
                        id = hashlib.sha224((line + key).encode()).hexdigest()
                        app = result['lines'][key][line]
                        year = int(app['year'])
                        month = int(app['month'])
                        day = int(app['day'])
                        time = app['time'].split(":")
                        hour = int(time[0])
                        minute = int(time[1])
                        date = datetime.datetime(year, month, day, hour, minute)
                        appointments.append(Appointment(id, date))
    except Exception as e:
        print("Error: ", e)
    return appointments

class AppointmentFilter:
    def __init__(self, fromDate, toDate):
        self.fromDate = fromDate
        self.toDate = toDate

class Appointment:
    def __init__(self,id, date):
        self.id = id
        self.date = date
        
def filter_appointments(appointments, filter: AppointmentFilter):
    filtered_appointments = []
    for appointment in appointments:
        if appointment.date >= filter.fromDate and appointment.date <= filter.toDate:
            filtered_appointments.append(appointment)
    return filtered_appointments

main()