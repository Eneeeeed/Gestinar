from data_manager import cargar_inventario
import os

base = os.path.dirname(os.path.abspath(__file__))
ruta = os.path.join(base, "data", "Data.xlsx")

def Ingresar_unidades(Item, Descripcion, Unidad, Cant): 
    df.loc[len(df)]=[Item, Descripcion, Unidad, Cant]                                                   #INGRESAR UNIDADES AL DATAFRAME
    guardar_excel()                                                                                     #GUARDAR CAMBIOS
    return
        
def validacion_unidad(Cant,Unidad):
    try: 
        if Unidad.strip().lower()!='u':                                                                 #VALIDACION DE UNIDAD PRESENTADA (CASO "u")
            Cant=float(Cant)
        else:                                                                                           #VALIDACION DE UNIDADA PRESENTADA (CASO DIFERENTE DE "u")
            Cant=int(Cant)
        
    except ValueError:                                                                                  #CASO EN QUE SE PRESENTE UN VALOR NO VALIDO
        return False, None
    
    if Cant<0:                                                                                          #CASO SI SE INGRESA UN VALOR NEGATIVO
        return False, None
    else:
        return True, Cant

def modificar_item(item_mod, nuevo_nombre, nuevo_desc, nueva_cant, nuevo_uni):
    df.loc[df['ITEM']==item_mod]=[nuevo_nombre, nuevo_desc, nueva_cant, nuevo_uni]                      #MODIFICACION DE DATOS DENTRO DEL DATAFRAME
    guardar_excel()

        
def eliminar_item(item_elem):
    df.drop(df.loc[df['ITEM']==item_elem].index, inplace=True)                                          #ELIMINAR ITEMS DENTRO DEL DATAFRAME
    guardar_excel()

def sacar_items(seleccion):
    recoger=df.loc[df['ITEM']==seleccion].values.tolist()                                               #SELECCIO DE ITEM ESPECIFICO
    return recoger

def guardar_excel():
    df.to_excel(ruta, index=False)

def dataframe():
    return cargar_inventario()                                                                          #LLAMADO A DATA_MANAGER Y EJECUCION DEL DF

df=dataframe()
