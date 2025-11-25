import datos as dt
import funciones as fa

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
