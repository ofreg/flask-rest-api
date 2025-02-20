from setuptools import setup, find_packages

setup(
    name='rest_api',              
    version='0.1',                
    packages=find_packages(),     
    install_requires=[            
        'Flask',
        'marshmallow',
    ],
    python_requires='>=3.6',       
)
