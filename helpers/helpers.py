"""
This file holds some useful functions that I frequently use
"""

def gcd(lon0: float, lat0: float,
        lon1: float, lat1: float,
        rad_earth = 6378137):
    """
    calculates the great circle distance between 2 coordinate pairs
    INPUTS: lat/lon of two points, in degrees
            rad_earth is radius of Earth, in meters
    OUTPUTS: distance between points, in meters as float
    """ 
    from sklearn.metrics.pairwise import haversine_distances
    from math import radians, atan2, cos, sin
    import numpy as np
    
    point_1 = np.array([lat0,lon0])
    point_2 = np.array([lat1,lon1])
    point1_in_radians = [radians(_) for _ in point_1]
    point2_in_radians = [radians(_) for _ in point_2]
    result = haversine_distances([point1_in_radians, point2_in_radians])
    # multiply by Earth radius to get kilometers and reformat to 1 value
    
    # Get azimuth
    phi1   = point1_in_radians[0]
    phi2   = point2_in_radians[0]
    dlon   = radians(point_2[-1]-point_1[-1]);
    y      = sin(dlon) * cos(phi2);
    x      = cos(phi1) * sin(phi2) - \
             sin(phi1) * cos(phi2) * cos(dlon);
    theta  = atan2(y, x);
    az_    = float(theta*180./np.pi)
    
    if az_>360.:
        az_ = az_-360.
    if az_<0.:
        az_0 = az_+360.
    
    return float(np.matmul(result * rad_earth,np.array([[1],[1]]))[0]), az_

# Helpful Functions
def calculate_winds(**kwargs):
    from metpy.calc import wind_direction, wind_speed
    from metpy.units import masked_array
    from numpy import sqrt, log
    u       = kwargs['u_wind_2m'].values**2
    v       = kwargs['v_wind_2m'].values**2
    w       = kwargs['w_wind_2m'].values**2
    z       = kwargs['altitude'].values
    windspd = sqrt(u+v+w)
    z0 = 0.22
    
    # Set any z<z0 to the surface roughness height
    z[z<z0]=z0
    
    uc = masked_array(u, data_units="m/s")
    vc = masked_array(v, data_units="m/s")
    
    # windspd   = wind_speed(uc,vc)
    
    speed     = windspd*(log(z/z0)/log(2./z0))
    direction = wind_direction(uc,vc)
    
    return speed, direction
