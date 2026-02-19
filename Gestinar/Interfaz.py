import tkinter as tk
from tkinter import ttk
import Logica
from tkinter import messagebox
import we

def ventana_principal():                                                                #VENTANA PRINCIPAL DONDE SE ENCUENTRAN TODAS LAS OPCIONES DISPONIBLES
    ventana=tk.Tk()
    ventana.geometry("500x400")
    ventana.title("Gestinar")
    ventana.resizable(False, False)
    
    bienvenida=tk.Label(ventana, text="Bienvenido", bg="black", fg="White")             #GENERACION DE LABEL, USADO PARA SOLO MOSTRAR TEXTO (NO SE REPETIRA, YA QUE SE VE SEGUIDAMENTE)
    bienvenida.pack(fill=tk.X)
    
    botones={                                                                           #DICCIONARIO DONDE SE ENCUENTRAN LAS OPCIONES Y SUS FUNCIONES
        "Ingresar Item": lambda: ingresar_item(ventana),    
        "Modificar Item": lambda: selec_item(modificar_item, ventana),
        "Eliminar Item": lambda: selec_item(eliminar_item, ventana),
        "Ver inventario": lambda: ver_inventario(ventana),
        "Entradas": lambda: reportes(ventana, "entrada"),
        "Salidas": lambda: reportes(ventana, "salida")
        }
    
    for boton in botones:
        tk.Button(ventana, text=boton, command=botones[boton]).pack(pady=12.5)
        
    ventana.mainloop()
    
def ingresar_item(parent):
    ventana_ingresar=tk.Toplevel(parent)
    ventana_ingresar.geometry("360x300")
    ventana_ingresar.title("Ingresar Item")
    ventana_ingresar.resizable(False, False)

    Titulo=tk.Label(ventana_ingresar, text="Esta agregando Items", bg="black", fg="White")
    Titulo.grid(columnspan=3 ,sticky="nsew")
    
    etiquetas=["Ingresar nombre del Item","Ingresar descripcion del Item","Ingresar unidad de medida del Item","Ingresar cantidad del Item"]    #LISTA DE ETIQUETAS
    
    for i, etiqueta in enumerate(etiquetas, start=1):
        tk.Label(ventana_ingresar, text=etiqueta).grid(row=i, column=0, padx=20, pady=20, sticky="e")

    entry_item=tk.Entry(ventana_ingresar)                                                                                                       #SERIE DE ENTRYS PARA RECOGER DATOS
    entry_item.grid(row=1, column=2)
    
    entry_desc=tk.Entry(ventana_ingresar)
    entry_desc.grid(row=2, column=2)
    
    entry_unid=tk.Entry(ventana_ingresar)
    entry_unid.grid(row=3, column=2)
    
    entry_cant=tk.Entry(ventana_ingresar)
    entry_cant.grid(row=4, column=2)
    
    botones2={                                                                                                                                  #DICCIONARIO DE BOTONES DISPONIBLES DENTRO DE LA VENTANA
        "Regresar": [lambda: ventana_ingresar.destroy(), 0],
        "Guardar": [lambda: guardar_items(ventana_ingresar, entry_item, entry_desc, entry_unid, entry_cant), 2]
        }
    
    for boton in botones2:
        n=botones2[boton][1]
        tk.Button(ventana_ingresar, text=boton, command=botones2[boton][0]).grid(row=5, column=n)
    
def guardar_items(ventana_ingresar, entry_item, entry_desc, entry_unid, entry_cant):
    item=entry_item.get()                                                                                                                       #RECOGIDA DE DATOS
    desc=entry_desc.get()
    unidad=entry_unid.get()
    cant_aux=entry_cant.get()

    datos=[item.strip(), unidad.strip().lower(), cant_aux.strip()]                                                                              #ENLISTAR DATOS
    
    if not all(datos):                                                                                                                          #VALIDACION, EXIGE QUE SE INGRESEN TODOS LOS CAMPOS DISPONIBLES
        error("Ingrese datos")
        return None

    valid, cant=Logica.validacion_unidad(cant_aux.strip(), unidad)                                                                              #EJECUCION DE LOGICA, USADA PARA LA VALIDACION DE DATOS
    
    if not valid:
        error("Ingrese cantidad valida")
        return
    
    if not confirmacion(f"¿Desea guardar el item '{item}'?"):
        return
        
    messagebox.showinfo("Éxito", "Item guardado correctamente")    
    Logica.Ingresar_unidades(item, desc, unidad, cant)                                                                                          #EJECUCION DE LOGICA, USADO PARA INGRESAR DATOS AL DATAFRAME "DATA"
    
    ventana_ingresar.destroy()

def ver_inventario(parent):
    ventana_inv=tk.Toplevel(parent)
    ventana_inv.geometry("500x350")
    ventana_inv.title("Vista de Items")
    
    data=Logica.dataframe()
    
    frame=ttk.Frame(ventana_inv)                                                                                                    
    frame.pack(fill=tk.BOTH, expand=True)
    
    
    columnas=list(data.columns)                                                                                                            #LLAMADO AL DATAFRAME DESDE LOGICA, SE BUSCA SOLO LAS COLUMNAS
    
    tree=ttk.Treeview(frame, columns=columnas, show='headings')                                                                                 #GENERACION DE TREEVIEW, USADO PARA VISUALIZACION DEL DATAFRAME "DATA"
    tree.grid(row=0, column=0, sticky="nsew")
    
    scrolly=ttk.Scrollbar(frame, orient="vertical", command=tree.yview)                                                                         #GENERACION DE UN SCROLLBAR PARA EL TREEVIEW, PARA EJE X E Y
    scrolly.grid(row=0, column=1, sticky="ns")
    scrollx=ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    scrollx.grid(row=1, column=0, sticky="ew")
    
    tree.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)                                                                      #CONFIGURACION DEL TREEVIEW CON SCROLLBAR

    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    for col in columnas:
        tree.heading(col, text=col)                                                                                                             #GENERACION DE ENCABEZADOS DEL TREEVIEW
        tree.column(col, width=120, anchor="center")                                                                                            #CONFIGURACION DE COLUMNAS
    
    for i, fila in data.iterrows():
        tree.insert("", tk.END, values=list(fila))                                                                                              #INSERTAR FILAS
    
def reportes(parent, caso):
    ventana_report=tk.Toplevel(parent)
    ventana_report.resizable(True, True)
    ventana_report.title("Vista de reportes")
    
    Titulo=tk.Label(ventana_report, text="Esta visualizando reportes", bg="black", fg="White")
    Titulo.grid(columnspan=5, sticky="nsew")
    frame=ttk.Treeview(ventana_report)                                                                                                          #GENERACION DE TREEVIEW
    frame.grid(column=3,rowspan=10, columnspan=5)
    
    if caso=="entrada":                                                                                                                         #DIFERENCIA DE CASOS DE REPORTE TANTO PARA ENTRADA COMO SALIDA
        Etiqueta=tk.Label(ventana_report, text="Seleccione item")
        Etiqueta.grid(row=1, column=2)
        Lista=ttk.Combobox(ventana_report, state="readonly", values=Logica.df['ITEM'].tolist())                                                 #COMBOBOX CON EL ENLISTADO DE ITEMS
        Lista.grid(row=2, column=2)
        
        Lista.bind(
        "<<ComboboxSelected>>",
        lambda event: reporte_entrada(event, caso, frame, ventana_report)
        )    
    
    elif caso=="salida":
        Etiqueta=tk.Label(ventana_report, text="Seleccione item")
        Etiqueta.grid(row=1, column=2)
        Lista=ttk.Combobox(ventana_report, state="readonly", values=Logica.df['ITEM'].tolist())
        Lista.grid(row=2, column=2)
        
        Lista.bind(
        "<<ComboboxSelected>>",
        lambda event: reporte_salida(event, caso, frame, ventana_report)
        )   
        
    regresar=tk.Button(ventana_report, text="Regresar", command=lambda: ventana_report.destroy())
    regresar.grid(row=8, column=2)

            

def selec_item(n, parent):
    ventana_selec=tk.Toplevel(parent)
    ventana_selec.geometry("400x130")
    ventana_selec.title("Seleccion Item")
    ventana_selec.resizable(False, False)
    
    Titulo=tk.Label(ventana_selec, text="Esta seleccionando Items", bg="black", fg="White")
    Titulo.grid(columnspan=3 ,sticky="nsew")
    
    Etiqueta=tk.Label(ventana_selec, text="Seleccione item")
    Etiqueta.grid(padx=20, pady=20)
    
    Lista=ttk.Combobox(ventana_selec, state="readonly", values=Logica.df['ITEM'].tolist())                                                      #COMBOBOX CON EL ENLISTADO DE ITEMS
    Lista.bind(
    "<<ComboboxSelected>>",
    lambda event: n(event, ventana_selec)
    )    
    Lista.grid(row=1, column=2)
    
    tk.Button(ventana_selec, text="Regresar", command=lambda: ventana_selec.destroy()).grid(row=2, column=1)
    
def modificar_item(event, ventana_selec):
    seleccion=event.widget.get()
    ventana_modificar=tk.Toplevel()
    ventana_modificar.geometry("360x300")
    ventana_modificar.title("Modificar Item")
    ventana_modificar.resizable(False, False)
    
    Titulo=tk.Label(ventana_modificar, text="Esta agregando Items", bg="black", fg="White")
    Titulo.grid(columnspan=4 ,sticky="nsew")
    
    etiquetas=["Nombre del item","Descripcion del Item","Unidad de medida del Item","Cantidad del Item"]                                        #SERIE DE ETIQUETAS
    
    for i, etiqueta in enumerate(etiquetas, start=1):
        tk.Label(ventana_modificar, text=etiqueta).grid(row=i, column=0, padx=20, pady=20, sticky="e")
    
    lista_iniciar=Logica.sacar_items(seleccion)                                                                                                 #SELECCION ESPECIFICA DE ITEM
    
    for i, elemento in enumerate(lista_iniciar[0], start=1):                                                                                    #MOSTRAR LOS DATOS ACTUALES DE UN ITEM
        tk.Label(ventana_modificar, text=elemento).grid(row=i, column=1, padx=20, pady=20, sticky="e")
        
    entry_item=tk.Entry(ventana_modificar)                                                                                                      #SERIE DE ENTRYS
    entry_item.grid(row=1, column=2)
     
    entry_desc=tk.Entry(ventana_modificar)
    entry_desc.grid(row=2, column=2)
     
    entry_unid=tk.Entry(ventana_modificar)
    entry_unid.grid(row=3, column=2)
     
    entry_cant=tk.Entry(ventana_modificar)
    entry_cant.grid(row=4, column=2)

    botones2={
        "Regresar": [lambda: ventana_modificar.destroy(), 0],
        "Guardar": [lambda: guardar_items(entry_item, entry_desc, entry_unid, entry_cant), 2]
        }
    
    for boton in botones2:
        n=botones2[boton][1]
        tk.Button(ventana_modificar, text=boton, command=botones2[boton][0]).grid(row=5, column=n)
        
def cargar_df(tree, df):
    for item in tree.get_children():                                                                                                            #OBTENER LOS "HIJOS" DEL ANTERIOR TREEVIEW Y ELIMINARLOS
        tree.delete(item)
        
    for col in df.columns:                                                                                                                      #GENERACION DE ENCABEZADOS Y CONFIGURACION DE COLUMNAS
        tree.heading(col, text=col)
        tree.column(col, width=120)
    
    for i,row in df.iterrows():                                                                                                                 #GENERACION DE FILAS DEL TREEVIEW
        tree.insert("", tk.END, values=list(row))
    

def reporte_entrada(event, caso, tree, ventana):
    seleccion=event.widget.get()
    registro=we.regitro_entrada(seleccion)                                                                                                      #GENERAR EL OBJETO REGISTRO ENTRADA
    df=registro.generar()                                                                                                                       #GENERAR EL DATAFRAME
    
    entry_desc=tk.Entry(ventana)                                                                                                                #SERIE DE ENTRYS
    entry_desc.grid(row=3, column=2)
        
    entry_cant=tk.Entry(ventana)
    entry_cant.grid(row=4, column=2)
        
    entry_prov=tk.Entry(ventana)
    entry_prov.grid(row=5, column=2)
        
    entry_fecha1=tk.Entry(ventana)
    entry_fecha1.grid(row=6, column=2)
        
    entry_fecha2=tk.Entry(ventana)
    entry_fecha2.grid(row=7, column=2)
    
    guardar=tk.Button(ventana, text="Guardar", command=lambda: data_entrada(entry_desc, entry_cant, entry_prov, entry_fecha1, entry_fecha2, df, registro, tree))
    guardar.grid(row=9, column=2)                                                                                                               #BOTON DE GUARDADO
        
    cargar_df(tree,df)                                                                                                                          #VOLVER A CARGAR DE TREEVIEW

def data_entrada(entry_desc, entry_cant, entry_prov, entry_fecha1, entry_fecha2, df, registro, tree):
    desc=entry_desc.get()                                                                                                                       #OBTENCION Y ENLISTADO DE DATOS
    cant=entry_cant.get()
    prov=entry_prov.get()
    fecha1=entry_fecha1.get()
    fecha2=entry_fecha2.get()
    datos=[desc, cant, prov, fecha1, fecha2]
    
    if not all(datos):                                                                                                                          #VALIDACION DE INGRESO DE TODOS LOS DATOS
        error("Ingrese datos")
        return None

    valid, cant=registro.validacion(cant)                                                                                                       #VALIDACION DE CANTIDAD CON UNIDAD INGRESADA
    
    if not valid:
        error("Ingrese cantidad valida")
        return
    
    if not confirmacion("¿Desea guardar?"):
        return
        
    messagebox.showinfo("Éxito", "Item guardado correctamente")
    registro.conexion(cant)                                                                                                                     #CONEXION DEL REPORTE CON DATAFRAME "DATA"
    registro.guardar_registro(datos, df)                                                                                                        #GUARDAR CAMBIOS
        
    cargar_df(tree, df)

def reporte_salida(event, caso, tree, ventana):                                                                                                 #MISMO CASO QUE EL DE ARRIBA SOLO USADO REGISTRO SALIDA
    seleccion=event.widget.get()
    registro=we.regitro_salida(seleccion)
    df=registro.generar()
    
    entry_desc=tk.Entry(ventana)
    entry_desc.grid(row=3, column=2)
        
    entry_cant=tk.Entry(ventana)
    entry_cant.grid(row=4, column=2)
        
    entry_ope=tk.Entry(ventana)
    entry_ope.grid(row=5, column=2)
        
    entry_fecha1=tk.Entry(ventana)
    entry_fecha1.grid(row=6, column=2)
    
    guardar=tk.Button(ventana, text="Guardar", command=lambda: data_salida(entry_desc, entry_cant, entry_ope, entry_fecha1, df, registro, tree))
    guardar.grid(row=9, column=2)
    
    cargar_df(tree,df)

def data_salida(entry_desc, entry_cant, entry_ope, entry_fecha1, df, registro, tree):
    desc=entry_desc.get()
    cant=entry_cant.get()
    ope=entry_ope.get()
    fecha1=entry_fecha1.get()
    datos=[desc, cant, ope, fecha1]
    
    if not all(datos):
        error("Ingrese datos")
        return None

    valid, cant=registro.validacion(cant)
    
    if not valid:
        error("Ingrese cantidad valida")
        return
    
    if not confirmacion("¿Desea guardar?"):
        return
        
    messagebox.showinfo("Éxito", "Item guardado correctamente")
    registro.conexion(cant)
    registro.guardar_registro(datos, df)
    
    cargar_df(tree, df)

def eliminar_item(event, ventana_selec):
    seleccion=event.widget.get()                                                    #OBTENCION DE LA SELECCION DEL COMBOBOX
    if confirmacion("¿Esta seguro de eliminar este item?"):                         #CONFIRMAR SELECCION
        Logica.eliminar_item(seleccion)                                             #ELIMINAR ITEM

    ventana_selec.destroy()                                                         #CERRAR VENTANA DE SELECCION

def error(msg):
    messagebox.showerror("Error", msg)
    
def confirmacion(msg):
    return messagebox.askyesno(title="¿Esta seguro?", message=msg)

def iniciar_app():
    ventana_principal()
    
iniciar_app()
