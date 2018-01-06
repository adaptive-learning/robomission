from glob import glob
import os
from setuptools import setup
from setuptools.command.develop import develop as _develop
from notebook.nbextensions import install_nbextension
from notebook.services.config import ConfigManager

extension_dir = os.path.join(os.path.dirname(__file__), "robomission", "static")

class develop(_develop):
    def run(self):
        _develop.run(self)
        install_nbextension(
            extension_dir,
            symlink=True,
            overwrite=True,
            user=False,
            sys_prefix=True,  # to install it inside virtualenv
            destination="robomission")
        cm = ConfigManager()
        cm.update('notebook', {"load_extensions": {"robomission/index": True } })

setup(
    name='robomission',
    cmdclass={'develop': develop},
    version='0.0.4',
    description='Visualization components for RoboMission',
    url='https://github.com/adaptive-learning/robomission',
    author='Tomas Effenberger',
    author_email='xeffenberger@gmail.com',
    license='MIT',
    packages=['robomission'],
    zip_safe=False,
    include_package_data=True,  # specified in MANIFEST.in
    data_files=[
        ('share/jupyter/nbextensions/robomission', ['robomission/static/index.js']),
        ('share/jupyter/nbextensions/robomission/media', glob('robomission/static/media/*'))
    ],
    install_requires=[
        "ipython",
        "jupyter-react"
    ])
