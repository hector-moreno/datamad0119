import pandas as pd
import numpy as np
import seaborn as sns



def acquire():
    df = pd.read_csv('googleplaystore.csv', encoding = "utf-8")
    
    return df



def wrangle(df):
    
    #Elimino los posibles valores duplicados
    dfwrang = df.drop_duplicates(subset='App', inplace=True)
    return dfwrang

def toMbg(x):
    if 'M' in str(x):
        return str(x).replace('M', '')
    elif 'k' in str(x):
        return float(str(x).replace('k', '')) / 1000
    else:
        return str(x).replace('Varies with device', 'NaN')

def cleaning(dfwrang):
    dfwrang['Size'] = dfwrang['Size'].apply(lambda x: toMb(x))
    dfwrang.loc[(dfwrang['Size']== '1,000+', 'Size')] = str(1)
    dfwrang['Size'] = dfwrang['Size'].apply(lambda x: float(x))
    return dfApp

def analyze(dfApp):
    SizeRating = dfApp['Size'].corr(dfApp['Rating'])
    return SizeRating
'''
def visualize(finalData,title):
    #title = 'test'
    fig, ax = plt.subplots(figsize=(12,10))
    barchart=sns.barplot(data=finalData, x='Month', y='n_killed')
    plt.title(title + "\n", fontsize=16)
    
    return barchart
'''

if __name__ == '__main__':
    df = acquire()
    dfwrang = wrangle(df)
    dfApp = cleaning(dfwrang)
    SizeRating = analyze(dfApp)
    #barchart = visualize(finalData, tit)