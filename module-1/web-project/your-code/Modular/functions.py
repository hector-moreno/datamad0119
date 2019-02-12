import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
from bs4 import BeautifulSoup

def get_externalCode(url):
    response = requests.get(url)
    return response


def dataF(content):
    dataFrame = pd.DataFrame(content)
    return dataFrame

def export_csv(dataframe, i=''):
    dfcsv = dataframe.to_csv('dataframe' + i + '.csv')
    return dfcsv


def listCol(list, sublist1, sublist2, sublist3, sublist4, sublist5):
    for element in list:
        sublist1.append(list[0])
        sublist2.append(list[1])
        sublist3.append(list[2])
        sublist4.append(list[3])
        sublist5.append(list[4])
    
    dict_selec = {'sublist1': sublist1, 'sublist2' : sublist2, 'sublist3' : sublist3, 'sublist4' : sublist4, 'sublist5' : sublist5}   
    
    return dict_selec

