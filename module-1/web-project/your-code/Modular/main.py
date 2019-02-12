# Importamos los módulos necesarios.
from functions import get_externalCode
from functions import dataF
from functions import export_csv
from functions import listCol
import requests
import json
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
from bs4 import BeautifulSoup

# Hacemos una llamada para obtener el json.

url = 'https://www.quandl.com/api/v3/datasets/WIKI/AAPL.json'

response = get_externalCode(url)

results = response.json()

data = dataF(results)

datel = []
openl = []
highl = []
lowl = []
closel = []
resultl = []
dict_cotiz = listCol(data['dataset'][3][:1185], datel, openl, highl, lowl, closel)


df_cotiz = dataF(dict_cotiz)

dfcsv = export_csv(df_cotiz, 'Cotiz')

# SCRAPING DE LA WEB DE FINANCIAL TIMES

url2 = 'https://www.ft.com/stream/a39a4558-f562-4dca-8774-000246e6eebe?format=&page=' 

# Hacemos Parsing del HTML para conseguir la info necesaria: los titulares diarios del FT sobre Apple.

dates = []
headlines = []
for i in range(16,143): 
    path = url2 + str(i)
    html = requests.get(path).content
    soup = BeautifulSoup(html, "lxml")
    text = soup.find_all('li',{'class':'o-teaser-collection__item o-grid-row'})
    for i in soup.findAll('time'):
        if i.has_attr('datetime'):
            dates.append(i['datetime'][0:10])
    for i in soup.find_all('a',{'class':'js-teaser-heading-link'}):
        headlines.append(i.text)

dfHead = dataF({'Date': dates, 'Titulares' : headlines})

dfHead = dfHead.groupby('Date', sort=False, as_index=False).agg({'Titulares': '| '.join})

dfHeadCsv = export_csv(dfHead,'Head')

dfConcat = pd.concat([df_cotiz, dfHead], axis=1, join_axes=[df_cotiz.index])

dfConcatCsv = export_csv(dfConcat, 'Concat')
