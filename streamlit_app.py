import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns



# Título de la aplicación
st.title("📈 Profit Pulse")
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

# Load training data
data_path = os.path.join(os.path.dirname(__file__), 'BasedeDatosCorte2.xlsx')
training_data = pd.read_excel(data_path)

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

if 'porcentaje_cambio' not in training_data.columns:
    training_data['porcentaje_cambio'] = np.nan  # Add as NaN if not prese
print(training_data['porcentaje_cambio'].dtype)

# Botón para hacer la predicción
if st.button("Hacer Predicción"):
    # Debugging: Check input_df before prediction
    st.write("Estructura de input_df:")
    st.write(input_df)

    try:
        # Realizar la predicción
        prediction = model.predict(input_df)
        st.write(f"La predicción es: {prediction[0]}")

        # Plot `porcentaje_cambio` prediction vs. training data
        if 'porcentaje_cambio' in training_data.columns:
            fig, ax = plt.subplots()
            sns.violinplot(x=training_data['porcentaje_cambio'], ax=ax, inner=None, color="skyblue")
            
            # Overlay the predicted value as a red point
            ax.plot(prediction[0], 1, 'ro', label='Predicción (User Input)')
            st.header('Comparación de Usuario vs Empresas que reportaron una variación positiva en ingresos')

            ax.set_title("Comparación de variacion entre el usuario y la otras empresas")
            ax.set_xlabel("porcentaje_cambio")
            ax.legend()
            
            st.pyplot(fig)
        else:
            st.error("La columna 'porcentaje_cambio' no se encuentra en los datos de entrenamiento.")
    except Exception as e:
        st.error(f"Error durante la predicción: {e}")

# Create comparison for important features
st.header('Comparación con Otras Empresas')

columns_to_compare = ['Ventas_Nacion19', 'Export_2019', 'Average_Cert_Employ19','Export_2020']

# Plotting boxplot with user input as points
st.header('Comparación de Usuario vs Distribución de la Base de Datos Original')

# Iterate over each column to plot in a 2x2 layout
for i, col_name in enumerate(columns_to_compare):
    # Create a new row with 2 columns for every two plots
    if i % 2 == 0:
        col1, col2 = st.columns(2)
    columns = [col1, col2]
    
    # Create the plot
    fig, ax = plt.subplots()
    
    # Violin plot for the training data
    sns.violinplot(x=training_data[col_name], ax=ax, inner=None, color="skyblue")
    
    # Overlay the user input as a red point
    ax.plot(input_df[col_name], 1, 'ro', label='User Input')
    ax.set_title(f'Comparación de {col_name}')
    ax.set_xlabel(col_name)
    ax.legend()
    
    # Display each plot in the current column
    columns[i % 2].pyplot(fig)

# Define categorical columns to compare
categorical_columns_to_compare = ['Bienes_Mejor_Emp', 'Metod_Nuev_Emp', 'Metod_Nuev_Prod', 'Metod_Nuev_Info', 'Metod_Nuev_Dist', 'Tec_Comerce_Nuev']

# Filter training data for rows where porcentaje_cambio is positive
filtered_data = training_data[training_data['porcentaje_cambio'] > 0]

# Convert the specified categorical columns in input_data to category
for col in categorical_columns_to_compare:
    if col in input_df.columns:
        input_data[col] = input_df[col].astype('category')

# Convert the specified categorical columns in training_data to category (if not already done)
for col in categorical_columns_to_compare:
    if col in training_data.columns:
        training_data[col] = training_data[col].astype('category')

# Set up a 3-column layout for plotting
for i, col_name in enumerate(categorical_columns_to_compare):
    # Create a new row with 3 columns for every three plots
    if i % 3 == 0:
        col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]
    
    # Create the plot
    fig, ax = plt.subplots()
    
    # Plot the count plot for the filtered training data
    sns.countplot(x=filtered_data[col_name], ax=ax, color="skyblue", label="Filtered Data")
    
    # Highlight the user's input as a separate bar
    user_input_value = input_df[col_name].iloc[0]  # Safely get the first value
    ax.bar(user_input_value, filtered_data[col_name].value_counts().get(user_input_value, 0), color='red', label='User Input')
    
    # Set title and labels
    ax.set_title(f'Comparación de {col_name}')
    ax.set_xlabel(col_name)
    ax.legend()
    
    # Display each plot in the current column
    columns[i % 3].pyplot(fig)



