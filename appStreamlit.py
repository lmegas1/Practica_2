"""
app.py — Servicio web Streamlit
Predictor de aprobación de carrera universitaria

Consume el modelo registrado en MLflow Model Registry.

Requisitos previos:
    1. MLflow corriendo en http://localhost:9090
       mlflow server --backend-store-uri sqlite:///mlflow.db --host 0.0.0.0 --port 9090

    2. Modelo registrado en MLflow como "arbolesCarrera01" en stage Production
       (se registra ejecutando el notebook 4_ejemplo-arbol-carreras-pipeline-mlflow.ipynb)

Inicio:
    pip install streamlit mlflow scikit-learn pandas
    streamlit run app.py
"""

import pandas as pd
import mlflow
import mlflow.sklearn
import streamlit as st

# ── Configuración MLflow ─────────────────────────────────────
MLFLOW_URI  = "http://127.0.0.1:9090"
# Cambie la versión si MLflow registra una nueva versión del modelo:
#http://127.0.0.1:9090/#/models/arbolesCarrera01/versions/1
MODEL_URI = "models:/arbolesCarrera01/1"

# ── Opciones del formulario (igual que el CSV) ───────────────
CARRERAS    = ["Arquitectura", "Computacion", "Derecho",
               "Economia", "Industrial", "Medicina"]
MODALIDADES = ["Hibrida", "Presencial", "Virtual"]
BECAS       = ["Si", "No"]


# ════════════════════════════════════════════════════════════
# Carga del modelo (con caché para no recargar en cada render)
# ════════════════════════════════════════════════════════════
@st.cache_resource(show_spinner="Cargando modelo desde MLflow...")
def cargar_modelo():
    mlflow.set_tracking_uri(MLFLOW_URI)
    try:
        modelo = mlflow.sklearn.load_model(MODEL_URI)
        return modelo, None
    except Exception as e:
        return None, str(e)


# ════════════════════════════════════════════════════════════
# Interfaz Streamlit
# ════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Predictor de Aprobacion",
    page_icon="🎓",
    layout="centered"
)

# ── Encabezado ───────────────────────────────────────────────
st.title("🎓 Predictor de Aprobación de Carrera")
st.markdown(
    "Completa los datos del estudiante y el modelo de "
    "**Árbol de Decisión** predecirá si aprobará o no la carrera."
)
st.divider()

# ── Carga del modelo ─────────────────────────────────────────
modelo, error = cargar_modelo()

if error:
    st.error(
        f"❌ No se pudo cargar el modelo desde MLflow.\n\n"
        f"**Causa:** {error}\n\n"
        "**Verifica que:**\n"
        f"- MLflow esté corriendo en `{MLFLOW_URI}`\n"
        f"- El modelo `{MODEL_URI}` esté en stage **Production**"
    )
    st.stop()

st.success(f"✅ Modelo `{MODEL_URI}` cargado correctamente desde MLflow.")
st.divider()

# ── Formulario de entrada ─────────────────────────────────────
st.subheader("📋 Datos del estudiante")

col1, col2 = st.columns(2)

with col1:
    carrera   = st.selectbox("Carrera",       CARRERAS)
    modalidad = st.selectbox("Modalidad",     MODALIDADES)
    beca      = st.selectbox("¿Tiene beca?",  BECAS)

with col2:
    edad        = st.number_input("Edad",
                                  min_value=16, max_value=60,
                                  value=22, step=1)
    asistencias = st.number_input("Asistencias (%)",
                                  min_value=0, max_value=100,
                                  value=75, step=1)

st.divider()

# ── Predicción ───────────────────────────────────────────────
if st.button("🔮 Predecir aprobación", use_container_width=True, type="primary"):

    # DataFrame con las mismas columnas que X del notebook
    # Nota: 'promedio' se excluyó en el entrenamiento
    entrada = pd.DataFrame([{
        "carrera":     carrera,
        "modalidad":   modalidad,
        "beca":        beca,
        "edad":        int(edad),
        "asistencias": int(asistencias),
    }])

    try:
        prediccion   = int(modelo.predict(entrada)[0])
        probabilidad = modelo.predict_proba(entrada)[0]

        prob_aprueba  = probabilidad[1]
        prob_reprueba = probabilidad[0]

        st.subheader("📊 Resultado")

        if prediccion == 1:
            st.success("## ✅ APROBADO")
        else:
            st.error("## ❌ NO APROBADO")

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("✅ Probabilidad de aprobar",    f"{prob_aprueba*100:.1f}%")
        with col_b:
            st.metric("❌ Probabilidad de no aprobar", f"{prob_reprueba*100:.1f}%")

        st.progress(float(prob_aprueba))

        with st.expander("🔍 Ver datos ingresados"):
            st.dataframe(entrada, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"❌ Error al realizar la predicción: {e}")

# ── Pie de página ─────────────────────────────────────────────
st.divider()
st.caption(
    f"Modelo: `{MODEL_URI}` "
    f"MLflow: [{MLFLOW_URI}]({MLFLOW_URI})"
)
