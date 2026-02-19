import pandas as pd
import os

class Registro:
    def __init__(self, item, caso):                                                                     #ATRIBUTOS DE LOS REPORTES
        self.item=item
        self.caso=caso
       
    def _ruta(self):
        return os.path.join(self.caso, f'Registro de {self.caso} de {self.item}.xlsx')                  #BUSCAR RUTA DE REPORTE ESPECIFICO
    
    def obtener_registro(self, columnas):
        ruta=self._ruta()                                                                               #USO DE LA VARIABLE RUTA CON LA DIRECCION DEL REPORTE
        
        if not os.path.exists(ruta):                                                                    #SI NO EXISTE EL DATA FRAME SE GENERA UNO
            df=pd.DataFrame(columns=columnas)
        else:                                                                                           #SI EXISTE UN REPORTE SOLO SE LEE
            df=pd.read_excel(ruta)
         
        return df
    
    def guardar_registro(self, datos, df):
        ruta=self._ruta()

        df.loc[len(df)]=datos
        df.to_excel(ruta, index=False)                                                                  #INGRESAR DATOS Y GUARDAR CAMBIOS
       
        
    def validacion(self, cant):
        ruta = os.path.join('data',"Data.xlsx")                                                         #BUSCAR RUTA DEL DATAFRAME DATA
        df=pd.read_excel(ruta)                                                                          #LEER DATAFRAME
        
        filtro=df.loc[df['ITEM']==self.item,"Unidad de medida"]                                         #IMPLEMENTAR FILTRO
        Unidad=filtro.iloc[0].strip().lower()
        
        if filtro.empty:                                                                                #CASO EN EL CUAL EL FILTRO ESTE VACIO
            return False, None
        
        try:
            cant=float(cant)                                                                            #PRIMERO PONER LA CANTIDAD INGRESADA EN FLOAT
        except ValueError:
            return False, None
        
        if cant<=0:                                                                                     #VALIDAR SI NO ES NEGATIVO
            return False, None
        
        if Unidad=='u':                                                                                 #VALIDACION POR UNIDAD
            if cant.is_integer():                                                                       #DETERMINAR SI LA CANTIDAD ES UN ENTERO SI ES QUE SE USA EL CASO "u"
                return True, int(cant)
            else:
                return False, None
        else:
            return True, float(cant)                                                                    #CASO CONTRARIO DE "u"
    
    def conexion(self, cant):
        ruta = os.path.join('data',"Data.xlsx")                                                         #BUSCAR RUTA DEL DATAFRAME DATA
        df=pd.read_excel(ruta)
        filtro=df.loc[df['ITEM']==self.item,"Cantidad"]                                                 #IMPLEMENTAR FILTRO
        dato=filtro.iloc[0]
        
        if filtro.empty:                                                                                #CASO EN EL CUAL EL FILTRO ESTE VACIO
            return False
        
        if self.caso.strip().lower()=='entrada':                                                        #CASO PARA ENTRADA
            nuevo=dato+cant
            
        elif self.caso.strip().lower()=='salida':                                                       #CASO PARA SALIDA
            nuevo=dato-cant
            
        df.loc[df['ITEM']==self.item,"Cantidad"]=nuevo
        df.to_excel(ruta, index=False)                                                                  #REALIZAR CAMBIOS Y GUARDAR
        return True
    
    def eliminar(self):                                                                                 #ELIMINAR REPORTES (PARA FUTURAS VERSIONES)
        ruta=self._ruta()
        if os.path.exists(ruta):
            os.remove(ruta)

class regitro_entrada(Registro):
    def __init__(self, item):
        super().__init__(item, "entrada")                                                               #ATRIBUTOS PARA REPORTE ENTRADA

    def generar(self):                                                                                  #GENERAR COLUMNAS PARA EL REPORTE
        columnas=["Descripcion",
            "Cantidad",
            "Proveedor",
            "Fecha de pedido",
            "Fecha de entrega"]
        return self.obtener_registro(columnas)
    


class regitro_salida(Registro):
    def __init__(self,item):
        super().__init__(item, "salida")

    
    def generar(self):
        columnas=["Descripcion",
            "Cantidad",
            "Operario",
            "Fecha de salida"]
        return self.obtener_registro(columnas)
