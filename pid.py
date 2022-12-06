import time
import json
import nvector as nv
from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

from datetime import datetime

from deepen import DeepenClient


def getProjection(lat, lon):
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=lon,
            south_lat_degree=lat,
            east_lon_degree=lon,
            north_lat_degree=lat,
            ),
            )
    return utm_crs_list[0].code

def main():

    #TODO: get file name from user
    f = open('CoordsFileWise.json')
    data = json.load(f)
    gps = []
    times = []
    for i in data:
        times.append(i["timestamp"])
        gps.append(i)
    
    seconds = []
    for i in range(0, len(times)-1):
        dt1 = datetime.fromtimestamp(times[i])
        dt2 = datetime.fromtimestamp(times[i+1])
        dlt = dt2 - dt1
        print(dlt.total_seconds())
        seconds.append(dlt.total_seconds())
    f.close()

    projection_val = "EPSG:"+getProjection((gps[0])["latitude"], (gps[0])["longitude"])

    ORIGIN = ((gps[0])["longitude"], (gps[0])["latitude"], 0.0) 
    client = DeepenClient(srid=projection_val, origin=ORIGIN)
   

    client.confirmConnection()
    client.enableApiControl(True)
    print("API Control enabled: %s" % client.isApiControlEnabled())
    move = True
    idx = 0
    #initalize kp,ki,  kd, 
    kp = 0.07
    ki = 0.0001
    kd = 1.40625
    client.PID(kp, ki, kd)

    start = time.time()
    client.move()
    while move:
        if(idx <  len(gps)-1):
            current_lat = (gps[idx])["latitude"]
            current_lon = (gps[idx])["longitude"] 
            next_lat = (gps[idx+1])["latitude"]
            next_lon = (gps[idx+1])["longitude"] 
            client.getCTEFromGPS(current_lat, current_lon, next_lat, next_lon)

            time.sleep(0.4)
            idx +=1
        else:
            move = False 
    client.applyBrake()
    print('Execution time:', time.time() -start, 'seconds')
    print("END")

if __name__ == '__main__':
    main()