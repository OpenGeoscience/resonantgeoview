from setuptools import setup, find_packages

setup(name='gaia_tasks',
    version='0.0.1',
    description='',
    url='',
    install_requires=[
        'girder_worker',
        'girder_worker_utils',
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
        'girder_worker_plugins': [
            'gaia_tasks = gaia_tasks:GaiaTasks',
        ]
    },
    packages=find_packages(exclude=['tests*', 'server*', 'docs']),
    zip_safe=False)
