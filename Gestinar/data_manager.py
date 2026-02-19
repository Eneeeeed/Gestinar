import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def cargar_inventario():
    ruta = os.path.join(BASE_DIR, "data", "Data.xlsx")                              #LOCALIZACION DEL DATAFRAME "DATA"
    return pd.read_excel(ruta)                                                      #REGRESAR DATAFRAME