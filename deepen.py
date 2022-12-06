from pyproj import Proj
import json
from airsim import CarClient
import airsim
import numpy as np
import nvector as nv

class DeepenClient(CarClient):
    def __init__(self, srid, origin, **kwargs):
        self.srid = srid
        self.origin = origin
        self.proj = Proj(init=srid)
        self.origin_proj = self.proj(*self.origin[0:2]) + (self.origin[2],)
        self.frame = nv.FrameE(a=6371e3, f=0)
        super(DeepenClient, self).__init__(**kwargs)

    def lonlatToProj(self, lon, lat, z, inverse=False):
        proj_coords = self.proj(lon, lat, inverse=inverse)
        return proj_coords + (z,)

    def projToAirSim(self, x, y, z):
        x_airsim = x - self.origin_proj[0]
        y_airsim = y - self.origin_proj[1]
        z_airsim = -z + self.origin_proj[2]
        return (x_airsim, -y_airsim, z_airsim)

    def lonlatToAirSim(self, lon, lat, z):
        return self.projToAirSim(*self.lonlatToProj(lon, lat, z))

    def nedToProj(self, x, y, z):
        """
        Converts NED coordinates to the projected map coordinates
        Takes care of offset origin, inverted z, as well as inverted y axis
        """
        x_proj = x + self.origin_proj[0]
        y_proj = -y + self.origin_proj[1]
        z_proj = -z + self.origin_proj[2]
        return (x_proj, y_proj, z_proj)

    def nedToGps(self, x, y, z):
        return self.lonlatToProj(*self.nedToProj(x, y, z), inverse=True)


    def getGpsLocation(self):
        """
        Gets GPS coordinates of the vehicle.
        (Lat, Lon, Alt)
        """
        pos = self.getCarState().kinematics_estimated.position
        gps = self.nedToGps(pos.x_val, pos.y_val, pos.z_val)
        return gps

    def convertGPSpoints(self, gpsPoints, **kwargs):
        self.Airsim_coor = []
        for point in gpsPoints:
            coords = self.lonlatToAirSim( point['longitude'], point['latitude'], 0.0)
            self.Airsim_coor.append(coords)
        return point


    def export_to_json(self):
        json_object = json.dumps(self.Airsim_coor)
        with open("output.json", "w") as outfile:
            outfile.write(json_object)

    def move(self):
        self.car_state = self.getCarState()
        self.car_controls = airsim.CarControls()
        self.car_controls.throttle = 0.5
        self.setCarControls(self.car_controls)
    
    def applyBrake(self):
        self.car_controls.brake = 1
        self.setCarControls(self.car_controls)
    
    def getCTEFromGPS(self, current_lat, current_lon, next_lat, next_lon):
        current_pos = self.getGpsLocation()
        pointA1 = self.frame.GeoPoint(current_lat, current_lon, degrees=True)
        pointA2 = self.frame.GeoPoint(next_lat, next_lon, degrees=True)
        pointB = self.frame.GeoPoint(current_pos[1], current_pos[0], degrees=True)
        pathA = nv.GeoPath(pointA1, pointA2)
        self.cte = pathA.cross_track_distance(pointB, method='greatcircle')
        self.updateError()
        self.steer_value = self.totalError()
        #steering
        self.car_controls.steering = self.steer_value
        self.setCarControls(self.car_controls)
    
    def PID(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.p_error = 0
        self.i_error = 0
        self.d_error = 0
    
    def updateError(self):
        self.d_error = self.cte - self.p_error
        self.p_error = self.cte
        self.i_error += self.cte

    def totalError(self):
        return -self.kp * self.p_error - self.ki * self.i_error - self.kd * self.d_error