from scipy import stats
import numpy as np

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

def RegresionLog(Datos_X, Datos_Y):
  """
  Realiza la regresión potenciaal en base a los datos de entrada con la librería sklearn y devuelve la función y un analisis estadístico sobre la relación entre las variables.
  Inputs:  Datos_X - Array de 1D de datos utilizados como variable independiente en la regresión.
           Datos_Y - Array de 1D y mismo tamaño que Datos_X de datos utilizados como variable dependiente en la regresión.
  Outputs: Recta_Regresion - Función Lambda obtenida mediante la regresión.
           R2 - Valor de R² para la relación de dependencia entre los Datos_X y Datos_Y
           PValue - Valor del P value para las dos listas de datos. Nos determina la significancia de la regresión.
           DesviacionEstandar - Estimacion del desvio estandar entre la recta real y la aproximada.
  """
  X_log = np.log(Datos_X) # Linealizamos los datos para poder utilizar el método de aproximación lineal con el que venimos trabajando
  Y_log = np.log(Datos_Y) # Y = C * X**b  ->  ln(Y) = b * ln(X) + ln(C)  ->  m = b, c = ln(C)

  Estadisticas = stats.linregress(X_log, Y_log) #"Entreno" al modelo de SciPy con los datos X e Y para que haga la regresión lineal.

  b = Estadisticas.slope
  log_c = Estadisticas.intercept
  C = np.exp(log_c) # Despejamos 'C' de la linealización.

  Recta_Regresion = lambda x: C * (x**b)

  PValue = Estadisticas.pvalue
  DesviacionEstandar = Estadisticas.stderr
  R2 = Estadisticas.rvalue**2

  return(Recta_Regresion, R2, PValue, DesviacionEstandar)
