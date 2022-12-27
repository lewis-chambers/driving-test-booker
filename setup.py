from setuptools import setup, find_packages

setup(name='Driving Test Booker',
      version='1.0',
      description='Application to reserve and hold a driving test',
      author='Lewis Chambers',
      author_email='lewis.n.chambers@gmail.com',
      packages=find_packages(),
      install_requires=[
        "selenium",
        "bs4",
        "undetected-chromedriver",
        "python-dotenv",
        "numpy"
      ]
     )