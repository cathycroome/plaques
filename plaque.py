import numpy as np
import pandas as pd
from pathlib import Path
from pandas import DataFrame

T = pd.read_csv('/Users/cathycroome/code/open-plaques-United-Kingdom-2025-12-14.csv')

MONTH_ANGLES = {
    'January':   (60, 90),
    'February':  (30, 60),
    'March':     (0, 30),
    'April':     (330, 360),
    'May':       (300, 330),
    'June':      (270, 300),
    'July':      (240, 270),
    'August':    (210, 240),
    'September': (180, 210),
    'October':   (150, 180),
    'November':  (120, 150),
    'December':  (90, 120),
}

def cartesian_to_polar(x, y):
    """
    Convert Cartesian coordinates to polar coordinates.
    Theta is measured anti-clockwise from the positive x-axis, in the range [0, 2*pi).
    """
    r = np.sqrt(x**2 + y**2)
    t = np.arctan2(y, x)  # radians, range (-pi, pi]

    # if y >= 0: quadrant 1 or 2, angle is already correct
    # if y < 0:  quadrant 3 or 4, add 2*pi to wrap into [0, 2*pi)
    theta = np.where(y >= 0, t, 2 * np.pi + t)

    theta_deg = np.degrees(theta)

    return r, theta_deg

def relative_location(lat,long, centre_lat = 53.4153, centre_long=-2.2127):
    """
    Return (x, y) offset of a point from a fixed centre point,
    in degrees of longitude/latitude (not true distance).
    """
    dx_deg = long - centre_long
    dy_deg = lat - centre_lat

    return dx_deg, dy_deg

def degrees_to_km(dx_deg, dy_deg, lat, km_per_degree = 111.0):
    """
    Convert a (dx_deg, dy_deg) offset into approximate (x_km, y_km),
    used to correct for longitude lines converging away from the equator.
    """
    lat_rad = np.radians(lat)
    x_km = dx_deg * km_per_degree * np.cos(lat_rad)
    y_km = dy_deg * km_per_degree
    
    return x_km, y_km

def get_filtered_data(T):
    # format data frame
    subset = T[['id', 'lead_subject_name', 'latitude', 'longitude',  'area',  'colour', 'inscription']].copy()
    subset = subset.dropna(subset=['latitude', 'longitude', 'lead_subject_name', 'colour'])

    # calculate r and theta and append to data frame
    dx_deg, dy_deg = relative_location(subset.latitude, subset.longitude)   # change in lat and long relative to set centre point
    x, y = degrees_to_km(dx_deg, dy_deg, subset.latitude)                   # convert to cartesian (approximate distances in km)
    km, theta_deg = cartesian_to_polar(x,y)                                 # convert to polar
    subset['km'] = km                                                       # approximate distances in km
    subset['theta_deg'] = theta_deg

    return subset

def get_plaques_for_month(month: str, df: DataFrame, max_distance, blue_only = False):
    low, high = MONTH_ANGLES[month]
    df = df[(df['theta_deg'] > low) & (df['theta_deg'] <= high) & (df['km'] < max_distance)]

    if blue_only:
        df = df[df['colour'] == 'blue']

    df = df.sort_values('km', ascending=True)

    return df

def random_plaque(matches: DataFrame):
    if matches.empty:
        return None

    return matches.sample(1).iloc[0]




# matches = get_plaques_for_month(month, subset, max_distance, False)

# # Get random result for a given month
# randomised_result = random_plaque(matches)
