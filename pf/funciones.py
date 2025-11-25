from scipy import stats
def Reglineal(Datos_X, Datos_Y):
  """
  Realiza la regresión lineal en base a los datos de entrada con la librería sklearn y devuelve la función y un analisis estadístico sobre la relación entre las variables.
  Inputs:  Datos_X - Array de 1D de datos utilizados como variable independiente en la regresión.
           Datos_Y - Array de 1D y mismo tamaño que Datos_X de datos utilizados como variable dependiente en la regresión.
  Outputs: Recta_Regresion - Función Lambda obtenida mediante la regresión.
           R2 - Valor de R² para la relación de dependencia entre los Datos_X y Datos_Y
           PValue - Valor del P value para las dos listas de datos. Nos determina la significancia de la regresión.
           DesviacionEstandar - Estimacion del desvio estandar entre la recta real y la aproximada.
  """
  X_reg = Datos_X.reshape(-1, 1)  #Para poder utilizar la función de sklearn: "linregress", la variable independiente debe de ser de dimensión 2
  Y_reg = Datos_Y                 #Guardo los datos en otra variable para no alterar los de entrada.

  Estadisticas = stats.linregress(Datos_X, Datos_Y) #"Entreno" al modelo de SciPy con los datos X e Y para que haga la regresión lineal.
  m = Estadisticas.slope               #Extraigo la pendiente de la recta a estimar del modelo.
  c = Estadisticas.intercept           #Extraigo la Ordenada al Origen del modelo.

  Recta_Regresion = lambda x: m * x + c

  PValue = Estadisticas.pvalue
  DesviacionEstandar = Estadisticas.stderr
  R2 = Estadisticas.rvalue**2

  return(Recta_Regresion, R2, PValue, DesviacionEstandar)
def es_float(valor):
   try: 
      float(valor)
      return True
   except:
      return False
def Pesos_Caracteristicos(
        pasajeros_nuevos,
        pasajeros_data,
        mtow_data,
        oew_data,
        fw_data,
        cu_data
    ):
    """
    Calcula los pesos característicos del avión usando SOLO los datos
    pasados como argumento. NO depende de módulos externos.

    Inputs:
        pasajeros_nuevos : valor a predecir
        pasajeros_data   : array de pasajeros de la base
        mtow_data        : array MTOW de la base
        oew_data         : array OEW de la base
        fw_data          : array fuel weight de la base
        cu_data          : array carga útil de la base
    """

    func_MTOW = Reglineal(pasajeros_data, mtow_data)[0]
    Nuevo_MTOW = func_MTOW(pasajeros_nuevos)

    func_OEW = Reglineal(mtow_data, oew_data)[0]
    Nuevo_OEW = func_OEW(Nuevo_MTOW)

    func_FW = Reglineal(mtow_data, fw_data)[0]
    Nuevo_FW = func_FW(Nuevo_MTOW)

    func_CU = Reglineal(mtow_data, cu_data)[0]
    Nuevo_CU_Reg = func_CU(Nuevo_MTOW)

    Nuevo_CU_Dif = Nuevo_MTOW - Nuevo_OEW - Nuevo_FW

    return Nuevo_MTOW, Nuevo_OEW, Nuevo_CU_Dif, Nuevo_CU_Reg

def Dimensiones_Fuselaje(
        mtow_nuevo,
        hileras_nuevas,
        hileras_data,
        anchos_fus_data,
        altos_fus_data,
        mtow_base,
        sw_base
    ):
    """
    Calcula dimensiones del fuselaje y superficie alar usando SOLO datos
    pasados como parámetros. NO toma nada de ningún módulo externo.
    """

    func_ancho = Reglineal(hileras_data, anchos_fus_data)[0]
    Nuevo_Ancho = func_ancho(hileras_nuevas)

    func_alto = Reglineal(hileras_data, altos_fus_data)[0]
    Nuevo_Alto = func_alto(hileras_nuevas)

    func_swal = Reglineal(mtow_base, sw_base)[0]
    Nuevo_SupAlar = func_swal(mtow_nuevo)

    Nuevo_CargaAlar = mtow_nuevo / Nuevo_SupAlar

    return Nuevo_Ancho, Nuevo_Alto, Nuevo_SupAlar, Nuevo_CargaAlar


