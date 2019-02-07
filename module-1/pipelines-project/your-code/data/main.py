
###     OBJETIVO:
'''
     Crear una herramienta para que el usuario investigue la interdependencia 
     entre: el Rating, las Reviews, el Peso, las Instalaciones y el Precio
     de la aplicaciones en la Play Store de Google.
'''

# Realizamos la importaciones que necesitaremos a lo largo del proyecto

import numpy as np
import pandas as pd
import re
import seaborn as sns
import argparse
import subprocess

# DATA ACQUISITION

# Importamos el archivo csv

def acqData():

    dfApp = pd.read_csv('googleplaystore.csv', encoding = "utf-8")
    return dfApp

# DATA WRANGLING

def wraData(dfApp):

    # Eliminamos las columnas duplicadas

    dfApp = dfApp.drop_duplicates()

    # Limpiamos la columna Size para presentar todas las medidas en MB y convertimos a float.

    def toMb(x):
        if 'M' in str(x):
            return str(x).replace('M', '')
        elif 'k' in str(x):
            return float(str(x).replace('k', '')) / 1000
        else:
            return str(x).replace('Varies with device', 'NaN')

    dfApp['Size'] = dfApp['Size'].apply(lambda x: toMb(x))
    dfApp.loc[(dfApp['Size']== '1,000+', 'Size')] = str(1)
    dfApp['Size'] = dfApp['Size'].apply(lambda x: float(x))

    # Limpiamos la columna Installs para poder pasar todos los registros a float.

    dfApp['Installs'] = dfApp['Installs'].apply(lambda x: x.replace('+', '') if '+' in str(x) else x)
    dfApp['Installs'] = dfApp['Installs'].apply(lambda x: x.replace(',', '') if ',' in str(x) else x)
    dfApp['Installs'] = dfApp['Installs'].apply(lambda x: x.replace('Free', '0') if 'Free' in str(x) else x)
    dfApp['Installs'] = dfApp['Installs'].apply(lambda x: int(x))
    dfApp['Installs'] = dfApp['Installs'].apply(lambda x: float(x))

    # Limpiamos la columna Price para poder pasar todos los registros a float.
    
    dfApp['Price'] = dfApp['Price'].apply(lambda x: str(x).replace('$', '') if '$' in str(x) else str(x))
    dfApp['Price'] = dfApp['Price'].apply(lambda x: x.replace('Everyone', '0') if 'Everyone' in str(x) else x)
    dfApp['Price'] = dfApp['Price'].apply(lambda x: float(x))

    # Limpiamos la columna Reviews para poder pasar todos los registros a float.

    dfApp['Reviews'] = dfApp['Reviews'].apply(lambda x: x.replace('3.0M', '3') if '3.0M' in str(x) else x)
    dfApp['Reviews'] = dfApp['Reviews'].apply(lambda x: int(x))

    return dfApp


# DATA ANALYSIS

# Pedimos al usuario que elija las variables a comparar y obtendrá la correlaciónn entre las mismas.

def toInput(dfApp):
    # Solicitud de los input:
    print('Elige el par de elementos que quieres comparar')
    try:
        opciones = ['Rating', 'Reviews', 'Size', 'Installs', 'Price']
        col1 = input('Choose the first: Rating, Reviews, Size, Installs or Price: ')
        if col1 in opciones: 
            print("Correct!!")  

        else:
            raise ValueError ("It looks bad! Try again")

        col2 = input('Choose the second: Rating, Reviews, Size, Installs or Price: ')   
        if col2 in opciones:
            print("Correct!!")
        else:
            raise ValueError ("It looks bad! Try again") 

    except:
        print ("INCORRECT input")

    col_corr = dfApp[col1].corr(dfApp[col2])  
    print('La correlación entre ', col1, 'y ', col2, 'es : ', col_corr)
    
    if col_corr < 0.6 or col_corr > -0.6:
        print('Parece que no es muy significativa esa correlación')
        print('\n')
        print('pero, ¡espera!')
        print('\n')
        print('¿sabes que...?')
        print('\n')
        rating_promedio = np.mean(dfApp['Rating']) 
        print('El rating promedio de las aplicaciones es ', rating_promedio)
        cats_app = len(dfApp['Category'].unique())
        print('\n')
        print('Hay más de ', cats_app, ' categorías de aplicaciones')
        cats = dfApp['Category'].value_counts().sort_values(ascending=False)
        print('\n')
        print('¿Cuáles?', cats)
        print('\n')
        print('Y por último, ya que preguntabas...')
        max_cor = dfApp['Installs'].corr(dfApp['Reviews'])
        print('Las variables que presentan más correlación son Instalaciones y Reviews con un :', max_cor)
    else: 
        print('Has dado con la mayor correlación entre variables!')
        print('pero, ¡espera!')
        print('\n')
        print('¿sabes que...?')
        print('\n')
        rating_promedio = np.mean(dfApp['Rating']) 
        print('El rating promedio de las aplicaciones es ', rating_promedio)
        cats_app = len(dfApp['Category'].unique())
        print('\n')
        print('Hay más de ', cats_app, ' categorías de aplicaciones')
        cats = dfApp['Category'].value_counts().sort_values(ascending=False)
        print('\n')
        print('¿Cuáles?', cats)


    return col_corr

#Pivotamos las columnas 'Category' y 'Type' para conocer mejor los promedios en instalaciones y rating.

def pivDat(dataWra):
    table = pd.pivot_table(dataWra, values=['Rating', 'Installs'], index=['Category', 'Type'], aggfunc={'Rating': np.mean,'Installs': [min, max, np.mean]})
    return table


# DATA CONCLUSIONS
'''
    Partíamos de la hipótesis que el Rating de las Apps estaba relacionado con su Size.
    Aplicamos la correlación entre ambas columnas y comprobamos que la hipótesis es errónea.
    Como refleja el siguiente gráfico:
'''

def Visual(dataWra):
    correl = dataWra.corr()
    graph =sns.heatmap(correl, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))
    return graph


# DATA REPORT

# Exporting DataFrame

def expData(dataWra):
    export = dataWra.to_csv('../output/dfApp.csv', index=False)
    return export



# Generamos la función para reportar

def reportTo(nombre, email):
    texto = "Reportando a {}".format(nombre)

    # Send the report via mail
    mailCmd = 'echo "{}" | mail -s "New Report" "{}"'.format(texto,email)
    subprocess.Popen(['/bin/bash', '-c', mailCmd])

    return mailCmd


# PARSER

parser = argparse.ArgumentParser(description='Google dataset analysis .')

parser.add_argument('-g', '--graph',  type = int, help='a correlation graph')

parser.add_argument('-r', '--result', type = int, help = 'correlation result')

parser.add_argument('-n', dest='nombre', default="Pepe", help='your name')

parser.add_argument('-e', dest='email', default="escribeun@email", help='your')

args = parser.parse_args()




if __name__ == '__main__':
    dataAcqu = acqData()
    dataWra = wraData(dataAcqu)
    dataAna = toInput(dataWra)
    dataVis = Visual(dataWra)
    dataPiv = pivDat(dataWra)
    
 
