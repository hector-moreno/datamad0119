
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

def acqData(csv):

    df = pd.read_csv('googleplaystore.csv', encoding = "utf-8")
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
    while True:
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
                print(col2)
            else:
                raise ValueError ("It looks bad! Try again") 
        
        except:
            print ("INCORRECT input")
            
    # realización de la correlación.

        return dfApp[col1].corr(dfApp[col2])


# DATA CONCLUSIONS
'''
    Partíamos de la hipótesis que el Rating de las Apps estaba relacionado con su Size.
    Aplicamos la correlación entre ambas columnas y comprobamos que la hipótesis es errónea.
    Como refleja el siguiente gráfico:
'''
def Visual(dfApp):
    correl = dfApp.corr()
    graph =sns.heatmap(correlmat, annot=True, cmap=sns.diverging_palette(220, 20, as_cmap=True))
    return graph


# DATA REPORT

# Exporting DataFrame

def expData(dfApp):
    export = dfApp.to_csv('../output/dfApp.csv', index=False)
    return export



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
# Generamo la función para reportar

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

parser.add_argument('-e', dest='email', default="escribeun@email", help='your

args = parser.parse_args()




if __name__ == '__main__':
    dataAcqu = acqData(csv)
    dataWra = wraData(dfApp)
    dataAna = toInput(dfApp)
    dfApp = cleaning(dfwrang)
    dataVis = Visual(dfApp)
    dataRep = reportTo(args.nombre, args.email)
    
 
