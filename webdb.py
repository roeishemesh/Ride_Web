import datetime

from peewee import *

mysql_db = MySQLDatabase('web.db', user='****', password='****',
                         host='localhost')


class Rides(Model):
    ride_id = AutoField()
    name = CharField()
    phone = CharField()
    date = DateField()
    hour = TimeField()
    departure = CharField()
    destination = CharField()
    several_places = IntegerField(default=-1)
    ride_price = IntegerField(default=-1)
    reference_num = IntegerField(default=None)

    class Meta:
        database = mysql_db


def reference_list():
    list_num = []
    reference = Rides.select(Rides.reference_num)
    for num in reference:
        list_num.append(num.reference_num)
    return list_num


if __name__ == '__main__':
    mysql_db.connect()
    # mysql_db.drop_tables([Rides])
    # mysql_db.create_tables([Rides])
    # Rides.create(name="Roei Shemesh", phone="+972547372008", date="2023-02-20", hour="23:43", departure="TEL AVIV - YAFO",
    #              destination="JERUSALEM", several_places = 3 , ride_price = 30,reference_num = 111111)
    # Rides.create(name="Ofir Trushinsky", phone="+972526526510", date="2023-02-23", hour="14:20", departure="RAMAT GAN",
    #              destination="BE'ER SHEVA",several_places = 2 , ride_price = 20,reference_num = 222222)
    # Rides.create(name="Ron Chanan", phone="+972547372008", date="2023-02-25", hour="10:00", departure="HAIFA",
    #              destination="ASHDOD", ride_price = 25,reference_num = 333333)
    # Rides.create(name="Adam Olivar", phone="+972504697017", date="2023-02-28", hour="12:00", departure="JERUSALEM",
    #              destination="RAMAT GAN",several_places = 3 , ride_price = 0,reference_num = 444444)
    # Rides.create(name="Ido Israel", phone="+972545658923", date="2023-03-29", hour="12:00", departure="TEL AVIV - YAFO",
    #              destination="RAMAT GAN",reference_num = 555555)
