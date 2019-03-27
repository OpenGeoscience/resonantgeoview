from setuptools import setup, find_packages

setup(name='resonantgeoview_server',
    version='0.0.1',
    description='',
    url='',
    install_requires=[
        'girder>=3.0.0a1',
        'girder_worker',
        'girder_worker_utils',
        'girder-plugin-geometa',
        'girder-plugin-geometa-vector',
        'girder-plugin-geometa-raster',
        'large_image',
        'shapely'
    ],
    extras_require={
        'worker': [
        # TODO: gaia
        ]
    },
    include_package_data=True,
    author='Kitware Inc',
    author_email='',
    license='',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: Apache Software License'
        'Topic :: Scientific/Engineering :: GIS',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python'
    ],
    entry_points={
        'girder.plugin': [
            'resonantgeoview_server = resonantgeoview_server:GirderPlugin'
        ],
        'girder_worker_plugins': [
            'gaia_task = gaia_task:GaiaTasks',
        ],
        'geometa.types': [
            'obj=geometa_OBJ_handler.schema:handler'
        ]
    },
    packages=find_packages(exclude=['tests*', 'server*', 'docs']),
    zip_safe=False)
