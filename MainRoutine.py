
"""

This is the Main Python function that will be used to scrape the data from the website.
We are looking in particular, for careers, given a large list of firms that I want to work at

Code by Zan Jia Tan, 2024
Contact: tanzanjia98@tanzanjia98@gmail.com

"""





import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from tqdm import tqdm
from Functions import LoadingFunctions as lf



###################
#                 #
#   Loading in    #
#   the data      #
#                 #
###################


# call the loading functions

lf.main_loading_function()



