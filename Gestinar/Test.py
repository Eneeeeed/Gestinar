import pandas as pd
import os
import re

def generar_registro_entrada(nombre):
    df_item=pd.DataFrame(
        {"Descripción": [],
         "Cantidad": [],
         "Proveedor": [],
         "Fecha de pedido": [],
         "Fecha de entrega": []
         })
    
    ruta = os.path.join('entrada', f"Registro de Ingresos de {nombre}.xlsx")
    df_item.to_excel(ruta, index=False)

def generar_registro_salida(nombre):
    df_item=pd.DataFrame(
        {"Descripción": [],
         "Cantidad": [],
         "Operario": [],
         "Fecha de consumo": []
         })
    
    ruta = os.path.join('salida', f"Registro de Salidas de {nombre}.xlsx")
    df_item.to_excel(ruta, index=False)

def ingresar_registro(selec, desc, cant, persona, fecha1, fecha2, op, decision):
    ruta=decision
    archivos=os.listdir(ruta)
    patron = re.compile(rf"{re.escape(selec)}.*\.xlsx$")
    
    for archivo in archivos:
        if patron.search(archivo):
            archivo_encontrado = archivo
            break
    
    ruta_comp=os.path.join(ruta, archivo_encontrado)
    df=pd.read_excel(ruta_comp)
    
    if decision=="Entrada":
        df.loc[len(df)]=[desc, cant, persona, fecha1, fecha2]
        
    elif decision=="Salida":
        df.loc[len(df)]=[desc, cant, persona, fecha1]

