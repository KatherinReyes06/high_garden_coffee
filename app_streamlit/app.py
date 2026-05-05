import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="High Garden Coffee — Análisis Estratégico",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;500;600&display=swap');
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2C1810 0%, #3E2723 100%);
    }
    [data-testid="stSidebar"] * {
        color: #F5F0EB !important;
    }
    [data-testid="stSidebar"] .stRadio label span {
        color: #D4A574 !important;
        font-size: 15px;
    }
    
    /* Métricas */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #F5F0EB 0%, #EDE4DA 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #5D4037;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    [data-testid="stMetric"] label {
        color: #8D6E63 !important;
        font-size: 13px !important;
    }
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #2C1810 !important;
        font-weight: 700 !important;
    }
    
    /* Header personalizado */
    .header-empresa {
        background: linear-gradient(135deg, #2C1810 0%, #5D4037 100%);
        padding: 30px 40px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    .header-empresa h1 {
        color: #F5F0EB !important;
        font-size: 32px !important;
        margin: 0 !important;
    }
    .header-empresa p {
        color: #D4A574 !important;
        font-size: 16px;
        margin: 5px 0 0 0;
    }
    
    /* Cards de hallazgos */
    .hallazgo-card {
        background: linear-gradient(135deg, #F5F0EB 0%, #EDE4DA 100%);
        padding: 20px;
        border-radius: 10px;
        border-top: 4px solid #5D4037;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        height: 100%;
    }
    .hallazgo-card h4 {
        color: #2C1810;
        margin-bottom: 10px;
    }
    .hallazgo-card p {
        color: #5D4037;
        font-size: 14px;
        line-height: 1.5;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        color: #5D4037;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #5D4037 !important;
        color: #2C1810 !important;
    }
    
    /* Subtítulos */
    h2, h3 {
        color: #2C1810 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# TRADUCCIÓN DE PAÍSES
# ============================================================
TRAD_PAISES = {
    'Brazil': 'Brasil', 'Ethiopia': 'Etiopía', 'Mexico': 'México',
    'Philippines': 'Filipinas', 'Viet Nam': 'Vietnam',
    'Thailand': 'Tailandia', 'Côte d\'Ivoire': 'Costa de Marfil',
    'Tanzania': 'Tanzania', 'Indonesia': 'Indonesia',
    'Colombia': 'Colombia', 'Venezuela': 'Venezuela', 'India': 'India',
    'Guatemala': 'Guatemala', 'Honduras': 'Honduras',
    'El Salvador': 'El Salvador', 'Costa Rica': 'Costa Rica',
    'Peru': 'Perú', 'Ecuador': 'Ecuador', 'Bolivia (Plurinational State of)': 'Bolivia',
    'Dominican Republic': 'República Dominicana', 'Cuba': 'Cuba',
    'Haiti': 'Haití', 'Jamaica': 'Jamaica', 'Nicaragua': 'Nicaragua',
    'Panama': 'Panamá', 'Paraguay': 'Paraguay',
    'Trinidad & Tobago': 'Trinidad y Tobago', 'Guyana': 'Guyana',
    'Ghana': 'Ghana', 'Yemen': 'Yemen', 'Togo': 'Togo',
    'Gabon': 'Gabón', 'Zimbabwe': 'Zimbabue', 'Zambia': 'Zambia',
    'Malawi': 'Malaui', 'Sierra Leone': 'Sierra Leona',
    'Sri Lanka': 'Sri Lanka', 'Uganda': 'Uganda', 'Kenya': 'Kenia',
    'Cameroon': 'Camerún', 'Nigeria': 'Nigeria',
    'Central African Republic': 'República Centroafricana',
    'Democratic Republic of Congo': 'R.D. del Congo',
    'Congo': 'Congo', 'Madagascar': 'Madagascar', 'Rwanda': 'Ruanda',
    'Burundi': 'Burundi', 'Angola': 'Angola', 'Guinea': 'Guinea',
    'Liberia': 'Liberia', 'Papua New Guinea': 'Papúa Nueva Guinea',
    'Timor-Leste': 'Timor Oriental',
    'Lao People\'s Democratic Republic': 'Laos'
}

def traducir(nombre):
    return TRAD_PAISES.get(nombre, nombre)

# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data
def cargar_datos():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    df_consumo = pd.read_parquet(os.path.join(BASE_DIR, 'coffee_db.parquet'))
    df_arabica = pd.read_csv(os.path.join(BASE_DIR, 'arabica_precios.csv'))
    df_robusta = pd.read_csv(os.path.join(BASE_DIR, 'robusta_precios.csv'))
    
    df_arabica = df_arabica.rename(columns={
        'observation_date': 'Fecha',
        'PCOFFOTMUSDA': 'Precio_Arabica_centavos_por_libra'
    })
    df_robusta = df_robusta.rename(columns={
        'observation_date': 'Fecha',
        'PCOFFROBUSDA': 'Precio_Robusta_centavos_por_libra'
    })
    
    df_arabica['Precio_Arabica_USD_por_libra'] = df_arabica['Precio_Arabica_centavos_por_libra'] / 100
    df_robusta['Precio_Robusta_USD_por_libra'] = df_robusta['Precio_Robusta_centavos_por_libra'] / 100
    df_arabica['Año'] = pd.to_datetime(df_arabica['Fecha']).dt.year
    df_robusta['Año'] = pd.to_datetime(df_robusta['Fecha']).dt.year
    
    year_columns = [col for col in df_consumo.columns if '/' in col]
    df_clean = df_consumo.copy()
    all_zero_mask = df_clean[year_columns].sum(axis=1) == 0
    df_clean = df_clean[~all_zero_mask].reset_index(drop=True)
    
    for idx, row in df_clean.iterrows():
        values = row[year_columns].values.astype(float)
        non_zero_idx = np.where(values > 0)[0]
        if len(non_zero_idx) > 0:
            for i in range(non_zero_idx[0]):
                df_clean.at[idx, year_columns[i]] = np.nan
            for i in range(non_zero_idx[-1] + 1, len(year_columns)):
                if values[i] == 0:
                    df_clean.at[idx, year_columns[i]] = np.nan
    
    df_consumo_pais = pd.melt(
        df_clean, id_vars=['Country', 'Coffee type'],
        value_vars=year_columns, var_name='Cosecha',
        value_name='Consumo_Anual_Domestico'
    )
    df_consumo_pais = df_consumo_pais.rename(columns={
        'Country': 'Pais', 'Coffee type': 'Tipo_Cafe'
    })
    df_consumo_pais['Pais'] = df_consumo_pais['Pais'].map(traducir)
    df_consumo_pais['Año_Inicio'] = df_consumo_pais['Cosecha'].str.split('/').str[0].astype(int)
    df_consumo_pais = df_consumo_pais.sort_values(['Pais', 'Año_Inicio']).reset_index(drop=True)
    
    return df_clean, df_consumo_pais, df_arabica, df_robusta, year_columns

df_clean, df_consumo_pais, df_arabica, df_robusta, year_columns = cargar_datos()

# ============================================================
# FUNCIÓN PARA FORMATEAR NÚMEROS
# ============================================================
def formato_tazas(valor):
    if valor >= 1e9:
        return f"{valor/1e9:.2f} Mil M"
    elif valor >= 1e6:
        return f"{valor/1e6:.0f}M"
    else:
        return f"{valor:,.0f}"

def tick_formato_millones(fig):
    fig.update_layout(
        yaxis=dict(
            tickvals=[0, 500e6, 1e9, 1.5e9, 2e9, 2.5e9, 3e9, 3.5e9, 4e9],
            ticktext=['0', '500M', '1,000M', '1,500M', '2,000M', '2,500M', '3,000M', '3,500M', '4,000M']
        )
    )
    return fig

# ============================================================
# MÉTRICAS GLOBALES
# ============================================================
consumo_mundial = df_consumo_pais.groupby('Año_Inicio')['Consumo_Anual_Domestico'].sum().reset_index()
consumo_mundial.columns = ['Año', 'Consumo_Total']

consumo_por_pais = df_consumo_pais.groupby('Pais')['Consumo_Anual_Domestico'].sum().reset_index()
consumo_por_pais.columns = ['Pais', 'Consumo_Total']
consumo_por_pais = consumo_por_pais.sort_values('Consumo_Total', ascending=False).reset_index(drop=True)
total_mundial = consumo_por_pais['Consumo_Total'].sum()
consumo_por_pais['Porcentaje'] = (consumo_por_pais['Consumo_Total'] / total_mundial) * 100

consumo_inicio = consumo_mundial.iloc[0]['Consumo_Total']
consumo_fin = consumo_mundial.iloc[-1]['Consumo_Total']
cagr_global = ((consumo_fin / consumo_inicio) ** (1 / (len(consumo_mundial)-1)) - 1) * 100

cagr_pais = []
for _, row in df_clean.iterrows():
    valores = row[year_columns].values.astype(float)
    valid_idx = np.where(~np.isnan(valores) & (valores > 0))[0]
    if len(valid_idx) >= 2:
        inicio_v = valores[valid_idx[0]]
        fin_v = valores[valid_idx[-1]]
        n_años = valid_idx[-1] - valid_idx[0]
        if n_años > 0 and inicio_v > 0:
            cagr = ((fin_v / inicio_v) ** (1 / n_años) - 1) * 100
            cagr_pais.append({'Pais': traducir(row['Country']), 'CAGR': cagr})
df_cagr = pd.DataFrame(cagr_pais).sort_values('CAGR', ascending=False)

# Clustering
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

features_pais = []
for _, row in df_clean.iterrows():
    valores = row[year_columns].values.astype(float)
    valid = valores[~np.isnan(valores)]
    if len(valid) >= 5:
        consumo_promedio = np.mean(valid)
        inicio_v = valid[0]
        fin_v = valid[-1]
        n = len(valid) - 1
        cagr_v = ((fin_v / inicio_v) ** (1 / n) - 1) * 100 if inicio_v > 0 else 0
        volatilidad = (np.std(valid) / np.mean(valid)) * 100
        features_pais.append({
            'Pais': traducir(row['Country']), 'Consumo_Promedio': consumo_promedio,
            'CAGR': cagr_v, 'Volatilidad': volatilidad,
            'Log_Consumo': np.log10(consumo_promedio)
        })

df_feat = pd.DataFrame(features_pais)
scaler = StandardScaler()
X = scaler.fit_transform(df_feat[['Log_Consumo', 'CAGR', 'Volatilidad']])
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
df_feat['Cluster'] = kmeans.fit_predict(X)

cluster_profiles = df_feat.groupby('Cluster').agg(
    Consumo_Medio=('Consumo_Promedio', 'mean'),
    CAGR_Medio=('CAGR', 'mean'),
    N_Paises=('Pais', 'count')
).reset_index()

nombres_cluster = {}
for _, row in cluster_profiles.iterrows():
    c = row['Cluster']
    if row['CAGR_Medio'] < 0:
        nombres_cluster[c] = 'En Declive'
    elif row['Consumo_Medio'] > cluster_profiles['Consumo_Medio'].median() and row['CAGR_Medio'] > 2:
        nombres_cluster[c] = 'Grandes y en Crecimiento'
    else:
        nombres_cluster[c] = 'Estables'

df_feat['Segmento'] = df_feat['Cluster'].map(nombres_cluster)

# ============================================================
# BARRA LATERAL
# ============================================================
st.sidebar.markdown("### ☕ High Garden Coffee")
st.sidebar.markdown("---")
pagina = st.sidebar.radio(
    "Navegación",
    ["Inicio", "Exploración", "Modelos y Predicciones", "Chatbot IA"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")
st.sidebar.caption("Datos: ICO | Precios: FMI vía FRED")

# ============================================================
# PÁGINA 1: INICIO
# ============================================================
if pagina == "Inicio":
    st.markdown("""
    <div class="header-empresa">
        <h1>☕ High Garden Coffee</h1>
        <p>Análisis Estratégico del Mercado Internacional del Café</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Consumo 2019/20", f"{consumo_fin/1e9:.2f} Mil M")
    col2.metric("CAGR Global", f"{cagr_global:.1f}% anual")
    col3.metric("Países Analizados", f"{df_clean.shape[0]}")
    col4.metric("Segmentos", "3")
    
    st.markdown("---")
    
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown("""
        <div class="hallazgo-card">
            <h4>Sobre este proyecto</h4>
            <p>
            Análisis de consumo doméstico de café en 53 países 
            (1990/91 – 2019/20) combinado con precios históricos del FMI para 
            identificar tendencias, proyectar consumo y precios a 10 años (ARIMA), 
            segmentar mercados (K-Means) y generar recomendaciones estratégicas.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_der:
        st.markdown("""
        <div class="hallazgo-card">
            <h4>Fuentes de datos</h4>
            <p>
            <strong>Consumo:</strong> coffee_db.parquet — 53 países, 30 cosechas<br>
            <strong>Precios Arábica:</strong> FMI vía FRED (PCOFFOTMUSDA)<br>
            <strong>Precios Robusta:</strong> FMI vía FRED (PCOFFROBUSDA)<br>
            <strong>Período:</strong> Cosechas 1990/91 a 2019/20
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    h1, h2, h3 = st.columns(3)
    with h1:
        st.markdown(f"""
        <div class="hallazgo-card">
            <h4>📈 Mercado en expansión</h4>
            <p>El consumo mundial creció {((consumo_fin-consumo_inicio)/consumo_inicio*100):.0f}% en 30 cosechas. 
            Brasil concentra el {consumo_por_pais.iloc[0]['Porcentaje']:.1f}% del mercado.</p>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        st.markdown(f"""
        <div class="hallazgo-card">
            <h4>🚀 Oportunidades claras</h4>
            <p>Tanzania ({df_cagr.iloc[0]['CAGR']:.1f}%), Vietnam ({df_cagr.iloc[1]['CAGR']:.1f}%) 
            y Tailandia ({df_cagr.iloc[2]['CAGR']:.1f}%) lideran el crecimiento.</p>
        </div>
        """, unsafe_allow_html=True)
    with h3:
        st.markdown("""
        <div class="hallazgo-card">
            <h4>💰 Precios al alza</h4>
            <p>Arábica y Robusta muestran tendencia alcista. 
            Robusta se encarece más rápido, reduciendo la brecha con Arábica.</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PÁGINA 2: EXPLORACIÓN
# ============================================================
elif pagina == "Exploración":
    st.title("Exploración de Datos")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Consumo Mundial", "Top Consumidores", "Tipos de Café", "Precios"
    ])
    
    with tab1:
        st.subheader("Evolución del Consumo Mundial de Café")
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=consumo_mundial['Año'], y=consumo_mundial['Consumo_Total'],
            marker_color='#5D4037', opacity=0.85
        ))
        fig.update_layout(
            xaxis_title='Año de inicio de cosecha',
            yaxis_title='Consumo Total (tazas)',
            template='plotly_white', height=500
        )
        fig.update_traces(hovertemplate='Año: %{x}<br>Consumo: %{y:,.0f} tazas')
        fig = tick_formato_millones(fig)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Top 10 Países Consumidores")
        top10 = consumo_por_pais.head(10)
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=top10['Pais'][::-1], x=top10['Consumo_Total'][::-1],
            orientation='h', marker_color='#5D4037',
            text=[f"{p:.1f}%" for p in top10['Porcentaje'][::-1]],
            textposition='outside'
        ))
        fig.update_layout(
            xaxis_title='Consumo Total Acumulado (tazas)',
            template='plotly_white', height=500
        )
        fig.update_traces(hovertemplate='%{y}: %{x:,.0f} tazas (%{text})')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Consumo por Tipo de Café")
        consumo_tipo = df_consumo_pais.groupby(['Año_Inicio', 'Tipo_Cafe'])['Consumo_Anual_Domestico'].sum().reset_index()
        colores = {'Arabica': '#2E86AB', 'Robusta': '#E84855',
                   'Robusta/Arabica': '#F6AE2D', 'Arabica/Robusta': '#33A474'}
        fig = px.line(consumo_tipo, x='Año_Inicio', y='Consumo_Anual_Domestico',
                      color='Tipo_Cafe', color_discrete_map=colores, markers=True)
        fig.update_layout(
            xaxis_title='Año', yaxis_title='Consumo (tazas)',
            template='plotly_white', height=500, legend_title='Tipo de Café',
            yaxis=dict(
                tickvals=[0, 200e6, 400e6, 600e6, 800e6, 1e9, 1.2e9, 1.4e9, 1.6e9],
                ticktext=['0', '200M', '400M', '600M', '800M', '1,000M', '1,200M', '1,400M', '1,600M']
            )
        )
        fig.update_traces(hovertemplate='Año: %{x}<br>Consumo: %{y:,.0f} tazas')
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Evolución de Precios: Arábica vs Robusta")
        df_arab_filt = df_arabica[df_arabica['Año'] <= 2020]
        df_rob_filt = df_robusta[df_robusta['Año'] <= 2020]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_arab_filt['Año'], y=df_arab_filt['Precio_Arabica_USD_por_libra'],
            mode='lines+markers', name='Arábica', line=dict(color='#5D4037', width=2.5)
        ))
        fig.add_trace(go.Scatter(
            x=df_rob_filt['Año'], y=df_rob_filt['Precio_Robusta_USD_por_libra'],
            mode='lines+markers', name='Robusta', line=dict(color='#D4A574', width=2.5)
        ))
        fig.update_layout(
            xaxis_title='Año', yaxis_title='Precio (USD por libra)',
            template='plotly_white', height=500
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.subheader("Mapa de Calor: Crecimiento por País y Década")
    
    decadas = {
        '1990-1999': ('1990/91', '1999/00'),
        '2000-2009': ('2000/01', '2009/10'),
        '2010-2019': ('2010/11', '2019/20')
    }
    heatmap_data = []
    for _, row in df_clean.iterrows():
        pais = traducir(row['Country'])
        for nombre_decada, (col_inicio, col_fin) in decadas.items():
            val_inicio = row[col_inicio]
            val_fin = row[col_fin]
            if pd.notna(val_inicio) and pd.notna(val_fin) and val_inicio > 0:
                cambio = ((val_fin - val_inicio) / val_inicio) * 100
                heatmap_data.append({'Pais': pais, 'Década': nombre_decada, 'Cambio_Pct': cambio})
    
    df_heatmap = pd.DataFrame(heatmap_data)
    top20_paises = consumo_por_pais.head(20)['Pais'].tolist()
    df_heatmap_filtrado = df_heatmap[df_heatmap['Pais'].isin(top20_paises)]
    heatmap_pivot = df_heatmap_filtrado.pivot(index='Pais', columns='Década', values='Cambio_Pct')
    heatmap_pivot = heatmap_pivot[['1990-1999', '2000-2009', '2010-2019']]
    heatmap_pivot = heatmap_pivot.sort_values('2010-2019', ascending=True)
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_pivot.values, x=heatmap_pivot.columns.tolist(),
        y=heatmap_pivot.index.tolist(),
        colorscale=[[0, '#E84855'], [0.5, '#FFFFFF'], [1, '#33A474']],
        zmid=0,
        text=[[f"{v:.0f}%" if pd.notna(v) else "" for v in row] for row in heatmap_pivot.values],
        texttemplate="%{text}", textfont={"size": 11}, colorbar_title="Cambio %"
    ))
    fig.update_layout(height=600, template='plotly_white', xaxis_title='Década', yaxis_title='')
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Verde = crecimiento, Rojo = declive. Top 20 consumidores.")

# ============================================================
# PÁGINA 3: MODELOS
# ============================================================
elif pagina == "Modelos y Predicciones":
    st.title("Modelos de Machine Learning")
    
    tab1, tab2, tab3 = st.tabs(["Predicción de Consumo", "Segmentación", "Proyección de Precios"])
    
    with tab1:
        st.subheader("Predicción de Consumo Mundial (ARIMA)")
        st.markdown("Modelo ARIMA(2,1,1) entrenado con datos hasta 2014, validado con 2015-2019, proyectado a 2029/30.")
        
        from statsmodels.tsa.arima.model import ARIMA
        consumo_ts = consumo_mundial.set_index('Año')['Consumo_Total']
        train = consumo_ts[consumo_ts.index <= 2014]
        modelo = ARIMA(train, order=(2, 1, 1))
        modelo_fit = modelo.fit()
        n_test = len(consumo_ts[consumo_ts.index > 2014])
        forecast = modelo_fit.get_forecast(steps=n_test + 10)
        pred_values = forecast.predicted_mean
        pred_ci = forecast.conf_int(alpha=0.2)
        pred_index = list(range(2015, 2015 + n_test + 10))
        pred_series = pd.Series(pred_values.values, index=pred_index)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(consumo_ts.index), y=list(consumo_ts.values),
            mode='lines+markers', name='Consumo Real', line=dict(color='#5D4037', width=2.5)
        ))
        fut = pred_series[pred_series.index > 2019]
        x_pred = [2019] + list(fut.index)
        y_pred = [consumo_ts.iloc[-1]] + list(fut.values)
        fig.add_trace(go.Scatter(
            x=x_pred, y=y_pred, mode='lines+markers', name='Predicción',
            line=dict(color='#D4A574', width=2.5, dash='dash')
        ))
        ci_fut = pred_ci.iloc[n_test:]
        fig.add_trace(go.Scatter(
            x=list(fut.index) + list(fut.index)[::-1],
            y=list(ci_fut.iloc[:, 1].values) + list(ci_fut.iloc[:, 0].values)[::-1],
            fill='toself', fillcolor='rgba(212,165,116,0.15)',
            line=dict(color='rgba(255,255,255,0)'), name='Rango probable (80%)'
        ))
        fig.update_layout(
            xaxis_title='Año', yaxis_title='Consumo Total (tazas)',
            template='plotly_white', height=500
        )
        fig.update_traces(hovertemplate='Año: %{x}<br>Consumo: %{y:,.0f} tazas', selector=dict(name='Consumo Real'))
        fig.update_traces(hovertemplate='Año: %{x}<br>Predicción: %{y:,.0f} tazas', selector=dict(name='Predicción'))
        fig = tick_formato_millones(fig)
        st.plotly_chart(fig, use_container_width=True)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Real 2019/20", formato_tazas(consumo_ts.iloc[-1]))
        c2.metric("Predicción 2029/30", formato_tazas(fut.iloc[-1]))
        cambio = ((fut.iloc[-1] - consumo_ts.iloc[-1]) / consumo_ts.iloc[-1]) * 100
        c3.metric("Cambio esperado", f"{cambio:+.1f}%")
    
    with tab2:
        st.subheader("Segmentación de Mercados (K-Means)")
        st.markdown("Los países se agruparon en 3 segmentos según consumo promedio, crecimiento (CAGR) y volatilidad.")
        
        colores_seg = {'Grandes y en Crecimiento': '#5D4037',
                       'Estables': '#D4A574', 'En Declive': '#E84855'}
        
        fig = px.scatter(df_feat, x='CAGR', y='Log_Consumo', color='Segmento',
                        color_discrete_map=colores_seg, hover_data=['Pais'])
        fig.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=1, color='white')))
        fig.update_layout(
            xaxis_title='CAGR (% crecimiento anual)',
            yaxis_title='Consumo Promedio Anual',
            template='plotly_white', height=500,
            yaxis=dict(tickvals=[5,6,7,8,9], ticktext=['100K','1M','10M','100M','1,000M'])
        )
        fig.add_vline(x=0, line_dash="dot", line_color="gray", opacity=0.5)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Pasa el cursor sobre los puntos para ver el nombre del país.")
        
        for seg in ['Grandes y en Crecimiento', 'Estables', 'En Declive']:
            grupo = df_feat[df_feat['Segmento'] == seg]
            if len(grupo) > 0:
                with st.expander(f"{seg} ({len(grupo)} países)"):
                    st.markdown(f"**Consumo promedio:** {grupo['Consumo_Promedio'].mean()/1e6:,.1f}M tazas/año")
                    st.markdown(f"**CAGR promedio:** {grupo['CAGR'].mean():.1f}%")
                    st.markdown(f"**Volatilidad promedio:** {grupo['Volatilidad'].mean():.1f}%")
                    st.markdown(f"**Países:** {', '.join(grupo['Pais'].tolist())}")
    
    with tab3:
        st.subheader("Proyección de Precios a 2030")
        from statsmodels.tsa.arima.model import ARIMA as ARIMA_P
        
        c1, c2 = st.columns(2)
        for col, nombre, serie_col, color in [
            (c1, 'Arábica', 'Precio_Arabica_USD_por_libra', '#5D4037'),
            (c2, 'Robusta', 'Precio_Robusta_USD_por_libra', '#D4A574')
        ]:
            with col:
                df_precio = df_arabica if 'Arabica' in serie_col else df_robusta
                df_precio_filt = df_precio[df_precio['Año'] <= 2020]
                serie = df_precio_filt.set_index('Año')[serie_col]
                train_p = serie[serie.index <= 2015]
                modelo_p = ARIMA_P(train_p, order=(2, 1, 1))
                modelo_p_fit = modelo_p.fit()
                n_test_p = len(serie[serie.index > 2015])
                forecast_p = modelo_p_fit.get_forecast(steps=n_test_p + 10)
                pred_p = pd.Series(forecast_p.predicted_mean.values,
                                   index=list(range(2016, 2016 + n_test_p + 10)))
                cambio_p = ((pred_p[2030] - serie.iloc[-1]) / serie.iloc[-1]) * 100
                st.metric(f"{nombre} (2020)", f"${serie.iloc[-1]:.2f}/lb")
                st.metric(f"{nombre} (2030 pred)", f"${pred_p[2030]:.2f}/lb")
                st.metric("Cambio", f"{cambio_p:+.1f}%")

# ============================================================
# PÁGINA 4: CHATBOT
# ============================================================
elif pagina == "Chatbot IA":
    st.title("Asistente de Análisis — High Garden Coffee")
    st.markdown("Haz preguntas sobre los datos y resultados del análisis en lenguaje natural.")
    st.markdown("---")
    
    contexto = f"""
    Eres un analista de datos experto de High Garden Coffee, una exportadora internacional de café.
    Responde basándote ÚNICAMENTE en los siguientes datos reales del análisis.
    
    DATOS GENERALES:
    - Consumo mundial 2019/20: {consumo_fin/1e9:.2f} mil millones de tazas
    - CAGR global: {cagr_global:.1f}% anual (crecimiento sostenido desde 1990)
    - Países analizados: {df_clean.shape[0]}
    - Top 5: Brasil (45.5%), Indonesia (8.0%), Etiopía (7.4%), México (5.2%), Filipinas (4.6%)
    - Los Top 5 concentran el 70.7% del consumo mundial
    
    TIPO DE CAFÉ POR PAÍS:
    - Brasil: Arábica/Robusta (mezcla)
    - Indonesia: Robusta
    - Etiopía: Arabica
    - México: Arábica/Robusta (mezcla)
    - Filipinas: Robusta/Arábica
    - Colombia: Arábica
    - Vietnam: Robusta
    
    PARTICIPACIÓN POR TIPO DE CAFÉ:
    - Arábica/Robusta (mezcla): 53.5% del mercado global
    - Robusta/Arábica: 22.7%
    - Arábica puro: 21.5%
    - Robusta puro: 2.3%
    
    MERCADOS EMERGENTES (CAGR): Tanzania 11.5%, Vietnam 10.4%, Tailandia 7.2%, Costa de Marfil 6.6%, Nicaragua 6.5%, Filipinas 5.3%, Indonesia 4.8%, Uganda 4.5%, Etiopía 4.0%, Brasil 3.5%
    MERCADOS EN DECLIVE (CAGR): Ghana -7.1%, Yemen -5.0%, Togo -4.5%, Gabón -4.1%, Ecuador -2.9%, Zimbabue -2.4%, Malaui -2.4%, Zambia -2.2%, Sri Lanka -2.2%, Sierra Leona -2.0%
    
    PREDICCIÓN DE CONSUMO MUNDIAL (ARIMA, precisión 98.5%):
    - 2019/20 (real): 3.00 mil millones de tazas
    - 2022/23 (pred): ~3.25 mil millones
    - 2024/25 (pred): ~3.47 mil millones
    - 2026/27 (pred): ~3.58 mil millones
    - 2029/30 (pred): 3.80 mil millones (+26.9% vs 2019)
    El modelo predice crecimiento continuo pero desacelerándose gradualmente.
    
    PREDICCIÓN POR PAÍS (a 2029/30):
    - Brasil: 1,320M -> 1,662M (+25.9%)
    - Indonesia: 288M -> 268M (-7.2%) — tendencia a la baja
    - Etiopía: 227M -> 290M (+27.8%)
    - México: 146M -> 141M (-3.3%) — leve declive
    - Filipinas: 195M -> 218M (+12.0%)
    
    PRECIOS (USD por libra de café verde):
    - Arábica 2020: $1.51 | Predicción 2030: $1.59 (+5.7%)
    - Robusta 2020: $0.69 | Predicción 2030: $0.81 (+18.3%)
    - Robusta se encarece más rápido que Arábica
    - Diferencia Arábica vs Robusta: $0.82 (2020) -> $0.78 (2030), se achica
    - Escenario pesimista 2030: Arábica $1.36, Robusta $0.69
    - Escenario base 2030: Arábica $1.59, Robusta $0.81
    - Escenario optimista 2030: Arábica $1.83, Robusta $0.94
    
    SEGMENTACIÓN (K-Means, 3 grupos):
    - Grandes y en crecimiento (10 países): Brasil, Indonesia, Vietnam, Etiopía, Filipinas, Tanzania, Costa de Marfil, Nicaragua, Tailandia, Uganda. Consumo promedio 147.8M, CAGR +6.4%
    - Estables (35 países): Colombia, México, India, Perú, Costa Rica, entre otros. Consumo promedio 16.2M, CAGR +0.5%
    - En declive (8 países): Ghana, Zimbabue, Zambia, Togo, Gabón, entre otros. Consumo promedio 0.2M, CAGR -3.0%
    
    RECOMENDACIONES:
    1. Diversificar hacia Tanzania, Vietnam y Filipinas
    2. Priorizar mezclas Arábica/Robusta (53.5% del mercado)
    3. Reducir exposición en Ghana, Yemen y Togo
    4. Usar escenarios de precio para negociar contratos
    5. Monitorear la reducción de la brecha de precio entre Arábica y Robusta
    
    Para años intermedios (2021-2028), puedes interpolar linealmente entre el dato real de 2019/20 y la predicción de 2029/30.
    Responde en español, de forma concisa y profesional. Si no tienes el dato exacto, da una estimación basada en la tendencia.
    """

    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []
    
    for msg in st.session_state.mensajes:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    pregunta = st.chat_input("Escribe tu pregunta sobre los datos...")
    
    if pregunta:
        st.session_state.mensajes.append({"role": "user", "content": pregunta})
        with st.chat_message("user"):
            st.markdown(pregunta)
        
        try:
            import google.generativeai as genai
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                st.error("No se encontró la API key de Gemini. Verifica el archivo .env")
            else:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-2.5-flash')
                prompt = f"{contexto}\n\nPregunta del usuario: {pregunta}"
                response = model.generate_content(prompt)
                respuesta = response.text
                st.session_state.mensajes.append({"role": "assistant", "content": respuesta})
                with st.chat_message("assistant"):
                    st.markdown(respuesta)
        except Exception as e:
            st.error(f"Error al conectar con Gemini: {str(e)}")