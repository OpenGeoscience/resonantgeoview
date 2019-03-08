from functools import partial
import os
import tempfile

from girder_worker.app import app
from girder_worker.utils import girder_job


def getTempFileName():
    tempName = next(tempfile._get_candidate_names())
    return os.path.join(tempfile.tempdir, tempName)


def getTempGeojsonFileName(name=None):
    tempName = name if name else next(tempfile._get_candidate_names())
    # print tempName
    return os.path.join(tempfile.tempdir, tempName + '.geojson')


def copy(input, output):
    # print input
    # print output
    with open(input) as f:
        with open(output, "w") as f1:
            for line in f:
                f1.write(line)
    return output


@girder_job(title='Crop Task')
@app.task(bind=True)
def crop_task(self, target_file, by_file, name):
    import gaia
    from gaia import preprocess

    target_file = copy(target_file, getTempGeojsonFileName())
    by_file = copy(by_file, getTempGeojsonFileName())

    # Load 2 datasets
    target = gaia.create(target_file)
    by_file = gaia.create(by_file)

    # Apply crop
    print('Before crop', target.get_data().shape)
    cropped = preprocess.crop(target, by_file)
    # print('After crop', cropped.get_data().shape)
    # print(cropped.get_data().head())
    # print cropped.get_data().to_json()

    tempName = getTempGeojsonFileName(name)
    with open(tempName, 'w') as f:
        f.write(cropped.get_data().to_json())

    return tempName
