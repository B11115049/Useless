#from django.db import models
from django.contrib.gis.db import models
import geopy.distance
from geopy.geocoders import Nominatim
from django.db.models.signals import pre_delete
from django.dispatch import receiver
# Create your models here.

geolocator = Nominatim(user_agent="djangoTest, email = ian523411756@gmail.com")
geolocator.headers = {'Accept-Language': 'en'}

class User(models.Model):
    name = models.CharField(max_length = 20, unique = True)
    passwd = models.CharField(max_length = 50)
    email = models.CharField(max_length = 50, unique = True)
    phone = models.CharField(max_length = 50, unique = True)
    wallet = models.PositiveBigIntegerField(editable = False,default = 0)

    def __str__(self):
        return self.name

class Record(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    startPlace = models.PointField()
    endPlace = models.PointField()
    routeLength = models.FloatField(editable = False)
    point = models.PositiveIntegerField(editable = False)
    dateTime = models.DateTimeField(auto_now_add = True,null = True)
    start = models.CharField(max_length = 200, null = True, editable = False)
    end = models.CharField(max_length = 200, null = True, editable = False)

    def getDistance(self):
        distance = self.startPlace.distance(self.endPlace)
        print((self.startPlace[1], self.startPlace[0]), (self.endPlace[1], self.endPlace[0]))
        return geopy.distance.geodesic((self.startPlace[1], self.startPlace[0]), (self.endPlace[1], self.endPlace[0])).km

    def save(self, *args, **kwargs):
        self.routeLength = self.getDistance()
        self.point = int(self.routeLength*10)
        self.start = geolocator.reverse((self.startPlace.y, self.startPlace.x)).address
        self.end = geolocator.reverse((self.endPlace.y, self.endPlace.x)).address
        self.user.wallet += self.point
        self.user.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.name} from {self.start} to {self.end}, length = {self.routeLength} km, get {self.point} points."


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField("Population 2005")
    fips = models.CharField("FIPS Code", max_length=2, null=True)
    iso2 = models.CharField("2 Digit ISO", max_length=2)
    iso3 = models.CharField("3 Digit ISO", max_length=3)
    un = models.IntegerField("United Nations Code")
    region = models.IntegerField("Region Code")
    subregion = models.IntegerField("Sub-Region Code")
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

@receiver(pre_delete, sender = Record, dispatch_uid = 'record_delete_signal')
def delete_record_point(sender, instance, using, **kwargs):
    print(type(instance))
    instance.user.wallet -= instance.point
    instance.user.save()

# Auto-generated `LayerMapping` dictionary for WorldBorder model
worldborders_mapping = {
    "fips": "FIPS",
    "iso2": "ISO2",
    "iso3": "ISO3",
    "un": "UN",
    "name": "NAME",
    "area": "AREA",
    "pop2005": "POP2005",
    "region": "REGION",
    "subregion": "SUBREGION",
    "lon": "LON",
    "lat": "LAT",
    "geom": "MULTIPOLYGON",
}
