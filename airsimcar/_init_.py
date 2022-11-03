

class AirSimCarClient:
    def _init_(self, srid, origin_coordinate, **kwargs):
        #TODO: asma
    def lonlatToProj(self, lon, lat, z, inverse=False):
        #TODO: BO
    def projToAirSim(self, x, y, z):
        #TODO:BO
    def lonlatToAirSim(self, lon, lat, z):
         #TODO:BO
    def nedToProj(self, x, y, z):
        #TODO:Bo
     def nedToGps(self, x, y, z):
        #TODO:BO
    def getGpsLocation(self):
        #TODO:BO
    def moveToPositionAsyncGeo(self, gps=None, proj=None, **kwargs):
        #TODO: Julie
    def moveOnPathAsyncGeo(self, gps=None, proj=None, velocity=10, **kwargs):
        #TODO: Julie

