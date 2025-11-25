import numpy as np
# import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
#from scipy import stats
import datos as dt
import funciones as fa

def punto_1_B(cant_pas_ini, filas_extra):
    # -------- VALIDACIONES DE INPUT --------
    if cant_pas_ini == "" or filas_extra == "":
        raise ValueError("Ningún campo puede estar vacío.")

    # verificar que sean números
    try:
        cant_pas_ini = float(cant_pas_ini)
        filas_extra = float(filas_extra)
    except:
        raise ValueError("Solo se permiten números. No se permiten letras ni símbolos.")

    # verificar que no sean negativos
    if cant_pas_ini < 0 or filas_extra < 0:
        raise ValueError("Los valores no pueden ser negativos.")

    # verificar límites usando datos reales
    min_pas = min(dt.Pasajeros)
    max_pas = max(dt.Pasajeros)

    if not (min_pas <= cant_pas_ini <= max_pas):
        raise ValueError(
            f"La cantidad de pasajeros debe estar entre {min_pas} y {max_pas}."
        )

    # verificar que no estén vacíos
    if cant_pas_ini == "" or filas_extra == "":
        raise ValueError("Ningún campo puede estar vacío.")

    # verificar que sean números
    try:
        cant_pas_ini = float(cant_pas_ini)
        filas_extra = float(filas_extra)
    except:
        raise ValueError("Solo se permiten números. No se permiten letras ni símbolos.")

    # verificar que no sean negativos
    if cant_pas_ini < 0 or filas_extra < 0:
        raise ValueError("Los valores no pueden ser negativos.")

    # verificar límites usando datos reales
    min_pas = min(dt.Pasajeros)
    max_pas = max(dt.Pasajeros)

    if not (min_pas <= cant_pas_ini <= max_pas):
        raise ValueError(
            f"La cantidad de pasajeros debe estar entre {min_pas} y {max_pas}."
        )

    # si filas extra tiene un rango establecido
    if hasattr(dt, "Filas_min") and hasattr(dt, "Filas_max"):
        if not(dt.Filas_min <= filas_extra <= dt.Filas_max):
            raise ValueError(
                f"Las filas extra deben estar entre {dt.Filas_min} y {dt.Filas_max}."
            )

    # --------- CÁLCULOS ORIGINALES (INTOCABLES) ---------

    filas_base = dt.Func_Filas(cant_pas_ini)
    hileras_base = dt.Func_Hileras(cant_pas_ini)
    pasillos_base = dt.Func_Pasillos(cant_pas_ini)

    filas_base_int = int(round(filas_base))
    hileras_base_int = int(round(hileras_base))
    pasillos_base_int = max(1, int(round(pasillos_base)))
    filas_extra_int = int(round(filas_extra))

    filas_totales = filas_base_int + filas_extra_int
    pasajeros_nuevos = filas_totales * hileras_base_int

    # ---------------- FIGURAS ORIGINALES ----------------
    fig = plt.Figure(figsize=(8,6))

    ax1 = fig.add_subplot(2,2,2)
    ax1.plot(dt.Pasajeros, dt.HilerasAsientos, 'm.')
    try:
        ax1.plot(dt.Pasajeros, dt.Recta_H, 'r-')
    except:
        pass
    ax1.set_title("Pasajeros vs Hileras")

    ax2 = fig.add_subplot(2,2,3)
    ax2.plot(dt.Pasajeros, dt.FilasAsientos, 'm.')
    try:
        ax2.plot(dt.Pasajeros, dt.Recta_F, 'r-')
    except:
        pass
    ax2.set_title("Pasajeros vs Filas")

    ax3 = fig.add_subplot(2,2,4)
    ax3.plot(dt.Pasajeros, dt.Pasillos, 'm.')
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
        "Hileras base": hileras_base_int,
        "Pasillos base": pasillos_base_int,
        "Filas totales": filas_totales,
        "Pasajeros nuevos": pasajeros_nuevos,
    }

    return resultados, [fig]

def punto_2_B(cant_pas):
    cant_pas = float(cant_pas)

    mtow_int = int(round(dt.Func_MTOW_pas(cant_pas)))
    oew_int  = int(round(dt.Func_OEW_pas(cant_pas)))
    cu_int   = int(round(dt.Func_CU_pas(cant_pas)))
    PC_int   = int(round(dt.Funcion_Peso_Comb_pas(cant_pas)))

    fig = plt.Figure(figsize=(10,10))

    ax1 = fig.add_subplot(2,2,1)
    ax1.plot(dt.Pasajeros, dt.MTOW, 'm.')
    try:
        ax1.plot(dt.Pasajeros, dt.Recta_M, 'r-')
    except Exception:
        pass
    ax1.set_title("Pasajeros vs MTOW")

    ax2 = fig.add_subplot(2,2,2)
    ax2.plot(dt.Pasajeros, dt.OEW, 'm.')
    try:
        ax2.plot(dt.Pasajeros, dt.Recta_OEW_P, 'r-')
    except Exception:
        pass
    ax2.set_title("Pasajeros vs OEW")

    ax3 = fig.add_subplot(2,2,3)
    ax3.plot(dt.Pasajeros, dt.CU, 'm.')
    try:
        ax3.plot(dt.Pasajeros, dt.Recta_CU_P, 'r-')
    except Exception:
        pass
    ax3.set_title("Pasajeros vs CU")

    ax4 = fig.add_subplot(2,2,4)
    ax4.plot(dt.Pasajeros, dt.Peso_Comb, 'm.')
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
        "MTOW": mtow_int,
        "OEW": oew_int,
        "CU": cu_int,
        "Peso Combustible": PC_int,
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
    try:
        x_lin2 = np.linspace(np.min(dt.HilerasAsientos33), np.max(dt.HilerasAsientos33), 200)
        ax2.plot(x_lin2, dt.Func_Alto(x_lin2), 'r-')
    except Exception:
        pass
    ax2.set_title("Alto fuselaje vs hileras")

    ax3 = fig.add_subplot(1,3,3)
    ax3.scatter(dt.MTOW33, dt.Carga_Alar, c="m")
    ax3.scatter([MTOW_in],[Nuevo_CargaAlar],c="b")
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
        "Ancho": Nuevo_Ancho,
        "Alto": Nuevo_Alto,
        "Superficie Alar": Nuevo_SupAlar,
        "Carga Alar": Nuevo_CargaAlar,
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
    try:
        x_lin2 = np.linspace(np.min(dt.DiametroMedio), np.max(dt.DiametroMedio), 200)
        ax2.plot(x_lin2, dt.Func_LN(x_lin2), "r-")
    except Exception:
        pass
    ax2.set_title("LN vs diámetro")

    ax3 = fig.add_subplot(1,3,3)
    ax3.scatter(dt.Pasajeros33, dt.L_Cab, c="m")
    ax3.scatter([pasajeros_diseño],[LCab_est],c="b")
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
        "LCC": LCC_est,
        "LN": LN_est,
        "L_Cab": LCab_est,
    }

    return resultados, [fig]

def punto_5_B(MTOW_in5):
    MTOW_in5 = int(round(float(MTOW_in5)))

    Carga_est5 = dt.Func_Carga5(MTOW_in5)
    Sw_est5    = dt.Func_Sw5(MTOW_in5)
    b_est5     = dt.Func_b5(MTOW_in5)
    Al_est5    = dt.Func_Al5(MTOW_in5)

    fig = plt.Figure(figsize=(10,8))

    ax1 = fig.add_subplot(2,2,1)
    ax1.scatter(dt.MTOW33, dt.Carga_Alar, c="m")
    ax1.scatter([MTOW_in5],[Carga_est5],c="b")
    try:
        ax1.plot(dt.MTOW33, dt.Func_Carga5(dt.MTOW33), 'r-')
    except Exception:
        pass
    ax1.set_title("Carga alar vs MTOW")

    ax2 = fig.add_subplot(2,2,2)
    ax2.scatter(dt.MTOW33, dt.Sw_m2, c="m")
    ax2.scatter([MTOW_in5],[Sw_est5],c="b")
    try:
        ax2.plot(dt.MTOW33, dt.Func_Sw5(dt.MTOW33), 'r-')
    except Exception:
        pass
    ax2.set_title("Superficie alar vs MTOW")

    ax3 = fig.add_subplot(2,2,3)
    ax3.scatter(dt.MTOW33, dt.b, c="m")
    ax3.scatter([MTOW_in5],[b_est5],c="b")
    try:
        ax3.plot(dt.MTOW33, dt.Func_b5(dt.MTOW33), 'r-')
    except Exception:
        pass
    ax3.set_title("Envergadura vs MTOW")

    ax4 = fig.add_subplot(2,2,4)
    ax4.scatter(dt.MTOW33, dt.Alargamiento, c="m")
    ax4.scatter([MTOW_in5],[Al_est5],c="b")
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
        "Carga Alar": Carga_est5,
        "Superficie Alar": Sw_est5,
        "Envergadura": b_est5,
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
    import matplotlib.pyplot as plt

    # -----------------------------------------
    # Validación
    # -----------------------------------------
    if not (fa.es_float(cant_pas_ini) and fa.es_float(filas_extra) and fa.es_float(diam_in)):
        raise ValueError("Todos los valores deben ser numéricos")

    cant_pas_ini = float(cant_pas_ini)
    filas_extra = float(filas_extra)
    diam_in = float(diam_in)

    if cant_pas_ini < 0 or filas_extra < 0 or diam_in < 0:
        raise ValueError("Todos los valores deben ser positivos")

    # -----------------------------------------
    # Cálculos principales
    # -----------------------------------------
    filas_base_int = int(round(dt.Func_Filas(cant_pas_ini)))
    hileras_base_int = int(round(dt.Func_Hileras(cant_pas_ini)))
    pasillos_base_int = max(1, int(round(dt.Func_Pasillos(cant_pas_ini))))
    filas_extra_int = int(round(filas_extra))

    filas_totales = filas_base_int + filas_extra_int
    pasajeros_nuevos = filas_totales * hileras_base_int

    mtow_int = int(round(dt.Func_MTOW_pas(pasajeros_nuevos)))
    oew_int  = int(round(dt.Func_OEW_pas(pasajeros_nuevos)))
    cu_int   = int(round(dt.Func_CU_pas(pasajeros_nuevos)))
    PC_int   = int(round(dt.Funcion_Peso_Comb_pas(pasajeros_nuevos)))

    LCC_est = dt.Func_LCC(diam_in)
    LN_est  = dt.Func_LN(diam_in)
    LCab_est = dt.Func_LCab(pasajeros_nuevos)

    Carga_est5 = dt.Func_Carga5(mtow_int)
    Sw_est5    = dt.Func_Sw5(mtow_int)
    b_est5     = dt.Func_b5(mtow_int)
    Al_est5    = dt.Func_Al5(mtow_int)

    # -----------------------------------------
    # Generar figuras (SIN plt.show)
    # -----------------------------------------
    figuras = []

    # ======================================================
    # FIGURA 1 - Pasajeros vs Hileras / Filas / Pasillos
    # ======================================================
    fig1 = plt.figure(figsize=(10,10))

    plt.subplot(2,2,2)
    plt.plot(dt.Pasajeros, dt.HilerasAsientos, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_H, 'r-')
    plt.title("Pasajeros vs Hileras")
    plt.grid()

    plt.subplot(2,2,3)
    plt.plot(dt.Pasajeros, dt.FilasAsientos, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_F, 'r-')
    plt.title("Pasajeros vs Filas")
    plt.grid()

    plt.subplot(2,2,4)
    plt.plot(dt.Pasajeros, dt.Pasillos, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_P, 'r-')
    plt.title("Pasajeros vs Pasillos")
    plt.grid()

    fig1.tight_layout()
    figuras.append(fig1)

    # ======================================================
    # FIGURA 2 - Pasajeros vs MTOW / OEW / CU / Combustible
    # ======================================================
    fig2 = plt.figure(figsize=(10,10))

    plt.subplot(2,2,1)
    plt.plot(dt.Pasajeros, dt.MTOW, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_M, 'r-')
    plt.title("Pasajeros vs MTOW")
    plt.grid()

    plt.subplot(2,2,2)
    plt.plot(dt.Pasajeros, dt.OEW, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_OEW_P, 'r-')
    plt.title("OEW vs Pasajeros")
    plt.grid()

    plt.subplot(2,2,3)
    plt.plot(dt.Pasajeros, dt.CU, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_CU_P, 'r-')
    plt.title("CU vs Pasajeros")
    plt.grid()

    plt.subplot(2,2,4)
    plt.plot(dt.Pasajeros, dt.Peso_Comb, 'm.')
    plt.plot(dt.Pasajeros, dt.Recta_PC_P, 'r-')
    plt.title("Combustible vs Pasajeros")
    plt.grid()

    fig2.tight_layout()
    figuras.append(fig2)

    # ======================================================
    # FIGURA 3 - MTOW vs (Combustible / CU / OEW)
    # ======================================================
    fig3 = plt.figure(figsize=(10,10))

    plt.subplot(2,2,1)
    plt.plot(dt.MTOW, dt.Peso_Comb, 'm.')
    plt.plot(dt.MTOW, dt.Recta_PC, 'r-')
    plt.title("MTOW vs Combustible")
    plt.grid()

    plt.subplot(2,2,2)
    plt.plot(dt.MTOW, dt.CU, 'm.')
    plt.plot(dt.MTOW, dt.Recta_CU, 'r-')
    plt.title("MTOW vs CU")
    plt.grid()

    plt.subplot(2,2,3)
    plt.plot(dt.MTOW, dt.OEW, 'm.')
    plt.plot(dt.MTOW, dt.Recta_OEW, 'r-')
    plt.title("MTOW vs OEW")
    plt.grid()

    fig3.tight_layout()
    figuras.append(fig3)

    # ======================================================
    # FIGURA 4 - LCC / LN / Cabina
    # ======================================================
    fig4 = plt.figure(figsize=(15,5))

    plt.subplot(1,3,1)
    plt.scatter(dt.DiametroMedio, dt.LCC, c="m")
    plt.plot(dt.DiametroMedio, dt.Func_LCC(dt.DiametroMedio), "r-")
    plt.scatter([diam_in], [LCC_est], c="b")
    plt.title("LCC vs Diámetro")
    plt.grid()

    plt.subplot(1,3,2)
    plt.scatter(dt.DiametroMedio, dt.LN, c="m")
    plt.plot(dt.DiametroMedio, dt.Func_LN(dt.DiametroMedio), "r-")
    plt.scatter([diam_in], [LN_est], c="b")
    plt.title("LN vs Diámetro")
    plt.grid()

    plt.subplot(1,3,3)
    plt.scatter(dt.Pasajeros33, dt.L_Cab, c="m")
    plt.plot(dt.Pasajeros33, dt.Func_LCab(dt.Pasajeros33), "r-")
    plt.scatter([pasajeros_nuevos], [LCab_est], c="b")
    plt.title("Cabina vs Pasajeros")
    plt.grid()

    fig4.tight_layout()
    figuras.append(fig4)

    # ======================================================
    # FIGURA 5 - Ala (Carga, Superficie, Envergadura, Alargamiento)
    # ======================================================
    fig5 = plt.figure(figsize=(12,10))

    plt.subplot(2,2,1)
    plt.scatter(dt.MTOW33, dt.Carga_Alar, c="m")
    plt.plot(dt.MTOW33, dt.Func_Carga5(dt.MTOW33), 'r-')
    plt.scatter([mtow_int], [Carga_est5], c="b")
    plt.title("Carga alar vs MTOW")
    plt.grid()

    plt.subplot(2,2,2)
    plt.scatter(dt.MTOW33, dt.Sw_m2, c="m")
    plt.plot(dt.MTOW33, dt.Func_Sw5(dt.MTOW33), 'r-')
    plt.scatter([mtow_int], [Sw_est5], c="b")
    plt.title("Superficie alar vs MTOW")
    plt.grid()

    plt.subplot(2,2,3)
    plt.scatter(dt.MTOW33, dt.b, c="m")
    plt.plot(dt.MTOW33, dt.Func_b5(dt.MTOW33), 'r-')
    plt.scatter([mtow_int], [b_est5], c="b")
    plt.title("Envergadura vs MTOW")
    plt.grid()

    plt.subplot(2,2,4)
    plt.scatter(dt.MTOW33, dt.Alargamiento, c="m")
    plt.plot(dt.MTOW33, dt.Func_Al5(dt.MTOW33), 'r-')
    plt.scatter([mtow_int], [Al_est5], c="b")
    plt.title("Alargamiento vs MTOW")
    plt.grid()

    fig5.tight_layout()
    figuras.append(fig5)

    # -----------------------------------------
    # Resultados devueltos a GUI
    # -----------------------------------------
    resultados = {
        "Pasajeros iniciales": cant_pas_ini,
        "Filas base": filas_base_int,
        "Hileras base": hileras_base_int,
        "Pasillos base": pasillos_base_int,
        "Filas extra": filas_extra_int,
        "Pasajeros totales": pasajeros_nuevos,
        "MTOW estimado": mtow_int,
        "OEW estimado": oew_int,
        "Carga útil": cu_int,
        "Peso combustible": PC_int,
        "LCC": LCC_est,
        "LN": LN_est,
        "L_Cab": LCab_est,
        "Carga alar": Carga_est5,
        "Superficie alar": Sw_est5,
        "Envergadura": b_est5,
        "Alargamiento": Al_est5
    }

    return resultados, figuras
