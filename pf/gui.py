import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import puntos_resueltos_B as prB
import funciones as fa
import datos as dt
from datetime import datetime
import re
import numpy as np

# -------------------------------------------------------------------
# ------------------------- ESTILO MODERNO ---------------------------
# -------------------------------------------------------------------

AZUL_OSCURO = "#0A3D62"
AZUL = "#1B9CFC"
AZUL_CLARO = "#74b9ff"
BLANCO = "#ffffff"
GRIS = "#f0f0f0"

ESTILO_FUENTE = ("Segoe UI", 11)
TITULO_FUENTE = ("Segoe UI", 20, "bold")
SUBTITULO_FUENTE = ("Segoe UI", 11, "italic")


class ScrollableFigures(tk.Frame):
    """Frame scrolleable para mostrar múltiples figuras de Matplotlib."""
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        canvas = tk.Canvas(self, borderwidth=0, bg=GRIS)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.fig_frame = tk.Frame(canvas, bg=GRIS)

        self.fig_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.fig_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas = canvas

    def clear(self):
        for widget in self.fig_frame.winfo_children():
            widget.destroy()


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # ------------------------------
        # Estética principal
        # ------------------------------
        self.title("DyRATools")
        self.configure(bg=GRIS)
        self.geometry("1200x850")

        # Evitar múltiples ventanas del menú / ejecutar todo
        self.menu_puntos_win = None
        self.ejecutar_todo_win = None

        # Validator registro para evitar letras y negativos
        self._vcmd = (self.register(self._validate_key), '%P')

        # ------------------------------
        # TITULO Y DESCRIPCIÓN
        # ------------------------------
        titulo = tk.Label(self, text="DyRATools", fg=AZUL_OSCURO, bg=GRIS, font=TITULO_FUENTE)
        titulo.pack(pady=(10, 0))

        descripcion = tk.Label(
            self,
            text="Este ejecutable es una herramienta de cálculo para el diseño de una aeronave con bases estadísticas.\n"
                 "Esperemos le sea de ayuda.",
            fg=AZUL_OSCURO, bg=GRIS, font=SUBTITULO_FUENTE
        )
        descripcion.pack(pady=(0, 15))

        # ------------------------------
        # BOTONES SUPERIORES
        # ------------------------------
        btn_frame = tk.Frame(self, bg=GRIS)
        btn_frame.pack(pady=10)

        estilo_boton = {"font": ESTILO_FUENTE, "bg": AZUL, "fg": BLANCO,
                        "activebackground": AZUL_OSCURO, "activeforeground": BLANCO,
                        "bd": 0, "relief": "flat", "padx": 12, "pady": 6}

        tk.Button(btn_frame, text="Ejecutar TODO", command=self.ejecutar_todo, **estilo_boton).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Menú Puntos", command=self.mostrar_menu, **estilo_boton).grid(row=0, column=1, padx=10)

        tk.Button(self, text="Guardar resultados en TXT", command=self.guardar_txt, **estilo_boton).pack(pady=10)

        # ------------------------------
        # CONTENEDOR SCROLLEABLE
        # ------------------------------
        self.scroll_figs = ScrollableFigures(self, bg=GRIS)
        self.scroll_figs.pack(fill="both", expand=True)

        self.resultados_frame = None
        self.resultados_obtenidos = None

    # -------------------------
    # Validator
    # -------------------------
    def _validate_key(self, proposed: str):
        if proposed == "":
            return True
        return re.match(r'^\d*\.?\d*$', proposed) is not None

    # -------------------------
    # Min/Max por parámetro
    # -------------------------
    def _get_min_max_for_param(self, param_name: str):

        p = param_name.lower()

        def arr_minmax(candidates):
            for c in candidates:
                if hasattr(dt, c):
                    arr = np.asarray(getattr(dt, c), dtype=float)
                    return float(np.nanmin(arr)), float(np.nanmax(arr))
            return 0.0, float(np.nanmax(dt.Pasajeros))

        if "pas" in p:
            return arr_minmax(["Pasajeros"])
        if "filas" in p:
            return arr_minmax(["FilasAsientos"])
        if "hiler" in p:
            return arr_minmax(["HilerasAsientos"])
        if "diam" in p:
            return arr_minmax(["DiametroMedio"])
        if "mtow" in p:
            return arr_minmax(["MTOW"])
        if "oew" in p:
            return arr_minmax(["OEW"])
        if "carga" in p:
            return arr_minmax(["CU"])
        if "comb" in p:
            return arr_minmax(["Peso_Comb"])
        return arr_minmax(["Pasajeros"])

    # -------------------------
    # Ejecutar TODO
    # -------------------------
    def ejecutar_todo(self):
        if self.ejecutar_todo_win and self.ejecutar_todo_win.winfo_exists():
            self.ejecutar_todo_win.lift()
            return

        self.ejecutar_todo_win = tk.Toplevel(self)
        win = self.ejecutar_todo_win
        win.title("Ejecutar TODO")
        win.configure(bg=GRIS)

        labels = [("Pasajeros iniciales", "cant_pas_ini"),
                  ("Filas extra", "filas_extra"),
                  ("Diámetro", "diam_in")]

        entries = []
        entry_keys = []

        for texto, key in labels:
            frame = tk.Frame(win, bg=GRIS)
            frame.pack(pady=5)

            tk.Label(frame, text=texto + ":", bg=GRIS, fg=AZUL_OSCURO, font=ESTILO_FUENTE).pack(side="left")

            entry = tk.Entry(frame, validate="key", validatecommand=self._vcmd)
            entry.pack(side="left", padx=5)

            if key != "filas_extra":
                mn, mx = self._get_min_max_for_param(key)
                entry._min_val = mn
                entry._max_val = mx
                tk.Label(frame, text=f"(min {mn:.0f}, max {mx:.0f})", bg=GRIS, fg=AZUL_OSCURO).pack(side="left")
            else:
                entry._min_val = None
                entry._max_val = None

            entries.append(entry)
            entry_keys.append(key)

        def run():
            vals = {}
            for entry, key in zip(entries, entry_keys):
                txt = entry.get().strip()
                if txt == "":
                    messagebox.showerror("Error", "Todos los campos deben completarse")
                    return

                val = float(txt)
                if val < 0:
                    messagebox.showerror("Error", "No se permiten valores negativos")
                    return

                if key != "filas_extra":
                    if val < entry._min_val or val > entry._max_val:
                        messagebox.showerror("Error", f"{key} fuera de rango")
                        return

                vals[key] = val

            pas_ini = vals["cant_pas_ini"]
            filas_extra = vals["filas_extra"]

            filas_base = dt.Func_Filas(pas_ini)
            max_fil = float(np.nanmax(dt.FilasAsientos))
            if int(round(filas_base)) + int(round(filas_extra)) > max_fil:
                messagebox.showerror("Error", "La suma filas_base + filas_extra excede el máximo permitido")
                return

            resultados, figuras = prB.ejecutar_todo_B(str(pas_ini), str(filas_extra), str(vals["diam_in"]))
            self.resultados_obtenidos = resultados

            self.mostrar_figuras(figuras)
            self.mostrar_resultados(resultados)

            win.destroy()
            self.ejecutar_todo_win = None

        tk.Button(win, text="Ejecutar", command=run, bg=AZUL, fg=BLANCO).pack(pady=10)

    # -------------------------
    # Menú puntos
    # -------------------------
    def mostrar_menu(self):
        if self.menu_puntos_win and self.menu_puntos_win.winfo_exists():
            self.menu_puntos_win.lift()
            return

        win = tk.Toplevel(self)
        self.menu_puntos_win = win
        win.title("Menú de puntos")
        win.configure(bg=GRIS)

        opciones = [
            ("Punto 1", lambda: self.ejecutar_punto(prB.punto_1_B)),
            ("Punto 2", lambda: self.ejecutar_punto(prB.punto_2_B)),
            ("Punto 3", lambda: self.ejecutar_punto(prB.punto_3_B)),
            ("Punto 4", lambda: self.ejecutar_punto(prB.punto_4_B)),
            ("Punto 5", lambda: self.ejecutar_punto(prB.punto_5_B)),
        ]

        for lab, f in opciones:
            tk.Button(win, text=lab, command=f,
                      bg=AZUL, fg=BLANCO, font=ESTILO_FUENTE,
                      activebackground=AZUL_OSCURO).pack(pady=5)

    # -------------------------
    # Ejecutar punto
    # -------------------------
    def ejecutar_punto(self, funcion):
        if hasattr(self, "_param_win") and self._param_win and self._param_win.winfo_exists():
            self._param_win.lift()
            return

        win = tk.Toplevel(self)
        self._param_win = win
        win.title(funcion.__name__)
        win.configure(bg=GRIS)

        entradas_meta = []

        params = funcion.__code__.co_varnames[:funcion.__code__.co_argcount]

        for param in params:
            frame = tk.Frame(win, bg=GRIS)
            frame.pack(pady=5)

            tk.Label(frame, text=param + ":", bg=GRIS, fg=AZUL_OSCURO).pack(side="left")

            entry = tk.Entry(frame, validate="key", validatecommand=self._vcmd)
            entry.pack(side="left", padx=5)

            if param == "filas_extra":
                entry._min_val = None
                entry._max_val = None
            else:
                mn, mx = self._get_min_max_for_param(param)
                entry._min_val = mn
                entry._max_val = mx
                tk.Label(frame, text=f"(min {mn:.0f}, max {mx:.0f})", bg=GRIS, fg=AZUL_OSCURO).pack(side="left")

            entradas_meta.append((entry, param))

        def run():
            valores = {}
            args = []

            for entry, param in entradas_meta:
                txt = entry.get().strip()
                if txt == "":
                    messagebox.showerror("Error", f"Falta valor para {param}")
                    return
                val = float(txt)
                if val < 0:
                    messagebox.showerror("Error", "No se permiten negativos")
                    return
                if param != "filas_extra":
                    if val < entry._min_val or val > entry._max_val:
                        messagebox.showerror("Error", f"{param} fuera de rango")
                        return

                valores[param] = val
                args.append(txt)

            if "filas_extra" in valores:
                pas_key = None
                for p in params:
                    if "pas" in p:
                        pas_key = p
                        break

                pas_ini = valores[pas_key]
                filas_base = dt.Func_Filas(pas_ini)
                maxfil = float(np.nanmax(dt.FilasAsientos))
                if int(round(filas_base)) + int(round(valores["filas_extra"])) > maxfil:
                    messagebox.showerror("Error", "La suma de filas_base + filas_extra excede el máximo")
                    return

            resultados, figs = funcion(*args)
            self.resultados_obtenidos = resultados
            self.mostrar_figuras(figs)
            self.mostrar_resultados(resultados)

            win.destroy()
            self._param_win = None

        tk.Button(win, text="Ejecutar", command=run, bg=AZUL, fg=BLANCO).pack(pady=10)

    # -------------------------
    # Mostrar figuras
    # -------------------------
    def mostrar_figuras(self, figuras):
        self.scroll_figs.clear()

        for fig in figuras:
            try:
                fig.set_size_inches(10, 6)
                fig.tight_layout(pad=3)
                fig.subplots_adjust(bottom=0.2, hspace=0.6)
            except:
                pass

            canvas = FigureCanvasTkAgg(fig, master=self.scroll_figs.fig_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(padx=20, pady=20)

    # -------------------------
    # Mostrar resultados
    # -------------------------
    def mostrar_resultados(self, resultados):
        if self.resultados_frame and self.resultados_frame.winfo_exists():
            self.resultados_frame.destroy()

        self.resultados_frame = tk.Frame(self.scroll_figs.fig_frame, bg=GRIS)
        self.resultados_frame.pack(fill="x", pady=10)

        tk.Label(self.resultados_frame, text="RESULTADOS:", fg=AZUL_OSCURO,
                 bg=GRIS, font=("Segoe UI", 14, "bold")).pack()

        for k, v in resultados.items():
            tk.Label(self.resultados_frame, text=f"{k}: {v}", bg=GRIS,
                     fg=AZUL_OSCURO, anchor="w").pack(fill="x")

    # -------------------------
    # Guardar TXT
    # -------------------------
    def guardar_txt(self):
        if not self.resultados_obtenidos:
            messagebox.showwarning("Aviso", "Debe ejecutar algo primero")
            return

        nombre = "resultados_" + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt"

        filepath = filedialog.asksaveasfilename(
            initialfile=nombre,
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")]
        )
        if not filepath:
            return

        with open(filepath, "w", encoding="utf-8") as f:
            for k, v in self.resultados_obtenidos.items():
                f.write(f"{k}: {v}\n")

        messagebox.showinfo("OK", "Archivo guardado exitosamente")


if __name__ == "__main__":
    App().mainloop()
