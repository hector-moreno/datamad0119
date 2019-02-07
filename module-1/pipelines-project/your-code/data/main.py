# Realizamos la importaciones que necesitaremos a lo largo del proyecto

import numpy as np
import pandas as pd
import re
import seaborn as sns
import argparse
import subprocess

# Importamos el archivo csv

dfApp = pd.read_csv('googleplaystore.csv', encoding = "utf-8")



dfReview = pd.read_csv('googleplaystore_user_reviews.csv', encoding = "utf-8")

#DATA CLEANING

# Limpiamos la columna Size y dejamos todas las medidas en MB

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

print(dfApp.head())

#Comprobamos que los datos son del tipo necesario para operar con ellos
print(dfApp.dtypes)

#Calculamos la correlación entre las columnas 'Rating' y 'Size'
corrmat = dfApp.corr()
def correlacion():
    return corrmat
print(corrmat)

#Partíamos de la hipótesis que el Rating de las Apps estaba relacionado con su Size.
# Aplicamos la correlación entre ambas columnas y comprobamos que la hipótesis es errónea.
# Como refleja el siguiente gráfico:

#f, ax = plt.subplots()
p =sns.heatmap(corrmat, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))

print(p)

# Exporting DataFrame
export = dfApp.to_csv('../output/dfApp.csv', index=False)




'''
parser = argparse.ArgumentParser(description="Google Play data set analysis")

parser.add_argument('action', help='La acción ejemplo)')
parser.add_argument('foo-bar', help='Ejemplo de argparse')

args = parser.parse_args()

if args.action == "install":
    print("You asked for installation")
else:
    print("You asked for something other than installation")

# The following do not work:
# print(args.foo-bar)
# print(args.foo_bar)

# But this works:
print(getattr(args, 'foo-bar'))


'''

def reportTo(nombre, email):
    texto = "Reportando a {}".format(nombre)

    # Send the report via mail
    mailCmd = 'echo "{}" | mail -s "New Report" "{}"'.format(texto,email)
    subprocess.Popen(['/bin/bash', '-c', mailCmd])

print("Sent report to mail {}".format(email))




parser = argparse.ArgumentParser(description='Google dataset analysis .')

parser.add_argument('-g', '--graph',  type = int, help='a correlation graph')

parser.add_argument('-r', '--result', type = int, help = 'correlation result')

parser.add_argument('-n', dest='nombre', default="Pepe", help='your name')

parser.add_argument('-e', dest='email', default="escribeun@email", help='your

args = parser.parse_args()




if __name__ == '__main__':
    correlacion = correlacion()    
    #reportTo(args.nombre, args.email)
    '''
    df = acquire()
    dfwrang = wrangle(df)
    dfApp = cleaning(dfwrang)
    SizeRating = analyze(dfApp)
    #barchart = visualize(finalData, tit)
    ''' 