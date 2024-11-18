import streamlit as st
import pickle
import numpy as np
import pandas as pd
import os
import seaborn as sns
import matplotlib.backends.backend_pdf
import matplotlib
matplotlib.use("Agg")  
import matplotlib.pyplot as plt


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
    ("Activ_Econ", "Pregunta 1: Código de la actividad económica principal de la empresa según la clasificación internacional (CIIU)", 0),
    ("Ventas_Nacion19", "Pregunta 2: Ingresos/ventas totales en el mercado nacional del año anterior (en miles de pesos)", 0),
    ("Export_2019", "Pregunta 3: Exportaciones totales de la empresa en el año anterior (en miles de pesos)", 0),
    ("Ventas_Nacion20", "Pregunta 4: Utilidades totales en el mercado nacional del año anterior (en miles de pesos)", 0),
    ("Export_2020", "Pregunta 5: Exportaciones esperadas totales de la empresa en el año actual (en miles de pesos)", 0),
    ("Bienes_Ctes", "Pregunta 6: Porcentaje de ventas nacionales esperadas de bienes o servicios que no cambiaran al año anterior (Valores entre 0 y 1)", 0.0, 0.0, 1.0),
    ("Razon_No_Proy", "Pregunta 7: Razón principal por la cual no introdujo innovaciones", 1, 1, 12),
    ("Average_Cert_Employ19", "Pregunta 8: Empleados con certificaciones laborales de competencias laborales inherentes a la actividad(es) principal(es) que desarrolla la empresaen el año anterior", 0),
    ("Average_Cert_Employ20", "Pregunta 9: Empleados con certificaciones laborales de competencias laborales inherentes a la actividad(es) principal(es) que desarrolla la empresa en el año actual", 0)
]

# Opciones para la razón de no innovación
razon_options = {
    1: "No hay una razón convincente para innovar",
    2: "No fue necesario innovar debido a innovaciones realizadas en periodos anteriores",
    3: "No fue necesario innovar debido a poca competencia en el mercado",
    4: "Falta de ideas para introducir innovaciones",
    5: "La empresa tuvo prioridades diferentes a la innovación",
    6: "Suposición de que la innovación cuesta demasiado",
    7: "Falta de personal calificado para realizar una innovación",
    8: "Falta de comprensión del concepto de innovación",
    9: "Falta de información disponible sobre metodología para realizar una innovación",
    10: "No fue claro identificar las necesidades de innovación",
    11: "No hay incentivos a innovar debido a demasiada competencia en el mercado",
    12: "No se cuenta con infraestructura para desarrollar una innovación"
}

# Diccionario para mapear respuestas de texto a códigos
respuesta_map = {
    'Estricta': 'ESTRIC',
    'Amplia': 'AMPLIA',
    'Potencial': 'POTENC',
    'No innovadora': 'NOINNO',
    'Internacional': 'INTENC'
}

# Preguntas personalizadas para datos categóricos con restricciones de respuesta (Sí=1, No=2)
categorical_questions_restricted = {
    "Bienes_Nuev_Emp": "Pregunta 10: ¿Introdujo su empresa bienes o servicios nuevos que ya existían en el mercado nacional o internacional, pero eran nuevos para la empresa durante los 2 últimos años? (Sí=1, No=2)",
    "Bienes_Nuev_Nacion": "Pregunta 11: ¿Introdujo su empresa bienes o servicios nuevos en el mercado nacional durante los 2 últimos años? (Sí=1, No=2)",
    "Bienes_Nuev_Inter": "Pregunta 12: ¿Introdujo su empresa bienes o servicios nuevos en el mercado internacional durante los 2 últimos años? (Sí=1, No=2)",
    "Bienes_Mejor_Emp": "Pregunta 13: ¿Introdujo su empresa mejoras a bienes o servicios que ya existían en el mercado, pero que fueron mejorados solo para la empresa durante los 2 últimos años? (Sí=1, No=2)",
    "Bienes_Mejor_Nacion": "Pregunta 14: ¿Introdujo su empresa mejoras a bienes o servicios en el mercado nacional durante los 2 últimos años? (Sí=1, No=2)",
    "Bienes_Mejor_Inter": "Pregunta 15: ¿Introdujo su empresa mejoras a bienes o servicios en el mercado internacional durante los 2 últimos años? (Sí=1, No=2)",
    "Metod_Nuev_Prod": "Pregunta 16: ¿Introdujo su empresa métodos nuevos o mejorados de producción de bienes o prestación de servicios durante los 2 últimos años? (Sí=1, No=2)",
    "Metod_Nuev_Emp": "Pregunta 17: ¿Implementó su empresa métodos organizativos nuevos o mejorados en su funcionamiento interno durante los 2 últimos años? (Sí=1, No=2)",
    "Tec_Comerce_Nuev": "Pregunta 18: ¿Introdujo su empresa técnicas de comercialización nuevas o mejoradas durante los 2 últimos años? (Sí=1, No=2)",
    "Metod_Nuev_Dist": "Pregunta 19: ¿Implementó su empresa métodos nuevos o mejorados de distribución, entrega o logística durante los 2 últimos años? (Sí=1, No=2)",
    "Metod_Nuev_Info": "Pregunta 20: ¿Introdujo su empresa métodos nuevos o mejorados de procesamiento de información o comunicación durante los 2 últimos años? (Sí=1, No=2)",
    "Metod_Nuev_Conta": "Pregunta 21: ¿Introdujo su empresa métodos nuevos o mejorados para la contabilidad u operaciones administrativas durante los 2 últimos años? (Sí=1, No=2)",
    "Proy_Bienes_Nuev": "Pregunta 22: ¿Tenía su empresa algún proyecto en marcha para introducir bienes o servicios nuevos o mejorados al finalizar los 2 últimos años? (Sí=1, No=2)",
    "Abandono_Proy": "Pregunta 23: ¿Abandonó su empresa algún proyecto de innovación durante los 2 últimos años? (Sí=1, No=2)",
    "Intencion_Proy": "Pregunta 24: ¿Tuvo su empresa la intención de realizar algún proyecto de innovación durante los 2 últimos años? (Sí=1, No=2)",
    "Cert_Quali_Process": "Pregunta 25: ¿Obtuvo su empresa certificaciones de calidad de procesos durante los 2 últimos años? (Sí=1, No=2)",
    "Cert_Quali_Product": "Pregunta 26: ¿Obtuvo su empresa certificaciones de calidad de productos durante los 2 últimos años? (Sí=1, No=2)",
    "Reglamento": "Pregunta 27: ¿Estuvieron los bienes o servicios de su empresa sujetos a reglamentos técnicos durante los 2 últimos años? (Sí=1, No=2)"
}

# Definir preguntas categóricas sin restricciones
categorical_inputs_unrestricted = {
    "Tipo": "Pregunta 28: Seleccione el tipo de empresa según el grado de innovación",
    "Ventas_NacionTotal": "Pregunta 29: Porcentaje de ventas nacionales esperadas de bienes o servicios totales en el año actual"
}


# Función para obtener entradas numéricas
def get_numerical_input():
    data = {}
    for col, question, default, *limits in numerical_inputs:
        if col == "Razon_No_Proy":  # Cambia a selectbox para esta entrada
            data[col] = st.radio(question, options=list(razon_options.keys()), format_func=lambda x: razon_options[x], key=col, index = None)
        elif limits:  # Casos donde hay un rango de valores
            data[col] = st.number_input(question, min_value=limits[0], max_value=limits[1], value=None, key=col)
        else:
            data[col] = st.number_input(question, value=None,  key=col)
    return data

# Función para obtener entradas categóricas restringidas (Sí=1, No=2)
def get_categorical_input_restricted():
    data = {}
    for col, question in categorical_questions_restricted.items():
        data[col] = st.radio(question, options=[1, 2], key=col, index = None)
    return data

def get_categorical_input_unrestricted():
    data = {}
    
    # Obtener opciones para el selectbox desde respuesta_map
    tipo_options = list(respuesta_map.keys())  # Opciones para el selectbox
    data["Tipo"] = st.radio(categorical_inputs_unrestricted["Tipo"], options=tipo_options,key="Tipo", index = None)
    
    # Entrada numérica para ventas nacionales totales
    data["Ventas_NacionTotal"] = st.number_input(
        categorical_inputs_unrestricted["Ventas_NacionTotal"],
        min_value=0.0,
        max_value=1.0,
        value=None,  key="Ventas_NacionTotal"
    )
    
    return data

# Obtener entradas del usuario
numerical_data = get_numerical_input()
categorical_data_restricted = get_categorical_input_restricted()
categorical_data_unrestricted = get_categorical_input_unrestricted()


# Concatenar todos los datos
input_data = {**numerical_data, **categorical_data_restricted, **categorical_data_unrestricted}
input_df = pd.DataFrame([input_data])  # Convertir a DataFrame

if 'porcentaje_cambio' not in training_data.columns:
    training_data['porcentaje_cambio'] = np.nan  # Add as NaN if not prese
print(training_data['porcentaje_cambio'].dtype)

# Create a PDF file to save all plots
pdf_path = "graphs_comparison.pdf"
pdf = matplotlib.backends.backend_pdf.PdfPages(pdf_path)

# Botón para hacer la predicción
if st.button("Hacer Predicción"):
    if input_df.isnull().values.any():  # This checks if any value is missing
        st.warning("Por favor, responda todas las preguntas antes de hacer la predicción.")  # Added warning if there are missing values
    else:
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
                pdf.savefig(fig)  # Save the figure to PDF
                plt.close(fig)  # Close the figure to avoid display issues
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
        pdf.savefig(fig)  # Save the figure to PDF
        plt.close(fig) 

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
        if user_input_value is None:
            st.warning("Invalid input provided for the bar chart.")
        else:
            ax.bar(user_input_value, filtered_data[col_name].value_counts().get(user_input_value, 0), color='red', label='User Input')

        
        # Set title and labels
        ax.set_title(f'Comparación de {col_name}')
        ax.set_xlabel(col_name)
        ax.legend()
        
        # Display each plot in the current column
        columns[i % 3].pyplot(fig)
        pdf.savefig(fig)  # Save the figure to PDF
        plt.close(fig) 


    # Close the PDF file
    pdf.close()

    # Provide a download button for the generated PDF
    with open(pdf_path, "rb") as file:
        st.download_button(label="Descargar todos los gráficos", data=file, file_name="comparacion_graficos.pdf")



