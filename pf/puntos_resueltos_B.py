import numpy as np
import matplotlib.pyplot as plt
import datos as dt
import funciones as fa

def punto_1_B(cant_pas_ini, filas_extra):
# --------- CÁLCULOS ORIGINALES (INTOCABLES) ---------

    filas_base = dt.Func_Filas(cant_pas_ini)
    hileras_base = dt.Func_Hileras(cant_pas_ini)
    pasillos_base = dt.Func_Pasillos(cant_pas_ini)

    filas_base_int = int(round(filas_base))
    hileras_base_int = int(round(hileras_base))
    pasillos_base_int = max(1, int(round(pasillos_base)))
    filas_extra_int = int(round(filas_extra))

    filas_totales = filas_base_int + filas_extra_int
    pasajeros_nuevos = filas_totales*hileras_base_int

    # ---------------- FIGURAS ----------------
    fig = plt.Figure(figsize=(8,6))

    ax1 = fig.add_subplot(2,2,2)
    ax1.plot(dt.Pasajeros, dt.HilerasAsientos, 'm.')
    ax1.scatter([pasajeros_nuevos],[hileras_base_int],c="b")
    ax1.grid(True)
    try:
        ax1.plot(dt.Pasajeros, dt.Recta_H, 'r-')
    except:
        pass
    ax1.set_title("Pasajeros vs Hileras")

    ax2 = fig.add_subplot(2,2,3)
    ax2.plot(dt.Pasajeros, dt.FilasAsientos, 'm.')
    ax2.scatter([pasajeros_nuevos],[filas_totales],c="b")
    ax2.grid(True)
    try:
        ax2.plot(dt.Pasajeros, dt.Recta_F, 'r-')
    except:
        pass
    ax2.set_title("Pasajeros vs Filas")

    ax3 = fig.add_subplot(2,2,4)
    ax3.plot(dt.Pasajeros, dt.Pasillos, 'm.')
    ax3.scatter([pasajeros_nuevos],[pasillos_base_int],c="b")
    ax3.grid(True)
    try:
        ax3.plot(dt.Pasajeros, dt.Recta_P, 'r-')
    except:
        pass
    ax3.set_title("Pasajeros vs Pasillos")

    try:
        fig.tight_layout()
    except:
        pass

    resultados = {
        "Filas base": filas_base_int,
        "Hileras": hileras_base_int,
        "Pasillos": pasillos_base_int,
        "Filas totales": filas_totales,
        "Pasajeros nuevos": pasajeros_nuevos,
    }

    return resultados, [fig]

def punto_2_B(cant_pas):
    cant_pas = int(cant_pas)

    mtow_int = int(round(dt.Func_MTOW_pas(cant_pas)))
    oew_int  = int(round(dt.Func_OEW_pas(cant_pas)))
    cu_int   = int(round(dt.Func_CU_pas(cant_pas)))
    PC_int   = int(round(dt.Funcion_Peso_Comb_pas(cant_pas)))

    fig = plt.Figure(figsize=(10,10))

    ax1 = fig.add_subplot(2,2,1)
    ax1.plot(dt.Pasajeros, dt.MTOW, 'm.')
    ax1.scatter([cant_pas],[mtow_int],c="b")
    ax1.grid(True)
    try:
        ax1.plot(dt.Pasajeros, dt.Recta_M, 'r-')

    except Exception:
        pass
    ax1.set_title("Pasajeros vs MTOW")

    ax2 = fig.add_subplot(2,2,2)
    ax2.plot(dt.Pasajeros, dt.OEW, 'm.')
    ax2.scatter([cant_pas],[oew_int],c="b")
    ax2.grid(True)
    try:
        ax2.plot(dt.Pasajeros, dt.Recta_OEW_P, 'r-')
    except Exception:
        pass
    ax2.set_title("Pasajeros vs OEW")

    ax3 = fig.add_subplot(2,2,3)
    ax3.plot(dt.Pasajeros, dt.CU, 'm.')
    ax3.scatter([cant_pas],[cu_int],c="b")
    ax3.grid(True)
    try:
        ax3.plot(dt.Pasajeros, dt.Recta_CU_P, 'r-')
    except Exception:
        pass
    ax3.set_title("Pasajeros vs CU")

    ax4 = fig.add_subplot(2,2,4)
    ax4.plot(dt.Pasajeros, dt.Peso_Comb, 'm.')
    ax4.scatter([cant_pas],[PC_int],c="b")
    ax4.grid(True)
    try:
        ax4.plot(dt.Pasajeros, dt.Recta_PC_P, 'r-')
    except Exception:
        pass
    ax4.set_title("Pasajeros vs Combustible")

    # ajustar layout
    try:
        fig.tight_layout()
    except Exception:
        pass

    resultados = {
        "MTOW [kg]": mtow_int,
        "OEW [kg]": oew_int,
        "CU [kg]": cu_int,
        "Peso Combustible [kg]": PC_int,
    }

    return resultados, [fig]

def punto_3_B(MTOW_in, hileras_in):
    MTOW_in = int(round(float(MTOW_in)))
    hileras_in = int(round(float(hileras_in)))

    Nuevo_Ancho = fa.Reglineal(dt.HilerasAsientos33, dt.An_Fus)[0](hileras_in)
    Nuevo_Alto = fa.Reglineal(dt.HilerasAsientos33, dt.Al_Fus)[0](hileras_in)

    Nuevo_SupAlar = fa.Reglineal(dt.MTOW33, dt.Sw_m2)[0](MTOW_in)
    Nuevo_CargaAlar = MTOW_in / Nuevo_SupAlar

    fig = plt.Figure(figsize=(12,4))

    ax1 = fig.add_subplot(1,3,1)
    ax1.scatter(dt.HilerasAsientos33, dt.An_Fus, c="m")
    ax1.scatter([hileras_in],[Nuevo_Ancho],c="b")
    ax1.grid(True)
    # agregar recta de regresión de ancho vs hileras (si existe Func_Ancho)
    try:
        x_lin = np.linspace(np.min(dt.HilerasAsientos33), np.max(dt.HilerasAsientos33), 200)
        ax1.plot(x_lin, dt.Func_Ancho(x_lin), 'r-')
    except Exception:
        pass
    ax1.set_title("Ancho fuselaje vs hileras")

    ax2 = fig.add_subplot(1,3,2)
    ax2.scatter(dt.HilerasAsientos33, dt.Al_Fus, c="m")
    ax2.scatter([hileras_in],[Nuevo_Alto],c="b")
    ax2.grid(True)
    try:
        x_lin2 = np.linspace(np.min(dt.HilerasAsientos33), np.max(dt.HilerasAsientos33), 200)
        ax2.plot(x_lin2, dt.Func_Alto(x_lin2), 'r-')
    except Exception:
        pass
    ax2.set_title("Alto fuselaje vs hileras")

    ax3 = fig.add_subplot(1,3,3)
    ax3.scatter(dt.MTOW33, dt.Carga_Alar, c="m")
    ax3.scatter([MTOW_in],[Nuevo_CargaAlar],c="b")
    ax3.grid(True)
    try:
        x_lin3 = np.linspace(np.min(dt.MTOW33), np.max(dt.MTOW33), 200)
        ax3.plot(x_lin3, dt.Func_Carga(x_lin3), 'r-')
    except Exception:
        pass
    ax3.set_title("Carga alar vs MTOW")

    # ajustar layout
    try:
        fig.tight_layout()
    except Exception:
        pass

    resultados = {
        "Ancho de Fuselaje [mm]": Nuevo_Ancho,
        "Alto de Fuselaje [mm]": Nuevo_Alto,
        "Superficie Alar [m^2]": Nuevo_SupAlar,
        "Carga Alar [kg/m^2]": Nuevo_CargaAlar,
    }

    return resultados, [fig]

def punto_4_B(diam_in, filas_in, hileras_in):
    diam_in = float(diam_in)
    filas_in = int(round(float(filas_in)))
    hileras_in = int(round(float(hileras_in)))

    pasajeros_diseño = filas_in * hileras_in

    LCC_est  = dt.Func_LCC(diam_in)
    LN_est   = dt.Func_LN(diam_in)
    LCab_est = dt.Func_LCab(pasajeros_diseño)

    fig = plt.Figure(figsize=(15,4))

    ax1 = fig.add_subplot(1,3,1)
    ax1.scatter(dt.DiametroMedio, dt.LCC, c="m")
    ax1.scatter([diam_in],[LCC_est],c="b")
    ax1.grid(True)
    # recta LCC vs diámetro
    try:
        x_lin = np.linspace(np.min(dt.DiametroMedio), np.max(dt.DiametroMedio), 200)
        ax1.plot(x_lin, dt.Func_LCC(x_lin), "r-")
    except Exception:
        pass
    ax1.set_title("LCC vs diámetro")

    ax2 = fig.add_subplot(1,3,2)
    ax2.scatter(dt.DiametroMedio, dt.LN, c="m")
    ax2.scatter([diam_in],[LN_est],c="b")
    ax2.grid(True)
    try:
        x_lin2 = np.linspace(np.min(dt.DiametroMedio), np.max(dt.DiametroMedio), 200)
        ax2.plot(x_lin2, dt.Func_LN(x_lin2), "r-")
    except Exception:
        pass
    ax2.set_title("LN vs diámetro")

    ax3 = fig.add_subplot(1,3,3)
    ax3.scatter(dt.Pasajeros33, dt.L_Cab, c="m")
    ax3.scatter([pasajeros_diseño],[LCab_est],c="b")
    ax3.grid(True)
    try:
        x_lin3 = np.linspace(np.min(dt.Pasajeros33), np.max(dt.Pasajeros33), 200)
        ax3.plot(x_lin3, dt.Func_LCab(x_lin3), "r-")
    except Exception:
        pass
    ax3.set_title("Cabina vs Pasajeros")

    # ajustar layout
    try:
        fig.tight_layout()
    except Exception:
        pass

    resultados = {
        "Longitud de cono de cola [mm]": LCC_est,
        "Longitud de nariz [mm]": LN_est,
        "Longitud de cabina [mm]": LCab_est,
    }

    return resultados, [fig]

def punto_5_B(MTOW_in5):
    MTOW_in5 = int(round(float(MTOW_in5)))
    Sw_est5    = dt.Func_Sw5(MTOW_in5)
    Carga_est5 = MTOW_in5/Sw_est5

    b_est5     = dt.Func_b5(MTOW_in5)
    Al_est5    = dt.Func_Al5(MTOW_in5)

    fig = plt.Figure(figsize=(10,8))

    x_linea = np.linspace(dt.MTOW33.min(), dt.MTOW33.max(), 1000)

    ax1 = fig.add_subplot(2,2,1)
    ax1.scatter(dt.MTOW33, dt.Carga_Alar, c="m")
    ax1.scatter([MTOW_in5],[Carga_est5],c="b")
    ax1.grid(True)
    try:
        ax1.plot(x_linea, dt.Func_Carga5(x_linea), 'r-')
    except Exception:
        pass
    ax1.set_title("Carga alar vs MTOW")

    ax2 = fig.add_subplot(2,2,2)
    ax2.scatter(dt.MTOW33, dt.Sw_m2, c="m")
    ax2.scatter([MTOW_in5],[Sw_est5],c="b")
    ax2.grid(True)
    try:
        ax2.plot(dt.MTOW33, dt.Func_Sw5(dt.MTOW33), 'r-')
    except Exception:
        pass
    ax2.set_title("Superficie alar vs MTOW")

    ax3 = fig.add_subplot(2,2,3)
    ax3.scatter(dt.MTOW33, dt.b, c="m")
    ax3.scatter([MTOW_in5],[b_est5],c="b")
    ax3.grid(True)
    try:
        ax3.plot(dt.MTOW33, dt.Func_b5(dt.MTOW33), 'r-')
    except Exception:
        pass
    ax3.set_title("Envergadura vs MTOW")

    ax4 = fig.add_subplot(2,2,4)
    ax4.scatter(dt.MTOW33, dt.Alargamiento, c="m")
    ax4.scatter([MTOW_in5],[Al_est5],c="b")
    ax4.grid(True)
    try:
        ax4.plot(dt.MTOW33, dt.Func_Al5(dt.MTOW33), 'r-')
    except Exception:
        pass
    ax4.set_title("Alargamiento vs MTOW")

    # ajustar layout
    try:
        fig.tight_layout()
    except Exception:
        pass

    resultados = {
        "Carga Alar [kg/m^2]": Carga_est5,
        "Superficie Alar [m^2]": Sw_est5,
        "Envergadura [mm]": b_est5,
        "Alargamiento": Al_est5,
    }

    return resultados, [fig]
def menu():
    print("Seleccione el punto a ejecutar:")
    print("1 - Punto 1")
    print("2 - Punto 2")
    print("3 - Punto 3")
    print("4 - Punto 4")
    print("5 - Punto 5")

    opcion = input("Ingrese número (1-5): ")

    if opcion == "1":
        punto_1_B()
    elif opcion == "2":
        punto_2_B()
    elif opcion == "3":
        punto_3_B()
    elif opcion == "4":
        punto_4_B()
    elif opcion == "5":
        punto_5_B()
    else:
        print("Opción inválida")
def ejecutar_todo_B(cant_pas_ini, filas_extra, diam_in):
    resultados = {}
    figuras = []
    resultadosp1, figurasp1 = punto_1_B(cant_pas_ini, filas_extra)
    hileras = resultadosp1['Hileras'] 
    filas = resultadosp1['Filas totales']
    resultadosp2, figurasp2 = punto_2_B(cant_pas_ini)
    MTOW = resultadosp2['MTOW [kg]']
    resultadosp3, figurasp3 = punto_3_B(MTOW, hileras)
    resultadosp4, figurasp4 = punto_4_B(diam_in, filas, hileras)
    resultadosp5, figurasp5 = punto_5_B(MTOW)
    for dic in (resultadosp1, resultadosp2, resultadosp3, resultadosp4, resultadosp5):
        resultados.update(dic)    
    for figs in (figurasp1, figurasp2, figurasp3, figurasp4, figurasp5):
        figuras.extend(figs)
    return resultados, figuras
