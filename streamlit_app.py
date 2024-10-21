import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os

# Título de la aplicación
st.title("🎈 Proyecto Analítica")
st.write("Por favor, contesta las siguientes preguntas para obtener una predicción:")

# Ruta al archivo del modelo .pkl
model_path = "modelo_random_forest_analiticaFinal.pkl"  # Replace with the correct path

# Check if the file exists
if os.path.exists(model_path):
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
            st.success("Modelo cargado exitosamente!")
    except Exception as e:
        st.error(f"Error al cargar el modelo: {e}")
else:
    st.error(f"El archivo {model_path} no existe!")

# Definir las columnas numéricas
num_cols = ['Activ_Econ', 'Ventas_Nacion19', 'Export_2019', 'Ventas_Nacion20',
            'Export_2020', 'Bienes_Ctes', 'Razon_No_Proy', 'Average_Cert_Employ19', 
            'Average_Cert_Employ20']

# Preguntas para los datos numéricos
numerical_inputs = [
    ("Activ_Econ", "Código de la actividad económica principal de la empresa", 0),
    ("Ventas_Nacion19", "Ingresos/ventas totales en el mercado nacional 2019 (en miles de pesos)", 0),
    ("Export_2019", "Exportaciones totales de la empresa en 2019 (en miles de pesos)", 0),
    ("Ventas_Nacion20", "Ingresos/ventas totales en el mercado nacional 2020 (en miles de pesos)", 0),
    ("Export_2020", "Exportaciones totales de la empresa en 2020 (en miles de pesos)", 0),
    ("Bienes_Ctes", "Porcentaje de ventas nacionales de bienes o servicios que no cambiaron (0 a 1)", 0.0, 0.0, 1.0),
    ("Razon_No_Proy", "Razón principal por la cual no introdujo innovaciones (1 a 12)", 1, 1, 12),
    ("Average_Cert_Employ19", "Empleados con certificaciones laborales en 2019", 0),
    ("Average_Cert_Employ20", "Empleados con certificaciones laborales en 2020", 0)
]

# Preguntas personalizadas para datos categóricos con restricciones de respuesta (Sí=1, No=2)
categorical_questions_restricted = {
    "Bienes_Nuev_Emp": "¿Introdujo su empresa bienes o servicios nuevos que ya existían en el mercado nacional o internacional, pero eran nuevos para la empresa durante el período 2019-2020? (Sí=1, No=2)",
    "Bienes_Nuev_Nacion": "¿Introdujo su empresa bienes o servicios nuevos en el mercado nacional durante el período 2019-2020? (Sí=1, No=2)",
    "Bienes_Nuev_Inter": "¿Introdujo su empresa bienes o servicios nuevos en el mercado internacional durante el período 2019-2020? (Sí=1, No=2)",
    "Bienes_Mejor_Emp": "¿Introdujo su empresa mejoras a bienes o servicios que ya existían en el mercado, pero que fueron mejorados solo para la empresa? (Sí=1, No=2)",
    "Bienes_Mejor_Nacion": "¿Introdujo su empresa mejoras a bienes o servicios en el mercado nacional durante el período 2019-2020? (Sí=1, No=2)",
    "Bienes_Mejor_Inter": "¿Introdujo su empresa mejoras a bienes o servicios en el mercado internacional durante el período 2019-2020? (Sí=1, No=2)",
    "Metod_Nuev_Prod": "¿Introdujo su empresa métodos nuevos o mejorados de producción de bienes o prestación de servicios durante el período 2019-2020? (Sí=1, No=2)",
    "Metod_Nuev_Emp": "¿Implementó su empresa métodos organizativos nuevos o mejorados en su funcionamiento interno durante el período 2019-2020? (Sí=1, No=2)",
    "Tec_Comerce_Nuev": "¿Introdujo su empresa técnicas de comercialización nuevas o mejoradas durante el período 2019-2020? (Sí=1, No=2)",
    "Metod_Nuev_Dist": "¿Implementó su empresa métodos nuevos o mejorados de distribución, entrega o logística durante el período 2019-2020? (Sí=1, No=2)",
    "Metod_Nuev_Info": "¿Introdujo su empresa métodos nuevos o mejorados de procesamiento de información o comunicación durante el período 2019-2020? (Sí=1, No=2)",
    "Metod_Nuev_Conta": "¿Introdujo su empresa métodos nuevos o mejorados para la contabilidad u operaciones administrativas durante el período 2019-2020? (Sí=1, No=2)",
    "Proy_Bienes_Nuev": "¿Tenía su empresa algún proyecto en marcha para introducir bienes o servicios nuevos o mejorados al finalizar 2020? (Sí=1, No=2)",
    "Abandono_Proy": "¿Abandonó su empresa algún proyecto de innovación durante el período 2019-2020? (Sí=1, No=2)",
    "Intencion_Proy": "¿Tuvo su empresa la intención de realizar algún proyecto de innovación durante el período 2019-2020? (Sí=1, No=2)",
    "Cert_Quali_Process": "¿Obtuvo su empresa certificaciones de calidad de procesos durante el período 2019-2020? (Sí=1, No=2)",
    "Cert_Quali_Product": "¿Obtuvo su empresa certificaciones de calidad de productos durante el período 2019-2020? (Sí=1, No=2)",
    "Reglamento": "¿Estuvieron los bienes o servicios de su empresa sujetos a reglamentos técnicos durante el período 2019-2020? (Sí=1, No=2)"
}

# Definir preguntas categóricas sin restricciones
categorical_inputs_unrestricted = {
    "Tipo": "Seleccione el tipo de empresa",
    "Ventas_NacionTotal": "Porcentaje de ventas nacionales de bienes o servicios totales (0 a 1)"
}

# Función para obtener entradas numéricas
def get_numerical_input():
    data = {}
    for col, question, default, *limits in numerical_inputs:
        if limits:  # Casos donde hay un rango de valores
            data[col] = st.number_input(question, min_value=limits[0], max_value=limits[1], value=default)
        else:
            data[col] = st.number_input(question, value=default)
    return data

# Función para obtener entradas categóricas restringidas (Sí=1, No=2)
def get_categorical_input_restricted():
    data = {}
    for col, question in categorical_questions_restricted.items():
        data[col] = st.selectbox(question, options=[1, 2])
    return data

# Función para obtener entradas categóricas sin restricciones
def get_categorical_input_unrestricted():
    data = {}
    for col, question in categorical_inputs_unrestricted.items():
        if col == 'Tipo':
            data[col] = st.selectbox(question, options=['AMPLIA', 'NOINNO', 'POTENC', 'INTENC', 'ESTRIC'])
        elif col == 'Ventas_NacionTotal':
            data[col] = st.number_input(question, min_value=0.0, max_value=1.0, value=0.0)
    return data

# Recolectar los datos de entrada
numerical_data = get_numerical_input()
categorical_data_restricted = get_categorical_input_restricted()
categorical_data_unrestricted = get_categorical_input_unrestricted()

# Unir todos los datos en un solo DataFrame
input_data = {**numerical_data, **categorical_data_restricted, **categorical_data_unrestricted}
input_df = pd.DataFrame([input_data])

# Botón para hacer la predicción
if st.button("Hacer Predicción"):
    # Debugging: Check input_df before prediction
    st.write("Estructura de input_df:")
    st.write(input_df)

    try:
        # Realizar la predicción
        prediction = model.predict(input_df)
        st.write(f"La predicción es: {prediction[0]}")
    except Exception as e:
        st.error(f"Error durante la predicción: {e}")
