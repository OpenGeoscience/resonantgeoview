from functools import partial
import os
from shutil import copyfile
import tempfile

from girder_worker.app import app
from girder_worker.utils import girder_job


def getTempFileNameWithExtention(driver, name=None):
    extension = None
    if driver == 'GeoJSON':
        extension = '.geojson'
    elif driver == 'GeoTIFF':
        extension = '.tif'
    tempName = name if name else next(tempfile._get_candidate_names())
    return os.path.join(tempfile.tempdir, tempName + extension)


@girder_job(title='Crop vector/raster with vector task')
@app.task(bind=True)
def crop_task(self, target_file, target_driver, by_file, name):
    import gaia
    from gaia import preprocess
    target_file = copyfile(target_file, getTempFileNameWithExtention(target_driver))
    by_file = copyfile(by_file, getTempFileNameWithExtention('GeoJSON'))

    target = gaia.create(target_file)
    by_file = gaia.create(by_file)

    cropped = preprocess.crop(target, by_file)

    tempName = getTempFileNameWithExtention(target_driver, name)
    # A bug with geopandas and fiona that throws an error like
    # fiona.errors.GeometryTypeValidationError: Record's geometry type does not match collection schema's geometry type: 'MultiPolygon' != 'Polygon'
    if(target_driver == 'GeoJSON'):
        with open(tempName, 'w') as f:
            f.write(cropped.get_data().to_json())
    else:
        gaia.save(cropped, tempName)

    return tempName
