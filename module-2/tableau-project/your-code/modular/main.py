
##### CASO PRÁCTICO DE BUSINESS INTELLIGENT ######

# OBJETIVO: encontrar la ubicación más adecuada, en todo el mundo, para la siguiente empresa:

    # Actividad: videojuego
    
    # Compañía de 50 empleados.
        # 20 desarrolladores
        # 20 diseñadores creativos
        # 10 ejecutivos 

    # Condiciones: 
        # Entorno con buen ratio entre grandes compañías y startups.
        # Entorno que cubra intereses de eqipo: 
            # empresas de diseño
            # empresas de desarrollo
            # consultoras y empresas para hacer negocio
        # Evitar compañías muy viejas
        
    # Estrategia
        # 1ª Realizamos un filtrado desde la base de datosque elimine:
            # Empresas sin información sobre ubicación
            # Empresas creadas anteriormente a 1996.
        
        # 2ª Asignamos un rating a cada empresa en función de:
            # Su número de empleados.
            # Su valor.
            # Su antigüedad.
            # Su actividad.
        
        # 3ª Seleccionamos la compañía con mejor ubicación en función del rating
        # de las empresas de su entorno (radio de 10 km).



if __name__ == '__main__':


  # Importamos los módulos necesarios.

  from functions_transf import toGeoJSON
  from functions_transf import getValuatio
  from functions_transf import companyDocument

  from functions_rating import rating
  from functions_rating import getAreasRat


  import pymongo
  import pandas as pd


  # Realizamos la llamada a Mongoclient

  MongoClient = pymongo.MongoClient

  # Asignamos MongoClient() a la variable client 

  client = MongoClient()

  # La variable db se encargará de hacer la llamada a la base de datos companies

  db = client.companies



  # A la variable filtered_comp, asignamos el filtrado de documentos de empresas que nos interesan:
      
      # que contengan las coordenadas: tanto latitud como longitud.
      
      # que hayan sido creadas con posterioridad a 1995,(las anteriores las 	    consideramos antiguas)
      
      # que no hayan desaparecido.

  # Por último nos aseguramos de extraer el id de cada documento.
      
  filtered_companies = db.companies.find(
                      {"$and": [ 
                          { "offices.latitude": {"$exists": True} },
                          { "offices.longitude": {"$exists": True} }, 
                          { "founded_year": {"$gt": 1995} }, 
                          {"deadpooled_year": None}  
                              ]},
                      {"_id":0})


  # Damos la forma y el contenido que nos interesa a los documentos que almacena filtered_companies:
      
          # Aplicamos companyDocument() (definida arriba) a cada documento.
          
          # y almacenamos cada documento (diccionario) en una lista, companies_docs 

  companies_docs = list(map(lambda r: companyDocument(r),filtered_companies))

  # Agrupamos todos los diccionarios de companies_docs en una sola lista.

  geoCompanies = [element for lista in companies_docs for element in lista]



  # Creamos un dataframe con los valores de geoCompanies.

  df = pd.DataFrame(geoCompanies)

  df.head()


  # Ejecutamos rating() sobre el df y asignamos los valores obtenidos a rating.

  rating = rating(df)


  # Creamos una nueva columna 'rating' en df con la puntuación obtenida por cada empresa.

  df['rating'] = rating

  df.head()


  # A partir de df generamos un nuevo data son con el que crearemos las colección 'location'

  df.to_json("comp_with_coords.json", orient="records", lines=True)


  # En companies almacenamos los diccionarios de cada compañía con su rating incorporado.

  companies = list(db.location.find({}))

  # Generamos un dataframe con los valores de companies

  dfRating = pd.DataFrame(companies)



  # Ejecutamos getAreasRat() y almacenamos los valores en listOfRating

  listOfRating = getAreasRat(companies)


  # Añadimos listofRating al df para añadir el valor del área de cada compañía

  dfRating['area_rating'] = listOfRating
  dfRating.head()




  # Preparamos el df para la posterior lectura de las coordenadas en Tableau.

  # Primero generamos un df con una columna para longitud y otro para latitud.

  coords_df = pd.DataFrame(pd.DataFrame(dfRating["position"].values.flatten().tolist())["coordinates"]
              .values.tolist())

  # Unimos dfRating con el df de las coordeenadas.
  clean_df = pd.concat([dfRating,coords_df],axis=1)

  # Eliminamos las columanas que no son útiles.
  clean_df.drop(['_id',"position"], inplace=True, axis=1)

  # Renombramos las columnas de coordenadas.
  clean_df = clean_df.rename({0:"long",1:"lat"}, axis=1)

  clean_df.head()


  # Localizamos la empresa con mejor ubicación

  selected_comp = clean_df.loc[clean_df['area_rating'].idxmax()]
  selected_name = selected_comp['name']
  selected_coord = [selected_comp['long'],selected_comp['lat']]
  

  # Generamos un dataframe definitivo con las datos seleccionados.
  clean_df.to_json('visualize_location.json', orient="records")



  selectedArea = db.location.find({
            "position": {
              "$near": {
                "$geometry": {
                  "type": "Point",
                  "coordinates": selected_coord
                },
                "$minDistance": 0,
                "$maxDistance":10000
              }
            }
          })



  dfSelected = pd.DataFrame(list(selectedArea))

  coords_df_selec = pd.DataFrame(pd.DataFrame(dfSelected["position"].values.flatten().tolist())["coordinates"].values.tolist())
  clean_df_selec = pd.concat([dfSelected,coords_df_selec],axis=1)
  clean_df_selec.drop(['_id',"position"], inplace=True, axis=1)
  clean_df_selec = clean_df_selec.rename({0:"long",1:"lat"}, axis=1)
  clean_df_selec.head()


  clean_df_selec.to_json('visualize_selected_location.json', orient="records")



