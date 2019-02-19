
# Importaciones necesarias

import pandas as pd
import pymongo
MongoClient = pymongo.MongoClient
client = MongoClient()
db = client.companies



#########                                                 #######
#########   FUNCIONES PARA RATING DE CADA COMPAÑÍA        #######
#########                                                 #######

# Creamos rating() para calcular el rating de cada compañía: 

        #Input: df

        #Output: lista con el rating total de cada compañía.

    # Dentro de la rating() creamos cuatro funciones para asignar una putuación a cada empresa por su:
            # Su número de empleados.
            # Su valor.
            # Su antigüedad.
            # Su actividad.
      
            
def rating(df):            
# Creamos getRatingCode() para asignar un rating a cada compañía en función de su actividad
    
    #Input: código de actividad de la compañía
    
    #Output: puntuación por actividad.

    def getRatingCode(code):
        ratingCode = 0
        ratingCode = 5 if code == ("web" or "software" or "hardware" or "design" or "consulting") \
        else ratingCode
        ratingCode = 4 if code == ("advertising" or "games_video" or  "ecommerce") else ratingCode
        ratingCode = 3 if ("network_hosting" or "search" or "cleantech" or "analytics" or "messaging") \
        else ratingCode
        ratingCode = 2 if ("mobile" or "public_relations"  or "finance" or "fashion") else ratingCode
        ratingCode = 1 if ("biotec" or "security" or "semiconductor" or "education" or "medical" 
                           or "health" or "manufacturing" or "nanotech" or "social" or "music" 
                           or "news" or "travel" or "photo_video") else ratingCode
        return ratingCode


    # Creamos getRatingFunds() para asignar un rating a cada compañía en función de su valor:

        #Input: valor de la compañía

        #Output: puntuación por valor.


    def getRatingFunds(funds):
        ratingFunds = 0
        ratingFunds = 5 if funds >= 100000000 else ratingFunds
        ratingFunds = 4 if funds >= 8000000 and funds < 100000000 else ratingFunds
        ratingFunds = 3 if funds >= 3000000 and funds < 8000000 else ratingFunds
        ratingFunds = 2 if funds >= 1500000 and funds < 3000000 else ratingFunds
        ratingFunds = 1 if funds >= 500000 and funds < 1500000 else ratingFunds
        return ratingFunds



    # Creamos getRatingEmpl() para asignar un rating a cada compañía en función de su número de empleados:

        #Input: número de empleados de la compañía

        #Output: puntuación por número de empleados.

    def getRatingEmpl(employees):
        ratingEmpl = 0
        ratingEmpl = 5 if employees >= 50000 else ratingEmpl
        ratingEmpl = 4 if employees >= 10000 and employees < 50000 else ratingEmpl
        ratingEmpl = 3 if employees >= 1000 and employees < 10000 else ratingEmpl    
        ratingEmpl = 2 if employees >= 200 and employees < 1000 else ratingEmpl
        ratingEmpl = 1 if employees >= 50 and employees < 200 else ratingEmpl
        return ratingEmpl

    # Creamos getRatingYear() para asignar puntos a la compañía si se trata de una start up:

        #Input: año de fundación de la compañía

        #Output: puntuación por año de la fundación.

    def getRatingYear(year):        
        ratingYear = 0
        ratingYear = 5 if year > 2010 else ratingYear
        return ratingYear    

    return df.number_of_employees.map(getRatingEmpl) + df.valuation.map(getRatingFunds) \




    + df.category_code.map(getRatingCode) + df.founded_year.map(getRatingYear)




# Definimos getAreasRat() para hallar el rating que suman las empresas en un radio
# de 10 km alrededor de una compañía. La empresa con mayor rating en su área, 
# representará las coordenadas elegidas para la ubicación de nuestra empresa.

    # Input: lista de compañías
    
    # Output: lista con el valor de rating del área de cada compañía.

def getAreasRat(companylist):
    areasRating = [sum(i['rating'] for i in list(
        db.location.find({
              "position": {
                "$near": {
                  "$geometry": {
                    "type": "Point",
                    "coordinates": companylist[i]['position']['coordinates']
                  },
                  "$minDistance": 0,
                  "$maxDistance":10000
                }
              }
            })
            ))   for i in range(len(companylist))]
    return areasRating


