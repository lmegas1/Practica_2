import pandas as pd
import random

# =====================================================
# Configuración para reproducibilidad
# =====================================================

random.seed(42)

# =====================================================
# Valores posibles
# =====================================================

carreras = [
    "Computacion",
    "Derecho",
    "Economia",
    "Medicina",
    "Arquitectura",
    "Industrial"
]

modalidades = [
    "Presencial",
    "Virtual",
    "Hibrida"
]

becas = [
    "Si",
    "No"
]

# =====================================================
# Lista donde se almacenarán los registros
# =====================================================

datos = []

# =====================================================
# Generación de 1000 registros
# =====================================================

for i in range(5000):

    # -----------------------------------------
    # Variables categóricas
    # -----------------------------------------

    carrera = random.choice(carreras)

    modalidad = random.choice(modalidades)

    beca = random.choice(becas)

    # -----------------------------------------
    # Edad
    # -----------------------------------------

    edad = random.randint(18, 30)

    # -----------------------------------------
    # Promedio base
    # -----------------------------------------

    promedio = round(random.uniform(4.0, 10.0), 1)

    # -----------------------------------------
    # Asistencias base
    # -----------------------------------------

    asistencias = random.randint(50, 100)

    # =================================================
    # Reglas coherentes para dar realismo
    # =================================================

    # Medicina suele tener estudiantes
    # con más asistencia

    if carrera == "Medicina":
        asistencias = asistencias + random.randint(5, 15)

    # Virtual suele reducir asistencia

    if modalidad == "Virtual":
        asistencias = asistencias - random.randint(5, 20)

    # Tener beca suele mejorar ligeramente
    # el promedio

    if beca == "Si":
        promedio = promedio + round(random.uniform(0.0, 0.8), 1)

    # -----------------------------------------
    # Limitar rangos
    # -----------------------------------------

    if asistencias > 100:
        asistencias = 100

    if asistencias < 0:
        asistencias = 0

    if promedio > 10:
        promedio = 10

    # =================================================
    # Variable objetivo con algo de ruido
    # =================================================

    probabilidad = random.random()

    aprobado = "Si"

    # Casos claramente reprobados

    if promedio < 5.5:
        aprobado = "No"

    elif asistencias < 60:
        aprobado = "No"

    # Casos ambiguos

    elif promedio < 7 and probabilidad > 0.4:
        aprobado = "No"

    elif asistencias < 75 and probabilidad > 0.6:
        aprobado = "No"

    # Algunos casos excepcionales

    elif promedio > 9 and asistencias > 90:
        aprobado = "Si"

    # =================================================
    # Guardar registro
    # =================================================

    datos.append([
        carrera,
        modalidad,
        beca,
        edad,
        promedio,
        asistencias,
        aprobado
    ])

# =====================================================
# Crear DataFrame
# =====================================================

df = pd.DataFrame(
    datos,
    columns=[
        "carrera",
        "modalidad",
        "beca",
        "edad",
        "promedio",
        "asistencias",
        "aprobado"
    ]
)

# =====================================================
# Guardar CSV
# =====================================================

df.to_csv(
    "data/estudiantes.csv",
    index=False
)

# =====================================================
# Mostrar información
# =====================================================

print(df.head())

print("\nTamaño del dataset:")
print(df.shape)

print("\nDistribución de aprobados:")
print(df["aprobado"].value_counts())
