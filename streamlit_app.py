import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Título de la aplicación
st.title("🎈 Proyecto Analítica")
st.write("Por favor, contesta las siguientes preguntas para obtener una predicción:")

# Ruta al archivo del modelo .pkl
model_path = "modelo_random_forest_analiticaFinal.pkl"  # Replace with the correct path

import os
import pickle

# Define the relative path to the model file
model_path = "modelo_random_forest_analiticaFinal.pkl"

# Check if the file exists
if os.path.exists(model_path):
    try:
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
            print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")
else:
    print(f"File {model_path} does not exist!")


# Definir las columnas numéricas y categóricas
num_cols = ['Activ_Econ', 'Ventas_Nacion19', 'Export_2019', 'Ventas_Nacion20',
            'Export_2020', 'Bienes_Ctes', 'Razon_No_Proy', 'Average_Cert_Employ19', 
            'Average_Cert_Employ20']

cat_cols = ['Tipo', 'Bienes_Nuev_Emp', 'Bienes_Nuev_Nacion', 'Bienes_Nuev_Inter',
            'Bienes_Mejor_Emp', 'Bienes_Mejor_Nacion', 'Bienes_Mejor_Inter',
            'Metod_Nuev_Prod', 'Metod_Nuev_Emp', 'Tec_Comerce_Nuev',
            'Metod_Nuev_Dist', 'Metod_Nuev_Info', 'Metod_Nuev_Conta',
            'Ventas_NacionTotal', 'Proy_Bienes_Nuev', 'Abandono_Proy',
            'Intencion_Proy', 'Cert_Quali_Process', 'Cert_Quali_Product',
            'Reglamento']

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

# Preguntas para los datos categóricos
categorical_inputs_restricted = {
    "Bienes_Nuev_Emp": "¿Introdujo bienes nuevos al mercado? (Sí=1, No=2)",
    "Bienes_Nuev_Nacion": "¿Introdujo bienes nuevos en el mercado nacional? (Sí=1, No=2)",
    # Añadir más preguntas categóricas restringidas
}

# Preguntas categóricas sin restricciones
categorical_inputs_unrestricted = {
    "Tipo": "¿Cuál es la tipología de la empresa? (AMPLIA, NOINNO, POTENC, INTENC, ESTRIC)",
    "Ventas_NacionTotal": "¿Porcentaje total de ventas nacionales de la empresa? (0 a 1)"
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
    for col, question in categorical_inputs_restricted.items():
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
    # Realizar la predicción
    prediction = model.predict(input_df)
    st.write(f"La predicción es: {prediction[0]}")
