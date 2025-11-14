from utils.constants import GEE_PROJECT_NAME

from pathlib import Path

import ee
import xarray as xr

def authenticate_ee():
    """
    Authenticates the Earth Engine API.
    """
    ee.Authenticate()
    ee.Initialize(project=GEE_PROJECT_NAME, opt_url='https://earthengine-highvolume.googleapis.com')

    return

def request_gee_image(ee_path: str, date: str|None=None, date_end: str|None=None, bbox: list=None) -> ee.ImageCollection:

    dataset_ic = ee.ImageCollection(ee_path)

    if date and date_end:
        date = ee.Date(date)
        date_end = ee.Date(date_end)
        dataset_ic = dataset_ic.filter(ee.Filter.date(date, date_end))
    
    if bbox:
        bbox_fc = ee.Geometry.Rectangle([bbox[:2], bbox[2:]])
        dataset_ic = dataset_ic.filter(ee.Filter.bounds(bbox_fc))

    return dataset_ic

def get_utm_crs(bbox: list) -> str:
    """
    Calculates the most appropriate UTM CRS EPSG code for a given bounding box.

    Args:
        bbox: A list containing the bounding box coordinates in the format
              [min_lon, min_lat, max_lon, max_lat].

    Returns:
        A string representing the EPSG code of the appropriate UTM zone,
        e.g., "EPSG:32630".
    """
    if not (isinstance(bbox, list) and len(bbox) == 4):
        raise ValueError("Bounding box must be a list of four numbers.")

    # Calculate the centroid of the bounding box
    center_lon = (bbox[0] + bbox[2]) / 2
    center_lat = (bbox[1] + bbox[3]) / 2

    # Calculate the UTM zone number
    # Zones are 6 degrees wide, starting from 180 degrees West
    utm_zone = int((center_lon + 180) // 6) + 1

    # Determine if it's Northern or Southern hemisphere
    # The base EPSG codes for UTM are 326xx for North and 327xx for South
    epsg_base = 32600 if center_lat >= 0 else 32700

    # Combine the base and zone to get the final EPSG code
    epsg_code = epsg_base + utm_zone

    return f"EPSG:{epsg_code}"
