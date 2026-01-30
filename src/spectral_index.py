from ee import ImageCollection

import ee
import xarray as xr


def extract_imagery(imagery_ic: ImageCollection, bbox: list, utm_crs: str, scale: int) -> xr.DataArray:

    bbox_fc = ee.Geometry.Rectangle([bbox[:2], bbox[2:]])

    ic_ds = xr.open_dataset(imagery_ic, engine="ee", geometry=bbox_fc, scale=scale, crs=utm_crs)
    ic_ds = ic_ds.ffill(dim='time').bfill(dim='time').isel(time=0).drop_vars('time')
    ic_ds = ic_ds.rename({'Y': 'y', 'X': 'x'}).rio.set_spatial_dims(x_dim='x', y_dim='y')

    ic_da = ic_ds.to_dataarray().transpose('variable', 'y', 'x')

    return ic_da

def calculate_lst(image,):
    
    thermal = image.select('ST_B10')
    lst = thermal.multiply(0.00341802).add(149.0).add(-273.15).rename('LST')
    
    return lst

def get_sample_info(feature):
    return ee.Feature(feature.geometry(), {
        'LST': feature.get('LST'), 
        'NDVI': feature.get('NDVI'), 
        'NDBI': feature.get('NDBI'),
        'lat': feature.geometry().coordinates()[1],
        'lon': feature.geometry().coordinates()[0]
    })