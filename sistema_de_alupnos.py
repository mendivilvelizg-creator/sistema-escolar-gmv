import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import matplotlib.pyplot as plt

# Crear carpeta
os.makedirs("registro", exist_ok=True)

# ------------------------
# Registrar
# ------------------------
def registrar():

    usuario = usuario_entry.get().strip()
    nombre = nombre_entry.get().strip()

    if usuario == "" or nombre == "":
        messagebox.showerror("Error", "Complete los datos")
        return

    try:
        promedio = float(promedio_entry.get())

        if promedio < 0 or promedio > 10:
            raise ValueError

    except:
        messagebox.showerror("Error", "Promedio inválido")
        return

    archivo = f"registro/{usuario}.txt"

    with open(archivo, "w", encoding="utf-8") as f:
        f.write(f"Usuario:{usuario}\n")
        f.write(f"Nombre:{nombre}\n")
        f.write(f"Promedio:{promedio}\n")

    messagebox.showinfo("Éxito", "Alumno guardado")

# ------------------------
# Ver alumnos
# ------------------------
def ver_alumnos():

    texto.delete("1.0", tk.END)

    archivos = os.listdir("registro")

    if len(archivos) == 0:
        texto.insert(tk.END, "No hay alumnos registrados")
        return

    for archivo in archivos:
        texto.insert(
            tk.END,
            archivo.replace(".txt", "") + "\n"
        )

# ------------------------
# Buscar alumno
# ------------------------
def buscar():

    usuario = simpledialog.askstring(
        "Buscar",
        "Usuario:"
    )

    if not usuario:
        return

    archivo = f"registro/{usuario}.txt"

    if not os.path.exists(archivo):
        messagebox.showerror(
            "Error",
            "Alumno no encontrado"
        )
        return

    with open(archivo, encoding="utf-8") as f:
        datos = f.read()

    texto.delete("1.0", tk.END)
    texto.insert(tk.END, datos)

# ------------------------
# Ranking
# ------------------------
def ranking():

    alumnos = []

    for archivo in os.listdir("registro"):

        ruta = f"registro/{archivo}"

        try:

            nombre = ""
            promedio = 0

            with open(ruta, encoding="utf-8") as f:

                for linea in f:

                    if linea.startswith("Nombre:"):
                        nombre = linea.replace(
                            "Nombre:",
                            ""
                        ).strip()

                    if linea.startswith("Promedio:"):
                        promedio = float(
                            linea.replace(
                                "Promedio:",
                                ""
                            ).strip()
                        )

            alumnos.append(
                (nombre, promedio)
            )

        except:
            pass

    alumnos.sort(
        key=lambda x: x[1],
        reverse=True
    )

    texto.delete("1.0", tk.END)

    texto.insert(
        tk.END,
        "RANKING DE PROMEDIOS\n\n"
    )

    posicion = 1

    for nombre, promedio in alumnos:

        texto.insert(
            tk.END,
            f"{posicion}. {nombre} - {promedio}\n"
        )

        posicion += 1

# ------------------------
# Gráfica
# ------------------------
def grafica():

    nombres = []
    promedios = []
    colores = []

    for archivo in os.listdir("registro"):

        ruta = f"registro/{archivo}"

        try:

            nombre = ""
            promedio = 0

            with open(ruta, encoding="utf-8") as f:

                for linea in f:

                    if linea.startswith("Nombre:"):
                        nombre = linea.replace(
                            "Nombre:",
                            ""
                        ).strip()

                    if linea.startswith("Promedio:"):
                        promedio = float(
                            linea.replace(
                                "Promedio:",
                                ""
                            ).strip()
                        )

            nombres.append(nombre)
            promedios.append(promedio)

            if promedio >= 9:
                colores.append("green")
            elif promedio >= 7:
                colores.append("orange")
            else:
                colores.append("red")

        except:
            pass

    if len(nombres) == 0:
        messagebox.showerror(
            "Error",
            "No hay alumnos"
        )
        return

    plt.figure(figsize=(8,4))
    plt.bar(
        nombres,
        promedios,
        color=colores
    )

    plt.ylim(0,10)
    plt.title("Promedios")
    plt.ylabel("Calificación")
    plt.show()

# ------------------------
# Ventana
# ------------------------

ventana = tk.Tk()
ventana.title("Sistema Escolar")
ventana.geometry("700x500")

titulo = tk.Label(
    ventana,
    text="SISTEMA ESCOLAR",
    font=("Arial", 18, "bold")
)
titulo.pack(pady=10)

tk.Label(
    ventana,
    text="Usuario"
).pack()

usuario_entry = tk.Entry(
    ventana,
    width=30
)
usuario_entry.pack()

tk.Label(
    ventana,
    text="Nombre"
).pack()

nombre_entry = tk.Entry(
    ventana,
    width=30
)
nombre_entry.pack()

tk.Label(
    ventana,
    text="Promedio"
).pack()

promedio_entry = tk.Entry(
    ventana,
    width=30
)
promedio_entry.pack()

tk.Button(
    ventana,
    text="Registrar Alumno",
    command=registrar
).pack(pady=3)

tk.Button(
    ventana,
    text="Ver Alumnos",
    command=ver_alumnos
).pack(pady=3)

tk.Button(
    ventana,
    text="Buscar Alumno",
    command=buscar
).pack(pady=3)

tk.Button(
    ventana,
    text="Ranking",
    command=ranking
).pack(pady=3)

tk.Button(
    ventana,
    text="Ver Gráfica",
    command=grafica
).pack(pady=3)

texto = tk.Text(
    ventana,
    height=12,
    width=70
)
texto.pack(
    pady=10,
    padx=10
)

ventana.mainloop()