
# Importaciones necesarias

import pymongo

import pandas as pd


#########                                                                       #######
#########   FUNCIONES PARA TRANSFORMACION DEL DOCUMENTO DE CADA COMPAÑÍA        #######
#########                                                                       #######


# Creación de toGeoJSON:
    # Input: lista con dos valores: la longitud y la latitud de la ubicación de la compañía.
    # Output: diccionario con ambas coordenadas en una sola lista y el establecimiento de "type".
    
def toGeoJSON(lista):
    return {
            "type": "Point",
            "coordinates":[lista[1],lista[0]]
        }

# Creación de toGeoJSON:
    # Input: lista co los valores de las rondas de inversión.
    # Output: entero con el total del valor de la inversión.

def getValuatio(funding_round):
    valor= 0
    for lista in funding_round:
        valor = lista['raised_amount']
    return valor

    

# Creación de company_Document() 
    
    # Input: documento (uno por compañía) tal y como se encuentra en la base de datos original.
    
    # Output: lista_dict: lista con diccionarios con la siguiente información sobre cadaa compañia:
        
        # Name (nombre), category_code (actividad),  number_of_employees (total de empleados),
        # valuation (valor de la compañía: así interpretamos la inversión obtenida en la ronda 
        # de inversiones), city(ciudad y códiigo del país de ubicación) y position (coordenadas). 
        
        # Para conseguir el valor de position usamos las función toGeoJso() anteriormente definida.
        
        # Para conseguir el valor de valuation usamos las función getValuatio() anteriormente definida.
        
def companyDocument(company):
    lista_dict = [
                {
                "name": company["name"],
                "category_code": company["category_code"],
                "number_of_employees": company["number_of_employees"],
                "founded_year": company["founded_year"],
                "valuation": getValuatio(company['funding_rounds']),
                "city": (key["city"],  key["country_code"]),  
                "position": toGeoJSON([key['latitude'],key['longitude']])   
                }
    for index in range(len(company['offices'])) for key in company['offices'] \
    if key['latitude'] != None and key['longitude'] != None
                ]
                
    return lista_dict
