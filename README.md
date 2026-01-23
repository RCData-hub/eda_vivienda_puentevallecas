# 🏠 Análisis Interactivo del precio de la vivienda en Puente de Vallecas

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Bokeh](https://img.shields.io/badge/bokeh-3.7.3-orange.svg)
![Pandas](https://img.shields.io/badge/pandas-latest-150458.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Análisis exploratorio de datos (EDA) del mercado inmobiliario en el distrito de Puente de Vallecas y sus barrios (Entrevías, Numancia, Palomeras Bajas, Palomeras Sureste, Portazgo, San Diego), Madrid. Este proyecto examina la evolución temporal de precios, comparaciones entre viviendas nuevas y usadas, y tendencias del mercado inmobiliario local mediante visualizaciones interactivas con Bokeh.

Fuente de los datos:
[Banco de datos del Ayuntamiento de madrid](https://servpub.madrid.es/CSEBD_WBINTER/seleccionSerie.html?numSerie=0504020100060)
## 📋 Descripción

Este proyecto realiza un análisis exhaustivo del mercado inmobiliario en Puente de Vallecas utilizando datos de propiedades disponibles. El objetivo es identificar patrones de precios, características más valoradas y insights relevantes para compradores, vendedores e inversores.

## 🎯 Objetivos

- Analizar la evolución temporal de precios por m² en Puente de Vallecas y sus barrios (2007-2024)
- Comparar precios entre viviendas nuevas y usadas
- Identificar tendencias y patrones en el mercado inmobiliario local
- Generar visualizaciones interactivas y dashboards dinámicos con Bokeh
- Proporcionar análisis estadísticos (mediana, media, percentiles) para la toma de decisiones
- Detectar el impacto de eventos económicos (crisis 2008, recuperación gradual)

## 📁 Estructura del Proyecto

```
eda_vivienda_puentevallecas/
│
├── data/                           # Datos utilizados en el análisis
│   └── clean/                      # Datos limpios y procesados
│       └── vivienda_puente_agrupado.csv
│
├── notebooks/                      # Jupyter notebooks con análisis exploratorio
│   └── eda_exploratorio.ipynb      # Análisis paso a paso
│
├── .ipynb_checkpoints/            # Checkpoints de Jupyter (auto-generado)
│
├── .virtual_documents/            # Documentos virtuales (auto-generado)
│
├── main.py                        # 🔥 Script principal - análisis interactivo completo
│                                  #    - Carga de datos (CSV/URL/ejemplo)
│                                  #    - Generación de 4 visualizaciones Bokeh
│                                  #    - Exportación a HTML
│
├── trial.py                       # Scripts de prueba y experimentación
│
├── analisis_precios_inmobiliarios.html  # 📊 OUTPUT: Visualización HTML interactiva
│                                        #    - 4 gráficos Bokeh completos
│                                        #    - Dashboard con controles dinámicos
│                                        #    - Standalone (sin dependencias)
│
├── eda_vivienda_puentevallecas.code-workspace  # Workspace de VS Code
│
├── LICENSE                        # Licencia MIT
│
├── README.md                      # 📖 Este archivo
│
└── .gitattributes                # Configuración Git LFS
```

### 🎨 Archivos Clave

- **`main.py`**: Script principal con 4 funciones de visualización + cargador interactivo de datos
- **`analisis_precios_inmobiliarios.html`**: Resultado final - visualización web interactiva
- **`data/clean/`**: Datos procesados listos para análisis
- **`notebooks/`**: Exploración paso a paso en Jupyter

## 🚀 Instalación y Uso

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (para visualizar el HTML)
- Jupyter Notebook (opcional, para exploración interactiva)

### Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/RCData-hub/eda_vivienda_puentevallecas.git
cd eda_vivienda_puentevallecas
```

2. (Recomendado) Crea y activa un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install pandas numpy bokeh jupyter
```

**Dependencias principales:**
- `pandas` - Manipulación de datos
- `numpy` - Operaciones numéricas
- `bokeh>=3.7.3` - Visualizaciones interactivas
- `jupyter` - Notebooks (opcional)

### Ejecución

#### Opción 1: Análisis Interactivo Completo
El script `main.py` ofrece un menú interactivo con múltiples opciones de carga de datos:

```bash
python main.py
```

**Opciones disponibles:**
1. 📂 Cargar desde archivo CSV (con validación automática)
2. 📝 Usar datos de ejemplo (para testing)
3. 🔗 Cargar desde URL
4. ❌ Salir

El script genera automáticamente `analisis_precios_inmobiliarios.html` con todas las visualizaciones.

#### Opción 2: Carga Rápida desde CSV
Si ya tienes tu archivo CSV preparado:

```python
from main import quick_load_csv

# Cargar y analizar directamente
layout, stats = quick_load_csv('data/clean/vivienda_puente_agrupado.csv')
```

#### Opción 3: Exploración en Jupyter
Para exploración interactiva, abre los notebooks:

```bash
jupyter notebook
# Navega a /notebooks y abre el notebook de análisis
```

#### Visualización de Resultados
Abre el archivo generado en tu navegador:

```bash
# Linux/Mac
open analisis_precios_inmobiliarios.html

# Windows
start analisis_precios_inmobiliarios.html
```

El archivo HTML contiene:
- ✅ Todas las visualizaciones interactivas
- ✅ Tooltips con información detallada
- ✅ Controles dinámicos (filtros, selectores)
- ✅ Sin dependencias externas (standalone)

## 📊 Tecnologías Utilizadas

- **Python 3.8+**: Lenguaje principal de programación
- **Pandas**: Manipulación y análisis de datos tabulares
- **NumPy**: Operaciones numéricas y estadísticas
- **Bokeh 3.7.3**: Visualizaciones interactivas y dashboards dinámicos
- **Jupyter Notebook**: Análisis exploratorio interactivo (notebooks incluidos en `/notebooks`)
- **HTML/JavaScript**: Exportación de visualizaciones interactivas

## 🔍 Principales Análisis Realizados

El proyecto incluye **4 visualizaciones interactivas principales** generadas con Bokeh:

### 1. 📈 Evolución de Precios por Distrito
- Líneas temporales para cada barrio de Puente de Vallecas
- Período: 2007-2024
- Distritos analizados: Entrevías, Numancia, Palomeras Bajas, Palomeras Sureste, Portazgo, San Diego
- Tooltips interactivos con información detallada

### 2. 🆚 Comparación: Viviendas Nuevas vs Usadas
- Análisis comparativo de precios por m² entre viviendas nuevas y usadas
- Top 6 distritos con datos más completos
- Visualización de diferenciales de precio
- Identificación de tendencias en cada segmento

### 3. 🎛️ Dashboard Interactivo
- **Controles dinámicos**:
  - Selector múltiple de distritos (checkboxes)
  - Selector de métrica (Precio Total / Nuevas / Usadas)
  - Filtro de rango de años (slider)
- Actualización en tiempo real con JavaScript callbacks
- Leyendas clicables para ocultar/mostrar series

### 4. 📊 Análisis Estadístico
- Estadísticas descriptivas por año:
  - Media y mediana de precios
  - Rango intercuartílico (Q1-Q3)
  - Valores mínimos y máximos
  - Desviación estándar
- Visualización de bandas de confianza
- Detección de outliers y valores atípicos

## 📈 Resultados Principales

### 🏘️ Distritos Analizados
El análisis cubre 7 barrios principales de Puente de Vallecas:
- Puente de Vallecas (distrito completo)
- Entrevías
- Numancia  
- Palomeras Bajas
- Palomeras Sureste
- Portazgo
- San Diego

### 📊 Período de Análisis
- **Rango temporal**: 2007-2024 (18 años)
- **Datos procesados**: 126+ registros anuales por distrito
- **Métricas clave**: 
  - Precio por m² total
  - Precio por m² viviendas nuevas
  - Precio por m² viviendas usadas

### 💡 Insights Clave

#### Tendencias Temporales
- 📉 **Crisis 2008-2012**: Caída gradual de precios (-30% aprox.)
- 📈 **Recuperación 2012-2024**: Crecimiento sostenido (+3% anual)
- 🎯 **Precios actuales (2024)**: Rango 2,100-2,600 €/m² según barrio

#### Comparativa Nuevas vs Usadas
- 🆕 **Viviendas nuevas**: Premium de +5-15% sobre precio medio
- 🏚️ **Viviendas usadas**: Descuento de 0-5% sobre precio medio
- 📊 **Diferencial promedio**: ~200-300 €/m²

#### Ranking de Distritos (2024)
1. 🥇 **Numancia**: ~2,580 €/m² (precio más alto)
2. 🥈 **Portazgo**: ~2,450 €/m²
3. 🥉 **San Diego**: ~2,430 €/m²
4. **Palomeras Sureste**: ~2,380 €/m²
5. **Palomeras Bajas**: ~2,350 €/m²
6. **Entrevías**: ~2,320 €/m²

### 📉 Estadísticas Generales
```python
Precio medio general: ~2,400 €/m²
Variabilidad (std): ~150-200 €/m²
Rango intercuartílico: 2,200-2,600 €/m²
```

**Nota**: Los resultados detallados se encuentran en el archivo HTML generado y en los notebooks de análisis.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Si deseas colaborar:

1. Haz un Fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Realiza tus cambios y haz commit (`git commit -m 'Añade nueva característica'`)
4. Sube los cambios a tu rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### 💡 Ideas para Contribuir
- Añadir más métricas de análisis (superficie media, número de habitaciones)
- Incorporar datos de otras fuentes (portales inmobiliarios)
- Crear visualizaciones adicionales (mapas de calor, gráficos 3D)
- Mejorar la interfaz del dashboard interactivo
- Añadir exportación a PDF de reportes
- Implementar modelos predictivos de precios

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**RCData-hub**

- GitHub: [@RCData-hub](https://github.com/RCData-hub)

<div align="center">

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub ⭐

</div>
