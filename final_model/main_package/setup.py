from setuptools import find_packages, setup

REQUIRED_PACKAGES = ['numpy==1.21',
                     'tensorflow==2.8.0',
                     'google-cloud',
                     'google-cloud-storage',
                     'cloudml-hypertune',
                     ]

setup(
    name='magic-autocomplete-training',
    version='1.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    description='Training application for magic-autocomplete.'
)
