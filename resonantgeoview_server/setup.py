import re
from setuptools import setup, find_packages

setup(name='resonantgeoview_server',
      version='0.0.0.dev1',
      description='',
      url='',
      install_requires=[
          'girder_worker',
          'girder_worker_utils'
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
              'gaia_task = gaia_task:GaiaTasks',
          ]
      },
      packages=find_packages(exclude=['tests*', 'server*', 'docs']),
      zip_safe=False)
