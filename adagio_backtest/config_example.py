import os

QUANDL_TOKEN = "YOUR_QUANDL_TOKEN"
FRED_API_KEY = "YOUR_FRED_API_KEY"
ARCTIC_HOST = "localhost"

ROOT_DIRECTORY = os.path.abspath(os.path.join(os.getcwd(), os.path.pardir))
OUTPUT_LOG = "{}/output/log/".format(ROOT_DIRECTORY)
DATA_DIRECTORY = "{}/data/".format(ROOT_DIRECTORY)
