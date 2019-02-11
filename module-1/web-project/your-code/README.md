![IronHack Logo](https://s3-eu-west-1.amazonaws.com/ih-materials/uploads/upload_d5c5793015fec3be28a63c4fa3dd4d55.png)

# Guided Project: Web -project

## Objetivos

- Generar un data set a partir de la información obtenida de:

    - Una API, en este caso: la de quandl.com
    - Una web, en este caso: ft.com, (Financial Times)

- El propósito de dicho data set es realizar un registro diario (cada día de cotización bursatil será un record):
    * la variación de la cotización de las acciones de Apple (obtenidas de la API) y 
    * los titulares diarios sobre dicha empresa vertidos por uno de los diarios económicos más influyenye: Financial Times.

Con ello, en futuros análisis podremos estudiar la influencia de dicho diario en las cotizaciones de empresas. 


## Actuaciones necesarias sobre los datos de trabajo.


* **Hacer una llamada a la APi seleccionada**.
* Obtener la **respuesta** de dicha API.
* Almacenar los datos en un **DataFrame** y exportarlos a un **csv**.
* **Scraping** de la web seleccionada.
* **Parsing** del HTML para conseguir la info necesaria.
* **Exportar** los resultados a un archivo donde se combinen ambos data frames.




## Acciones concretas realizadas sobre los datos aportados.

*  Realizamos el siguiente **request**: curl "https://www.quandl.com/api/v3/datasets"

*  **Importamos** los módulos necesarios.

*  Hacemos una llamada para obtener el **json**.

*  Obtenemos la respuesta de la **API**.

*  **Seleccionamos** la información que necesitamos para generar el data frame.

*  Cada serie de información seleccionada la almacenamos en una **lista** distinta.

*  Creamos el **data frame**. Las columnas proceden de las listas generadas.

*  Exportamos el data frame a un **csv**.

*  Hacemos **Parsing** del HTML para conseguir la info necesaria: los titulares diarios del FT sobre Apple.

*  Realizamos un **data frame** con la información obtenida del parsing.

*  Agrupamos los titulares procedentes de los mismos días en un mismo registro: utilizando **groupby** y **aggregate**.

*  Exportamos del **df** con los titulares.

*  Creamos un data frame uniendo el data frame de las cotizaciones y de los titulares: **concat**

*  Exportamos del **df combinado**.
