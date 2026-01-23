import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.layouts import column, row
from bokeh.models import (
    HoverTool,
    ColumnDataSource,
    Select,
    CheckboxGroup,
    RangeSlider,
    Div,
    CustomJS,
)
from bokeh.palettes import Category20, Set3, Turbo256

# ===============================
# CONFIGURACIÓN Y CARGA DE DATOS
# ===============================


def load_csv_data(file_path, encoding="utf-8"):
    """
    Cargar DataFrame desde archivo CSV con validación

    Parameters:
    -----------
    file_path : str
        Ruta al archivo CSV
    encoding : str, optional
        Codificación del archivo (default: 'utf-8')
        Otras opciones comunes: 'latin1', 'cp1252', 'iso-8859-1'

    Returns:
    --------
    pd.DataFrame
        DataFrame con los datos cargados y validados
    """
    print(f"📂 Cargando datos desde: {'data/clean/vivienda_puente_agrupado.csv'}")

    try:
        # Intentar cargar con diferentes separadores y codificaciones
        separators = [",", ";", "\t"]
        encodings = [encoding, "utf-8", "latin1", "cp1252", "iso-8859-1"]

        df = None
        used_sep = None
        used_encoding = None

        for enc in encodings:
            for sep in separators:
                try:
                    df_temp = pd.read_csv(file_path, sep=sep, encoding=enc)

                    # Verificar si tiene las columnas esperadas
                    expected_columns = [
                        "distrito",
                        "year",
                        "price_m2_total",
                        "price_m2_nuevas",
                        "price_m2_usadas",
                    ]

                    if all(col in df_temp.columns for col in expected_columns):
                        df = df_temp
                        used_sep = sep
                        used_encoding = enc
                        print("✅ Archivo cargado exitosamente:")
                        print(f"   - Separador: '{used_sep}'")
                        print(f"   - Codificación: {used_encoding}")
                        break
                except (
                    UnicodeDecodeError,
                    pd.errors.EmptyDataError,
                    pd.errors.ParserError,
                ):
                    continue

            if df is not None:
                break

        if df is None:
            raise ValueError("No se pudo cargar el archivo con ninguna configuración")

        # Validar estructura de datos
        print(f"📊 Datos cargados: {len(df)} filas, {len(df.columns)} columnas")
        print(f"Columnas encontradas: {list(df.columns)}")

        # Verificar columnas requeridas
        required_columns = [
            "distrito",
            "year",
            "price_m2_total",
            "price_m2_nuevas",
            "price_m2_usadas",
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"⚠️  Columnas faltantes: {missing_columns}")
            print(
                "❌ El DataFrame debe tener las columnas: distrito, year, price_m2_total, price_m2_nuevas, price_m2_usadas"
            )

            # Intentar mapear columnas similares
            column_mapping = suggest_column_mapping(df.columns, required_columns)
            if column_mapping:
                print("💡 Posibles mapeos de columnas:")
                for original, suggested in column_mapping.items():
                    print(f"   '{original}' -> '{suggested}'")

                response = input(
                    "\n¿Deseas aplicar estos mapeos automáticamente? (y/n): "
                )
                if response.lower() == "y":
                    df = df.rename(columns=column_mapping)
                    print("✅ Columnas renombradas automáticamente")
                else:
                    raise ValueError("Columnas requeridas no encontradas")
            else:
                raise ValueError(
                    "Columnas requeridas no encontradas y no se pueden mapear automáticamente"
                )

        # Convertir tipos de datos
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        price_columns = ["price_m2_total", "price_m2_nuevas", "price_m2_usadas"]

        for col in price_columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Mostrar información básica
        print("\n📈 Resumen de datos:")
        print(f"   - Distritos únicos: {df['distrito'].nunique()}")
        print(f"   - Años: {df['year'].min():.0f} - {df['year'].max():.0f}")
        print(
            f"   - Registros con precio total > 0: {(df['price_m2_total'] > 0).sum()}"
        )

        # Mostrar primeras filas
        print("\n🔍 Primeras 5 filas:")
        print(df.head())

        return df

    except FileNotFoundError:
        print(f"❌ Error: Archivo no encontrado en '{file_path}'")
        print("💡 Verifica que la ruta sea correcta y que el archivo exista")
        raise
    except Exception as e:
        print(f"❌ Error al cargar el archivo: {str(e)}")
        raise


def suggest_column_mapping(existing_columns, required_columns):
    """
    Sugerir mapeos automáticos de columnas basado en similitud de nombres
    """
    import difflib

    mapping = {}

    # Palabras clave para cada columna requerida
    column_keywords = {
        "distrito": ["distrito", "district", "zona", "area", "barrio", "neighborhood"],
        "year": ["year", "año", "fecha", "date", "periodo", "period"],
        "price_m2_total": [
            "price_m2_total",
            "precio_total",
            "precio_m2",
            "price_total",
            "total",
        ],
        "price_m2_nuevas": [
            "price_m2_nuevas",
            "precio_nuevas",
            "nuevas",
            "new",
            "nueva",
        ],
        "price_m2_usadas": [
            "price_m2_usadas",
            "precio_usadas",
            "usadas",
            "used",
            "segunda",
        ],
    }

    for required_col in required_columns:
        best_match = None
        best_ratio = 0

        for existing_col in existing_columns:
            # Calcular similitud directa
            ratio = difflib.SequenceMatcher(
                None, required_col.lower(), existing_col.lower()
            ).ratio()

            # Buscar palabras clave
            for keyword in column_keywords[required_col]:
                if keyword in existing_col.lower():
                    ratio = max(ratio, 0.8)  # Dar alta prioridad a palabras clave

            if ratio > best_ratio and ratio > 0.6:  # Umbral de similitud
                best_ratio = ratio
                best_match = existing_col

        if best_match:
            mapping[best_match] = required_col

    return mapping if mapping else None


def load_sample_data():
    """
    Crear datos de ejemplo si no se proporciona archivo CSV
    """
    print("📝 Generando datos de ejemplo...")

    # Distritos de ejemplo (basados en tu muestra)
    distritos = [
        "Puente de Vallecas",
        "Entrevías",
        "San Diego",
        "Palomeras Bajas",
        "Palomeras Sureste",
        "Portazgo",
        "Numancia",
        "Villa de Vallecas",
        "Casco Histórico de Vallecas",
        "Santa Catalina",
    ]

    years = list(range(2007, 2025))

    # Generar datos sintéticos más realistas
    np.random.seed(42)
    data = []

    base_prices = {
        "Puente de Vallecas": 3200,
        "Entrevías": 2800,
        "San Diego": 2900,
        "Palomeras Bajas": 2700,
        "Palomeras Sureste": 2600,
        "Portazgo": 2850,
        "Numancia": 3100,
        "Villa de Vallecas": 2950,
        "Casco Histórico de Vallecas": 3000,
        "Santa Catalina": 2750,
    }

    for distrito in distritos:
        base_price = base_prices[distrito]

        for year in years:
            # Simular crisis 2008-2012 y recuperación gradual
            if year <= 2008:
                factor = 1.0
            elif year <= 2012:
                factor = 0.7 + (year - 2008) * -0.05  # Caída gradual
            else:
                factor = 0.55 + (year - 2012) * 0.03  # Recuperación gradual

            # Agregar variabilidad
            noise_factor = np.random.uniform(0.9, 1.1)

            price_total = base_price * factor * noise_factor

            # Precios nuevas vs usadas
            price_nuevas = price_total * np.random.uniform(
                1.05, 1.15
            )  # 5-15% más caras
            price_usadas = price_total * np.random.uniform(
                0.95, 1.05
            )  # Ligeramente más baratas

            # Algunos años sin datos (realista)
            if np.random.random() < 0.1:  # 10% de probabilidad de datos faltantes
                price_total = price_nuevas = price_usadas = 0.0

            data.append(
                {
                    "distrito": distrito,
                    "year": year,
                    "price_m2_total": round(price_total, 2),
                    "price_m2_nuevas": round(price_nuevas, 2),
                    "price_m2_usadas": round(price_usadas, 2),
                }
            )

    df = pd.DataFrame(data)
    print(f"✅ Datos de ejemplo generados: {len(df)} registros")

    return df


def interactive_data_loader():
    """
    Cargador interactivo de datos con opciones múltiples
    """
    print("=" * 60)
    print("🏠 ANÁLISIS DE PRECIOS INMOBILIARIOS CON BOKEH")
    print("=" * 60)
    print("\n¿Cómo quieres cargar los datos?")
    print("\n1. 📂 Cargar desde archivo CSV")
    print("2. 📝 Usar datos de ejemplo")
    print("3. 🔗 Cargar desde URL")
    print("4. ❌ Salir")

    while True:
        try:
            option = input("\nSelecciona una opción (1-4): ").strip()

            if option == "1":
                return load_from_csv()
            elif option == "2":
                return load_sample_data()
            elif option == "3":
                return load_from_url()
            elif option == "4":
                print("👋 ¡Hasta luego!")
                return None
            else:
                print("❌ Opción inválida. Por favor selecciona 1, 2, 3 o 4.")

        except KeyboardInterrupt:
            print("\n👋 ¡Hasta luego!")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print("Intenta nuevamente...")


def load_from_csv():
    """Cargar datos desde archivo CSV con validación interactiva"""

    while True:
        file_path = input("📂 Introduce la ruta al archivo CSV: ").strip().strip("\"'")

        if not file_path:
            print("❌ Debes introducir una ruta")
            continue

        try:
            # Preguntar por codificación si es necesario
            encoding = input("🔤 Codificación del archivo (Enter para UTF-8): ").strip()
            if not encoding:
                encoding = "utf-8"

            df = load_csv_data(file_path, encoding)
            return df

        except FileNotFoundError:
            print(f"❌ Archivo no encontrado: {file_path}")
            retry = input("¿Intentar con otra ruta? (y/n): ")
            if retry.lower() != "y":
                return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            retry = input("¿Intentar nuevamente? (y/n): ")
            if retry.lower() != "y":
                return None


def load_from_url():
    """Cargar datos desde URL"""

    while True:
        url = input("🔗 Introduce la URL del archivo CSV: ").strip()

        if not url:
            print("❌ Debes introducir una URL")
            continue

        try:
            print(f"🌐 Descargando desde: {url}")
            df = pd.read_csv(url)

            # Validar estructura
            required_columns = [
                "distrito",
                "year",
                "price_m2_total",
                "price_m2_nuevas",
                "price_m2_usadas",
            ]
            missing_columns = [col for col in required_columns if col not in df.columns]

            if missing_columns:
                print(f"⚠️  Columnas faltantes: {missing_columns}")
                print("El archivo debe tener las columnas requeridas")
                return None

            print(f"✅ Datos cargados desde URL: {len(df)} registros")
            return df

        except Exception as e:
            print(f"❌ Error al cargar desde URL: {str(e)}")
            retry = input("¿Intentar con otra URL? (y/n): ")
            if retry.lower() != "y":
                return None


def load_and_prepare_data(df):
    """
    Preparar el DataFrame para visualización
    df: DataFrame con columnas ['distrito', 'year', 'price_m2_total', 'price_m2_nuevas', 'price_m2_usadas']
    """
    print("📊 Preparando datos...")

    # Limpiar datos - reemplazar 0s con NaN para mejor visualización
    price_columns = ["price_m2_total", "price_m2_nuevas", "price_m2_usadas"]
    df_clean = df.copy()

    for col in price_columns:
        df_clean[col] = df_clean[col].replace(0, np.nan)

    # Estadísticas básicas
    print(f"Distritos únicos: {df_clean['distrito'].nunique()}")
    print(f"Rango de años: {df_clean['year'].min()} - {df_clean['year'].max()}")
    print(f"Distritos: {sorted(df_clean['distrito'].unique())}")

    return df_clean


# ===============================
# GRÁFICO 1: EVOLUCIÓN POR DISTRITO
# ===============================


def create_district_evolution_plot(df):
    """Crear gráfico de evolución de precios por distrito"""

    distritos = sorted(df["distrito"].unique())
    colors = (
        Category20[len(distritos)]
        if len(distritos) <= 20
        else Turbo256[:: len(Turbo256) // len(distritos)]
    )

    p = figure(
        title="Evolución de Precios por m² - Total por Distrito",
        x_axis_label="Año",
        y_axis_label="Precio €/m²",
        width=1000,
        height=500,
        tools="pan,wheel_zoom,box_zoom,reset,save,crosshair",
    )

    # Crear líneas para cada distrito
    sources = {}
    for i, distrito in enumerate(distritos):
        distrito_data = df[df["distrito"] == distrito].sort_values("year")

        # Filtrar valores no nulos
        distrito_data = distrito_data.dropna(subset=["price_m2_total"])

        if len(distrito_data) > 0:
            source = ColumnDataSource(
                {
                    "year": distrito_data["year"],
                    "price": distrito_data["price_m2_total"],
                    "distrito": [distrito] * len(distrito_data),
                }
            )
            sources[distrito] = source

            # Línea principal
            p.line(
                "year",
                "price",
                source=source,
                legend_label=distrito,
                line_width=2,
                color=colors[i % len(colors)],
                alpha=0.8,
            )

            # Puntos para hover
            p.circle(
                "year",
                "price",
                source=source,
                size=5,
                color=colors[i % len(colors)],
                alpha=0.6,
            )

    # Configurar hover
    hover = HoverTool(
        tooltips=[
            ("Distrito", "@distrito"),
            ("Año", "@year"),
            ("Precio", "@price{0,0} €/m²"),
        ]
    )
    p.add_tools(hover)

    # Personalizar leyenda
    p.add_layout(p.legend[0], "right")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "8pt"

    return p, sources


# ===============================
# GRÁFICO 2: COMPARACIÓN NUEVAS VS USADAS
# ===============================


def create_nuevas_vs_usadas_plot(df, selected_districts=None):
    """Comparar precios de viviendas nuevas vs usadas"""

    if selected_districts is None:
        # Seleccionar distritos con datos más completos
        district_completeness = (
            df.groupby("distrito")[["price_m2_nuevas", "price_m2_usadas"]]
            .count()
            .min(axis=1)
        )
        selected_districts = district_completeness.nlargest(6).index.tolist()

    p = figure(
        title="Comparación Precios: Nuevas vs Usadas - Top Distritos",
        x_axis_label="Año",
        y_axis_label="Precio €/m²",
        width=1000,
        height=500,
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    colors = Set3[12]  # Paleta con colores suaves

    for i, distrito in enumerate(selected_districts):
        distrito_data = df[df["distrito"] == distrito].sort_values("year")

        # Datos para nuevas
        nuevas_data = distrito_data.dropna(subset=["price_m2_nuevas"])
        if len(nuevas_data) > 0:
            p.line(
                nuevas_data["year"],
                nuevas_data["price_m2_nuevas"],
                legend_label=f"{distrito} (Nuevas)",
                line_width=2,
                color=colors[i % len(colors)],
                line_dash="solid",
            )

        # Datos para usadas
        usadas_data = distrito_data.dropna(subset=["price_m2_usadas"])
        if len(usadas_data) > 0:
            p.line(
                usadas_data["year"],
                usadas_data["price_m2_usadas"],
                legend_label=f"{distrito} (Usadas)",
                line_width=2,
                color=colors[i % len(colors)],
                line_dash="dashed",
                alpha=0.7,
            )

    # Hover tool
    hover = HoverTool(tooltips=[("Año", "$x"), ("Precio", "$y{0,0} €/m²")])
    p.add_tools(hover)

    p.add_layout(p.legend[0], "right")
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "8pt"

    return p


# ===============================
# GRÁFICO 3: DASHBOARD INTERACTIVO
# ===============================


def create_interactive_dashboard(df):
    """Dashboard interactivo con controles"""

    distritos = sorted(df["distrito"].unique())
    years = sorted(df["year"].unique())

    # Datos iniciales - todos los distritos
    initial_districts = distritos[:5]  # Primeros 5 para no saturar

    # Crear figura principal
    p = figure(
        title="Dashboard Interactivo - Precios Inmobiliarios",
        x_axis_label="Año",
        y_axis_label="Precio €/m²",
        width=800,
        height=500,
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    # Preparar datos para ColumnDataSource
    sources = {}
    line_renderers = {}
    circle_renderers = {}
    colors = Category20[20]

    for i, distrito in enumerate(distritos):
        distrito_data = df[df["distrito"] == distrito].sort_values("year")
        distrito_data = distrito_data.dropna(subset=["price_m2_total"])

        if len(distrito_data) > 0:
            source_data = {
                "year": distrito_data["year"],
                "price_total": distrito_data["price_m2_total"],
                "price_nuevas": distrito_data["price_m2_nuevas"].fillna(0),
                "price_usadas": distrito_data["price_m2_usadas"].fillna(0),
                "distrito": [distrito] * len(distrito_data),
            }

            source = ColumnDataSource(source_data)
            sources[distrito] = source

            # Crear líneas (inicialmente ocultas excepto las primeras 5)
            visible = distrito in initial_districts

            line = p.line(
                "year",
                "price_total",
                source=source,
                legend_label=distrito,
                line_width=2,
                color=colors[i % len(colors)],
                visible=visible,
            )

            circles = p.circle(
                "year",
                "price_total",
                source=source,
                size=4,
                color=colors[i % len(colors)],
                visible=visible,
                alpha=0.6,
            )

            line_renderers[distrito] = line
            circle_renderers[distrito] = circles

    # Widgets de control

    # 1. Selector múltiple de distritos
    district_select = CheckboxGroup(
        labels=distritos,
        active=[i for i, d in enumerate(distritos) if d in initial_districts],
        width=250,
        height=300,
    )

    # 2. Selector de métrica
    metric_select = Select(
        title="Métrica:",
        value="price_total",
        options=[
            ("price_total", "Precio Total"),
            ("price_nuevas", "Viviendas Nuevas"),
            ("price_usadas", "Viviendas Usadas"),
        ],
        width=200,
    )

    # 3. Filtro de años
    year_range = RangeSlider(
        title="Rango de Años",
        start=min(years),
        end=max(years),
        value=(min(years), max(years)),
        step=1,
        width=300,
    )

    # JavaScript callbacks corregidos
    district_callback = CustomJS(
        args=dict(
            line_renderers=line_renderers,
            circle_renderers=circle_renderers,
            checkbox=district_select,
            districts=distritos,
        ),
        code="""
        const active_indices = checkbox.active;
    
        for (let i = 0; i < districts.length; i++) {
            const distrito = districts[i];
            
            // Verificar que existen los renderers
            if (line_renderers[distrito] && circle_renderers[distrito]) {
                const line = line_renderers[distrito];
                const circles = circle_renderers[distrito];
            
                if (active_indices.includes(i)) {
                    line.visible = true;
                    circles.visible = true;
                } else {
                    line.visible = false;
                    circles.visible = false;
                }
            }
        }
        """,
    )

    metric_callback = CustomJS(
        args=dict(
            line_renderers=line_renderers,
            circle_renderers=circle_renderers,
            sources=sources,
            metric_select=metric_select,
            plot=p,  # Asegúrate de pasar la referencia del plot
        ),
        code="""
        const metric = metric_select.value;
    
        // Actualizar los campos Y de todos los renderers
        for (const distrito in sources) {
            if (line_renderers[distrito] && circle_renderers[distrito]) {
                const line = line_renderers[distrito];
                const circles = circle_renderers[distrito];
            
                line.glyph.y.field = metric;
                circles.glyph.y.field = metric;
            }
        }
    
        // Actualizar título del eje Y
        const metric_names = {
            'price_total': 'Precio Total €/m²',
            'price_nuevas': 'Precio Nuevas €/m²',
            'price_usadas': 'Precio Usadas €/m²'
        };
        
        // Aplicar el nuevo título
        if (plot.left && plot.left.length > 0) {
            plot.left[0].axis_label = metric_names[metric] || metric;
        }
    
        // Forzar actualización de las fuentes de datos
        for (const distrito in sources) {
            sources[distrito].change.emit();
        }
        """,
    )
    year_callback = CustomJS(
        args=dict(
            sources=sources,
            year_slider=year_range,
            df_data=df.to_dict("series"),  # Pasar el DataFrame completo
        ),
        code="""
        const [min_year, max_year] = year_slider.value;
        
        // Obtener datos del DataFrame
        const all_years = df_data.year;
        const all_districts = df_data.distrito;
        const all_price_total = df_data.price_m2_total;
        const all_price_nuevas = df_data.price_m2_nuevas;
        const all_price_usadas = df_data.price_m2_usadas;
        
        // Filtrar para cada distrito
        for (const distrito in sources) {
            const source = sources[distrito];
            
            const filtered_data = {
                year: [],
                price_total: [],
                price_nuevas: [],
                price_usadas: [],
                distrito: []
            };
            
            // Filtrar datos por distrito y años
            for (let i = 0; i < all_years.length; i++) {
                if (all_districts[i] === distrito && 
                    all_years[i] >= min_year && 
                    all_years[i] <= max_year) {
                    
                    filtered_data.year.push(all_years[i]);
                    filtered_data.price_total.push(all_price_total[i] || 0);
                    filtered_data.price_nuevas.push(all_price_nuevas[i] || 0);
                    filtered_data.price_usadas.push(all_price_usadas[i] || 0);
                    filtered_data.distrito.push(distrito);
                }
            }
            
            source.data = filtered_data;
        }
        """,
    )

    # Conectar callbacks
    district_select.js_on_change("active", district_callback)
    metric_select.js_on_change("value", metric_callback)
    year_range.js_on_change("value", year_callback)

    # Hover tool
    hover = HoverTool(
        tooltips=[
            ("Distrito", "@distrito"),
            ("Año", "@year"),
            ("Precio", "$y{0,0} €/m²"),
        ]
    )
    p.add_tools(hover)

    # Layout
    controls = column(
        Div(text="<h3>Controles</h3>"),
        metric_select,
        Div(text="<h4>Seleccionar Distritos:</h4>"),
        district_select,
        year_range,
        width=300,
    )

    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.legend.label_text_font_size = "8pt"

    dashboard = row(controls, p)
    return dashboard


# ===============================
# GRÁFICO 4: ANÁLISIS ESTADÍSTICO
# ===============================


def create_statistical_analysis(df):
    """Crear análisis estadístico con percentiles y tendencias"""

    # Calcular estadísticas por año
    yearly_stats = (
        df.groupby("year")["price_m2_total"]
        .agg(
            [
                "count",
                "mean",
                "median",
                "std",
                lambda x: x.quantile(0.25),  # Q1
                lambda x: x.quantile(0.75),  # Q3
                "min",
                "max",
            ]
        )
        .round(2)
    )

    yearly_stats.columns = [
        "count",
        "mean",
        "median",
        "std",
        "q25",
        "q75",
        "min",
        "max",
    ]
    yearly_stats = yearly_stats.dropna()

    p = figure(
        title="Análisis Estadístico - Precios por Año",
        x_axis_label="Año",
        y_axis_label="Precio €/m²",
        width=1000,
        height=500,
        tools="pan,wheel_zoom,box_zoom,reset,save",
    )

    years = yearly_stats.index.tolist()

    # Área entre Q1 y Q3 (rango intercuartílico)
    p.varea(
        x=years,
        y1=yearly_stats["q25"],
        y2=yearly_stats["q75"],
        alpha=0.2,
        color="blue",
        legend_label="Rango Intercuartílico",
    )

    # Línea de mediana
    p.line(
        years, yearly_stats["median"], line_width=3, color="red", legend_label="Mediana"
    )

    # Línea de media
    p.line(
        years,
        yearly_stats["mean"],
        line_width=2,
        line_dash="dashed",
        color="green",
        legend_label="Media",
    )

    # Puntos min/max
    p.circle(
        years,
        yearly_stats["max"],
        size=6,
        color="orange",
        alpha=0.7,
        legend_label="Máximo",
    )

    p.circle(
        years,
        yearly_stats["min"],
        size=6,
        color="purple",
        alpha=0.7,
        legend_label="Mínimo",
    )

    p.legend.location = "top_left"
    return p, yearly_stats


# ===============================
# FUNCIÓN PRINCIPAL
# ===============================


def create_complete_analysis(df):
    """Crear análisis completo con todos los gráficos"""

    print("🏠 Creando análisis completo de precios inmobiliarios...")

    # Preparar datos
    df_clean = load_and_prepare_data(df)

    # Crear gráficos
    district_plot, sources = create_district_evolution_plot(df_clean)
    comparison_plot = create_nuevas_vs_usadas_plot(df_clean)
    dashboard = create_interactive_dashboard(df_clean)
    stats_plot, yearly_stats = create_statistical_analysis(df_clean)

    # Título general
    title_div = Div(
        text="""
    <h1 style="text-align: center; color: #2F4F4F;">
    📊 Análisis de Precios Inmobiliarios por Distrito
    </h1>
    <p style="text-align: center; font-size: 14px; color: #666;">
    Evolución temporal de precios por m² en diferentes distritos
    </p>
    """,
        width=1000,
        height=80,
    )

    # Layout final
    layout = column(title_div, district_plot, comparison_plot, dashboard, stats_plot)

    # Configurar salida
    output_file("analisis_precios_inmobiliarios.html")
    show(layout)

    print("✅ Análisis completado!")
    print("📁 Archivo guardado: analisis_precios_inmobiliarios.html")

    # Mostrar estadísticas
    print("\n📈 Estadísticas generales:")
    print(f"Precio medio general: {df_clean['price_m2_total'].mean():.2f} €/m²")
    print(
        f"Distrito más caro (promedio): {df_clean.groupby('distrito')['price_m2_total'].mean().idxmax()}"
    )
    print(
        f"Distrito más barato (promedio): {df_clean.groupby('distrito')['price_m2_total'].mean().idxmin()}"
    )

    return layout, yearly_stats


# ===============================
# FUNCIÓN PRINCIPAL CON CARGA AUTOMÁTICA
# ===============================


def main():
    """
    Función principal que ejecuta todo el proceso:
    1. Carga de datos (interactiva)
    2. Análisis completo
    3. Generación de visualizaciones
    """
    try:
        # Cargar datos de forma interactiva
        df = interactive_data_loader()

        if df is None:
            print("❌ No se cargaron datos. Finalizando...")
            return

        # Crear análisis completo
        print("\n" + "=" * 60)
        print("🚀 INICIANDO ANÁLISIS...")
        print("=" * 60)

        layout, stats = create_complete_analysis(df)

        # Mostrar resumen final
        print("\n" + "=" * 60)
        print("✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("📁 Archivo generado: analisis_precios_inmobiliarios.html")
        print(
            "🌐 Abre el archivo HTML en tu navegador para ver los gráficos interactivos"
        )

        return layout, stats

    except KeyboardInterrupt:
        print("\n👋 Proceso cancelado por el usuario")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {str(e)}")
        print("Por favor verifica tus datos y vuelve a intentar")


def quick_load_csv(file_path, encoding="utf-8"):
    """
    Función rápida para cargar CSV directamente (sin interactividad)

    Parameters:
    -----------
    file_path : str
        Ruta al archivo CSV
    encoding : str, optional
        Codificación del archivo (default: 'utf-8')

    Returns:
    --------
    tuple
        (layout, stats) del análisis completo

    Example:
    --------
    >>> layout, stats = quick_load_csv('mis_datos.csv')
    """
    print(f"⚡ Carga rápida desde: {file_path}")

    try:
        df = load_csv_data(file_path, encoding)
        layout, stats = create_complete_analysis(df)

        print("✅ Análisis completado - Carga rápida")
        return layout, stats

    except Exception as e:
        print(f"❌ Error en carga rápida: {str(e)}")
        raise


if __name__ == "__main__":
    # Ejecutar análisis interactivo
    print("\n🚀 Iniciando análisis interactivo...")
    main()
