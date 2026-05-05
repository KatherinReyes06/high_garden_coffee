# High Garden Coffee — Análisis Estratégico del Mercado del Café

Análisis de consumo doméstico de café en 53 países (1990/91 – 2019/20) con modelos de Machine Learning para identificar tendencias, proyectar precios y segmentar mercados.

## Estructura del proyecto

- **data/** — Datos fuente (consumo y precios)
- **notebooks/analysis.ipynb** — Análisis completo (EDA, modelos, conclusiones)
- **app_streamlit/app.py** — Dashboard interactivo con chatbot de IA
- **app_streamlit/.env** — API key de Gemini (no incluida por seguridad)
- **HighGardenCoffee_Presentacion.pdf** — Presentación ejecutiva
- **requirements.txt** — Dependencias del proyecto
- **README.md** — Este archivo

## Cómo ejecutar

### Notebook
1. Instalar dependencias: `pip install -r requirements.txt`
2. Abrir `notebooks/analysis.ipynb` en VS Code o Jupyter
3. Ejecutar todas las celdas en orden

### Streamlit
1. Crear archivo `.env` dentro de `app_streamlit/` con el contenido: `GEMINI_API_KEY=tu_clave_de_gemini`
2. Ejecutar en terminal:

cd app_streamlit
streamlit run app.py

## Tecnologías

- Python (pandas, numpy, scikit-learn, statsmodels)
- ARIMA para predicción de consumo y precios
- K-Means para segmentación de mercados
- Streamlit + Google Gemini para dashboard con chatbot
- Plotly para visualizaciones interactivas

## Fuentes de datos

- **Consumo:** dataset proporcionado (coffee_db.parquet)
- **Precios Arábica:** FMI vía FRED (PCOFFOTMUSDA)
- **Precios Robusta:** FMI vía FRED (PCOFFROBUSDA)
