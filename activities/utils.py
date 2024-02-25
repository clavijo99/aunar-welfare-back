from datetime import datetime

CHOICES = [(f"{h:02d}:{m:02d}", f"{h:02d}:{m:02d}") for h in range(6, 19) for m in [0, 30]]

DIAS_SEMANA_CHOICES = [
    ('lunes', 'Lunes'),
    ('martes', 'Martes'),
    ('miercoles', 'Miércoles'),
    ('jueves', 'Jueves'),
    ('viernes', 'Viernes'),
    ('sabado', 'Sábado'),
    ('domingo', 'Domingo'),
]


def get_hour_and_minute():
    date = datetime.now()
    hour = date.strftime('%H:%M')

    return hour

def get_day():
    date = datetime.now()
    number_day = date.weekday()
    days = [
'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'
    ]

    return  days[number_day]

