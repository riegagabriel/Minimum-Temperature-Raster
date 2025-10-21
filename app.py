import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

# ============================================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================================
st.set_page_config(
    page_title="Peru Tmin Analysis 2024",
    page_icon="🌡️",
    layout="wide"
)

# ============================================================================
# TÍTULO Y DESCRIPCIÓN
# ============================================================================
st.title("🌡️ Análisis de Temperatura Mínima en Perú — 2024")
st.markdown("""
Esta aplicación muestra el análisis de temperaturas mínimas (Tmin) a nivel distrital en Perú,
identificando zonas críticas para intervenciones de política pública.
""")

# ============================================================================
# CARGA DE DATOS
# ============================================================================
@st.cache_data
def load_data():
    """Carga todos los archivos CSV necesarios"""
    files = {
        'tabla_mapa': 'tabla_mapa_tmin_2024.csv',
        'frio': 'ranking_top15_frio_2024.csv',
        'calor': 'ranking_top15_calor_2024.csv'
    }
    
    data = {}
    for key, filename in files.items():
        if os.path.exists(filename):
            data[key] = pd.read_csv(filename)
        else:
            st.warning(f"⚠️ Archivo no encontrado: {filename}")
            data[key] = None
    
    return data

# Cargar datos
with st.spinner("Cargando datos..."):
    data = load_data()

# ============================================================================
# SIDEBAR - FILTROS Y ESTADÍSTICAS
# ============================================================================
st.sidebar.header("📊 Estadísticas Generales")

if data['tabla_mapa'] is not None:
    df_main = data['tabla_mapa']
    
    # Estadísticas básicas
    st.sidebar.metric("Total Distritos", len(df_main))
    
    if 'mean' in df_main.columns:
        st.sidebar.metric("Tmin Promedio Nacional", f"{df_main['mean'].mean():.2f}°C")
        st.sidebar.metric("Tmin Más Baja", f"{df_main['mean'].min():.2f}°C")
        st.sidebar.metric("Tmin Más Alta", f"{df_main['mean'].max():.2f}°C")
    
    # Filtro de umbral
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros")
    
    if 'mean' in df_main.columns:
        threshold = st.sidebar.slider(
            "Filtrar por temperatura (°C)",
            float(df_main['mean'].min()),
            float(df_main['mean'].max()),
            (float(df_main['mean'].min()), float(df_main['mean'].max()))
        )
        
        # Aplicar filtro
        df_filtered = df_main[
            (df_main['mean'] >= threshold[0]) & 
            (df_main['mean'] <= threshold[1])
        ]
        st.sidebar.info(f"Mostrando {len(df_filtered)} distritos")

# ============================================================================
# TABS PRINCIPALES
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📍 Mapa y Rankings",
    "📊 Análisis Estadístico", 
    "🎯 Políticas Públicas",
    "💾 Datos y Descargas"
])

# ============================================================================
# TAB 1: MAPA Y RANKINGS
# ============================================================================
with tab1:
    st.header("Mapa de Temperatura Mínima Promedio")
    
    # Mostrar mapa estático si existe
    if os.path.exists("static_map.png"):
        img = Image.open("static_map.png")
        st.image(img, use_container_width=True, caption="Distribución espacial de Tmin en Perú (2024)")
    else:
        st.warning("⚠️ Imagen del mapa no encontrada: static_map.png")
    
    st.markdown("---")
    
    # Rankings lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("❄️ Top 15 Distritos Más Fríos")
        if data['frio'] is not None:
            st.dataframe(
                data['frio'].style.format({
                    col: "{:.2f}" for col in data['frio'].select_dtypes(include=[np.number]).columns
                }),
                use_container_width=True,
                height=400
            )
        else:
            st.error("No se pudo cargar el ranking de frío")
    
    with col2:
        st.subheader("🔥 Top 15 Distritos Más Cálidos")
        if data['calor'] is not None:
            st.dataframe(
                data['calor'].style.format({
                    col: "{:.2f}" for col in data['calor'].select_dtypes(include=[np.number]).columns
                }),
                use_container_width=True,
                height=400
            )
        else:
            st.error("No se pudo cargar el ranking de calor")

# ============================================================================
# TAB 2: ANÁLISIS ESTADÍSTICO
# ============================================================================
with tab2:
    if data['tabla_mapa'] is not None and 'mean' in data['tabla_mapa'].columns:
        df_stats = data['tabla_mapa']
        
        st.header("Distribución de Temperaturas")
        
        # Histograma
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.hist(df_stats['mean'].dropna(), bins=50, color='steelblue', edgecolor='black', alpha=0.7)
        ax.axvline(df_stats['mean'].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df_stats["mean"].mean():.2f}°C')
        ax.axvline(df_stats['mean'].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df_stats["mean"].median():.2f}°C')
        ax.set_xlabel('Temperatura Mínima Promedio (°C)', fontsize=12)
        ax.set_ylabel('Número de Distritos', fontsize=12)
        ax.set_title('Distribución de Tmin Promedio por Distrito - Perú 2024', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(alpha=0.3)
        st.pyplot(fig)
        
        st.markdown("---")
        
        # Estadísticas por departamento (si existe la columna)
        if 'DEPARTAMENTO' in df_stats.columns or 'departamento' in df_stats.columns:
            dept_col = 'DEPARTAMENTO' if 'DEPARTAMENTO' in df_stats.columns else 'departamento'
            
            st.subheader("📍 Estadísticas por Departamento")
            
            dept_stats = df_stats.groupby(dept_col)['mean'].agg([
                ('Promedio', 'mean'),
                ('Mínimo', 'min'),
                ('Máximo', 'max'),
                ('Desv. Estándar', 'std'),
                ('N° Distritos', 'count')
            ]).round(2).sort_values('Promedio')
            
            st.dataframe(dept_stats, use_container_width=True)
            
            # Gráfico de barras por departamento
            st.subheader("Tmin Promedio por Departamento")
            fig2, ax2 = plt.subplots(figsize=(12, 8))
            dept_means = df_stats.groupby(dept_col)['mean'].mean().sort_values()
            dept_means.plot(kind='barh', ax=ax2, color='coral')
            ax2.set_xlabel('Temperatura Mínima Promedio (°C)', fontsize=12)
            ax2.set_ylabel('Departamento', fontsize=12)
            ax2.set_title('Tmin Promedio por Departamento', fontsize=14, fontweight='bold')
            ax2.grid(axis='x', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)
        
        st.markdown("---")
        
        # Métricas clave
        st.subheader("🎯 Métricas Clave")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            bajo_cero = len(df_stats[df_stats['mean'] < 0])
            st.metric("Distritos < 0°C", bajo_cero, delta=f"{(bajo_cero/len(df_stats)*100):.1f}%")
        
        with col2:
            bajo_4 = len(df_stats[df_stats['mean'] < 4])
            st.metric("Distritos < 4°C", bajo_4, delta=f"{(bajo_4/len(df_stats)*100):.1f}%")
        
        with col3:
            rango_frio = len(df_stats[(df_stats['mean'] >= 4) & (df_stats['mean'] < 10)])
            st.metric("Distritos 4-10°C", rango_frio, delta=f"{(rango_frio/len(df_stats)*100):.1f}%")
        
        with col4:
            templado = len(df_stats[df_stats['mean'] >= 10])
            st.metric("Distritos ≥ 10°C", templado, delta=f"{(templado/len(df_stats)*100):.1f}%")

# ============================================================================
# TAB 4: DATOS Y DESCARGAS
# ============================================================================
with tab4:
    st.header("💾 Datos y Descargas")
    
    st.markdown("""
    ### Archivos Disponibles
    Descarga los datos procesados en formato CSV para análisis adicional.
    """)
    
    # Tabla completa
    if data['tabla_mapa'] is not None:
        st.subheader("📋 Tabla Completa de Datos")
        st.dataframe(data['tabla_mapa'], use_container_width=True, height=400)
        
        # Botón de descarga
        csv = data['tabla_mapa'].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⬇️ Descargar Tabla Completa (CSV)",
            data=csv,
            file_name="tabla_completa_tmin_2024.csv",
            mime="text/csv"
        )
    
    st.markdown("---")
    
    # Rankings
    col1, col2 = st.columns(2)
    
    with col1:
        if data['frio'] is not None:
            csv_frio = data['frio'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar Ranking Frío (CSV)",
                data=csv_frio,
                file_name="ranking_frio_2024.csv",
                mime="text/csv"
            )
    
    with col2:
        if data['calor'] is not None:
            csv_calor = data['calor'].to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ Descargar Ranking Calor (CSV)",
                data=csv_calor,
                file_name="ranking_calor_2024.csv",
                mime="text/csv"
            )
    
    st.markdown("---")
    
    # Información del raster
    st.subheader("🗺️ Datos Raster")
    
    raster_info = []
    if os.path.exists("tmin_raster.tif"):
        raster_info.append("✅ tmin_raster.tif - Raster completo")
    if os.path.exists("recorte.tif"):
        raster_info.append("✅ recorte.tif - Raster recortado")
    
    if raster_info:
        for info in raster_info:
            st.markdown(info)
    else:
        st.warning("⚠️ No se encontraron archivos raster")
    
    st.markdown("---")
    
    # Metadatos
    st.subheader("ℹ️ Metadatos")
    st.markdown("""
    - **Fuente de datos:** Análisis de temperatura mínima 2024
    - **Nivel territorial:** Distrital
    - **Unidad:** Grados Celsius (°C)
    - **Año de referencia:** 2024
    - **Total de distritos analizados:** """ + (str(len(data['tabla_mapa'])) if data['tabla_mapa'] is not None else "N/A") + """
    """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("🛠️ Built with Streamlit | 📊 Data Analysis - Peru Tmin 2024")
