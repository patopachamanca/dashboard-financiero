import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Estado financiero | Comercial Ejemplo",
    page_icon="📊",
    layout="wide",
)

EMPRESA = "Comercial Ejemplo, S.A."
MONEDA = "S/"
ANIOS = [2021, 2022, 2023, 2024, 2025]

DATOS = {
    "Efectivo y equivalentes": [70_000, 85_000, 100_000, 115_000, 140_000],
    "Cuentas por cobrar": [45_000, 55_000, 68_000, 82_000, 100_000],
    "Inventarios": [60_000, 70_000, 83_000, 98_000, 115_000],
    "Pagos anticipados": [8_000, 10_000, 12_000, 14_000, 16_000],
    "Propiedades, planta y equipo": [220_000, 250_000, 285_000, 320_000, 350_000],
    "Activos intangibles": [20_000, 24_000, 28_000, 32_000, 36_000],
    "Inversiones a largo plazo": [10_000, 12_000, 15_000, 20_000, 25_000],
    "Proveedores": [48_000, 55_000, 64_000, 76_000, 88_000],
    "Préstamos a corto plazo": [35_000, 40_000, 44_000, 50_000, 54_000],
    "Impuestos por pagar": [10_000, 12_000, 14_000, 17_000, 20_000],
    "Préstamos a largo plazo": [120_000, 140_000, 155_000, 170_000, 180_000],
    "Pasivos diferidos": [8_000, 9_000, 10_000, 12_000, 14_000],
    "Capital social": [180_000, 200_000, 220_000, 240_000, 260_000],
    "Utilidades retenidas": [32_000, 50_000, 84_000, 116_000, 166_000],
}

GRUPOS = {
    "Activos corrientes": [
        "Efectivo y equivalentes",
        "Cuentas por cobrar",
        "Inventarios",
        "Pagos anticipados",
    ],
    "Activos no corrientes": [
        "Propiedades, planta y equipo",
        "Activos intangibles",
        "Inversiones a largo plazo",
    ],
    "Pasivos corrientes": [
        "Proveedores",
        "Préstamos a corto plazo",
        "Impuestos por pagar",
    ],
    "Pasivos no corrientes": ["Préstamos a largo plazo", "Pasivos diferidos"],
    "Patrimonio": ["Capital social", "Utilidades retenidas"],
}

INDICADORES_EQUIPO = [
    {
        "estudiante": "Marti",
        "tipo_grafico": "radar",
        "kgi": "Aumentar las ventas anuales",
        "resultado_kgi": 17,
        "meta_kgi": 15,
        "unidad_kgi": "%",
        "direccion_kgi": "mayor",
        "kpis": [
            {"nombre": "Crecimiento de clientes", "resultado": 12, "meta": 10, "unidad": "%", "direccion": "mayor"},
            {"nombre": "Crecimiento del ticket promedio", "resultado": 6.2, "meta": 5, "unidad": "%", "direccion": "mayor"},
            {"nombre": "Conversión de oportunidades", "resultado": 22, "meta": 20, "unidad": "%", "direccion": "mayor"},
        ],
    },
    {
        "estudiante": "Blass",
        "tipo_grafico": "barras",
        "kgi": "Elevar la satisfacción del cliente",
        "resultado_kgi": 91,
        "meta_kgi": 90,
        "unidad_kgi": "%",
        "direccion_kgi": "mayor",
        "kpis": [
            {"nombre": "Quejas resueltas en 48 horas", "resultado": 97, "meta": 95, "unidad": "%", "direccion": "mayor"},
            {"nombre": "Tasa de recompra", "resultado": 63, "meta": 65, "unidad": "%", "direccion": "mayor"},
            {"nombre": "Tiempo de respuesta al cliente", "resultado": 20, "meta": 24, "unidad": "horas", "direccion": "menor"},
        ],
    },
    {
        "estudiante": "Fernando",
        "tipo_grafico": "medidores",
        "kgi": "Reducir los quiebres de inventario",
        "resultado_kgi": 1.8,
        "meta_kgi": 2,
        "unidad_kgi": "%",
        "direccion_kgi": "menor",
        "kpis": [
            {"nombre": "Rotación de inventario", "resultado": 7.4, "meta": 8, "unidad": "veces", "direccion": "mayor"},
            {"nombre": "Inventario obsoleto", "resultado": 4.1, "meta": 3, "unidad": "%", "direccion": "menor"},
            {"nombre": "Precisión del pronóstico de demanda", "resultado": 92, "meta": 90, "unidad": "%", "direccion": "mayor"},
        ],
    },
    {
        "estudiante": "Kenya",
        "tipo_grafico": "linea",
        "kgi": "Mejorar el cobro oportuno de facturas",
        "resultado_kgi": 93,
        "meta_kgi": 95,
        "unidad_kgi": "%",
        "direccion_kgi": "mayor",
        "kpis": [
            {"nombre": "Seguimiento de cobranza", "resultado": 97, "meta": 95, "unidad": "%", "direccion": "mayor"},
            {"nombre": "Cuentas vencidas", "resultado": 7, "meta": 5, "unidad": "%", "direccion": "menor"},
            {"nombre": "Días promedio de cobro", "resultado": 38, "meta": 35, "unidad": "días", "direccion": "menor"},
        ],
    },
]

df = pd.DataFrame(DATOS, index=ANIOS)
df.index.name = "Año"

df["Total activos corrientes"] = df[GRUPOS["Activos corrientes"]].sum(axis=1)
df["Total activos no corrientes"] = df[GRUPOS["Activos no corrientes"]].sum(axis=1)
df["Total activos"] = df["Total activos corrientes"] + df["Total activos no corrientes"]
df["Total pasivos corrientes"] = df[GRUPOS["Pasivos corrientes"]].sum(axis=1)
df["Total pasivos no corrientes"] = df[GRUPOS["Pasivos no corrientes"]].sum(axis=1)
df["Total pasivos"] = df["Total pasivos corrientes"] + df["Total pasivos no corrientes"]
df["Total patrimonio"] = df[GRUPOS["Patrimonio"]].sum(axis=1)
df["Capital de trabajo"] = df["Total activos corrientes"] - df["Total pasivos corrientes"]

if not (df["Total activos"] == df["Total pasivos"] + df["Total patrimonio"]).all():
    raise ValueError("Los datos no cuadran: activos debe ser igual a pasivos más patrimonio.")


def formato_um(valor):
    return f"{MONEDA} {valor:,.0f}"


def cumplimiento(resultado, meta, direccion):
    if meta == 0:
        return 100.0 if resultado == 0 else 0.0
    if direccion == "menor":
        return meta / resultado * 100 if resultado > 0 else 120.0
    return resultado / meta * 100


def formato_indicador(valor, unidad):
    return f"{valor:g} {unidad}"


def grafico_lineas(datos, y, titulo, nombres=None):
    fig = px.line(
        datos,
        x=datos.index,
        y=y,
        markers=True,
        title=titulo,
        labels={"index": "Año", "value": MONEDA, "variable": "Cuenta"},
    )
    if nombres:
        fig.for_each_trace(lambda trace: trace.update(name=nombres.get(trace.name, trace.name)))
    fig.update_layout(legend_title_text="", hovermode="x unified")
    fig.update_yaxes(tickformat=",.0f", title=MONEDA)
    return fig


st.title(f"📊 Dashboard financiero — {EMPRESA}")
st.caption(
    "Estado de situación financiera comparativo 2021–2025 | "
    "Empresa y cifras ficticias para fines académicos | Valores en soles (S/)"
)

with st.sidebar:
    st.header("Filtros")
    anios_seleccionados = st.slider(
        "Periodo mostrado",
        min_value=min(ANIOS),
        max_value=max(ANIOS),
        value=(min(ANIOS), max(ANIOS)),
    )
    anio = st.selectbox("Año del estado detallado", options=ANIOS, index=len(ANIOS) - 1)

periodo = df.loc[anios_seleccionados[0] : anios_seleccionados[1]]
datos_anio = df.loc[anio]

tab_dashboard, tab_indicadores, tab_estado, tab_datos = st.tabs(
    ["Dashboard", "KGI y KPI del equipo", "Estado financiero", "Datos base"]
)

with tab_dashboard:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total activos", formato_um(datos_anio["Total activos"]))
    col2.metric("Total pasivos", formato_um(datos_anio["Total pasivos"]))
    col3.metric("Patrimonio", formato_um(datos_anio["Total patrimonio"]))
    col4.metric("Efectivo", formato_um(datos_anio["Efectivo y equivalentes"]))

    fig_evolucion = grafico_lineas(
        periodo,
        ["Total activos", "Total pasivos", "Total patrimonio"],
        "Evolución de activos, pasivos y patrimonio",
    )
    st.plotly_chart(fig_evolucion, width="stretch")

    izquierda, derecha = st.columns(2)

    with izquierda:
        fig_activos = px.bar(
            periodo,
            x=periodo.index,
            y=GRUPOS["Activos corrientes"] + GRUPOS["Activos no corrientes"],
            title="Composición de activos por cuenta",
            labels={"index": "Año", "value": MONEDA, "variable": "Cuenta"},
        )
        fig_activos.update_layout(barmode="stack", legend_title_text="")
        fig_activos.update_yaxes(tickformat=",.0f", title=MONEDA)
        st.plotly_chart(fig_activos, width="stretch")

    with derecha:
        fig_pasivos = px.bar(
            periodo,
            x=periodo.index,
            y=GRUPOS["Pasivos corrientes"] + GRUPOS["Pasivos no corrientes"],
            title="Composición de pasivos por cuenta",
            labels={"index": "Año", "value": MONEDA, "variable": "Cuenta"},
        )
        fig_pasivos.update_layout(barmode="stack", legend_title_text="")
        fig_pasivos.update_yaxes(tickformat=",.0f", title=MONEDA)
        st.plotly_chart(fig_pasivos, width="stretch")

    izquierda, derecha = st.columns(2)

    with izquierda:
        fig_clasificacion = px.bar(
            periodo,
            x=periodo.index,
            y=[
                "Total activos corrientes",
                "Total activos no corrientes",
                "Total pasivos corrientes",
                "Total pasivos no corrientes",
            ],
            barmode="group",
            title="Activos y pasivos corrientes vs. no corrientes",
            labels={"index": "Año", "value": MONEDA, "variable": "Clasificación"},
        )
        fig_clasificacion.update_layout(legend_title_text="")
        fig_clasificacion.update_yaxes(tickformat=",.0f", title=MONEDA)
        st.plotly_chart(fig_clasificacion, width="stretch")

    with derecha:
        fig_financiamiento = px.area(
            periodo,
            x=periodo.index,
            y=["Total pasivos", "Total patrimonio"],
            title="Fuentes de financiamiento",
            labels={"index": "Año", "value": MONEDA, "variable": "Fuente"},
        )
        fig_financiamiento.update_layout(legend_title_text="")
        fig_financiamiento.update_yaxes(tickformat=",.0f", title=MONEDA)
        st.plotly_chart(fig_financiamiento, width="stretch")

    izquierda, derecha = st.columns(2)

    with izquierda:
        activos_detalle = pd.DataFrame(
            {"Cuenta": GRUPOS["Activos corrientes"] + GRUPOS["Activos no corrientes"],
             MONEDA: [datos_anio[cuenta] for cuenta in GRUPOS["Activos corrientes"] + GRUPOS["Activos no corrientes"]]}
        )
        fig_activos_anio = px.pie(
            activos_detalle,
            names="Cuenta",
            values=MONEDA,
            hole=0.42,
            title=f"Distribución de activos — {anio}",
        )
        st.plotly_chart(fig_activos_anio, width="stretch")

    with derecha:
        financiamiento_detalle = pd.DataFrame(
            {
                "Cuenta": ["Total pasivos", "Total patrimonio"],
                MONEDA: [datos_anio["Total pasivos"], datos_anio["Total patrimonio"]],
            }
        )
        fig_fuentes_anio = px.pie(
            financiamiento_detalle,
            names="Cuenta",
            values=MONEDA,
            hole=0.42,
            title=f"Pasivos y patrimonio — {anio}",
        )
        st.plotly_chart(fig_fuentes_anio, width="stretch")

    izquierda, derecha = st.columns(2)

    with izquierda:
        fig_capital_trabajo = px.bar(
            periodo,
            x=periodo.index,
            y="Capital de trabajo",
            title="Capital de trabajo por año",
            labels={"index": "Año", "Capital de trabajo": MONEDA},
            text_auto=True,
        )
        fig_capital_trabajo.update_traces(texttemplate="%{y:,.0f}")
        fig_capital_trabajo.update_yaxes(tickformat=",.0f", title=MONEDA)
        st.plotly_chart(fig_capital_trabajo, width="stretch")

    with derecha:
        variacion = periodo[["Total activos", "Total pasivos", "Total patrimonio"]].pct_change() * 100
        variacion = variacion.iloc[1:].copy()
        variacion.index = [f"{actual}" for actual in variacion.index]
        variacion.index.name = "Año"
        fig_variacion = px.bar(
            variacion,
            x=variacion.index,
            y=["Total activos", "Total pasivos", "Total patrimonio"],
            barmode="group",
            title="Variación anual de activos, pasivos y patrimonio",
            labels={"index": "Año", "value": "%", "variable": "Cuenta"},
        )
        fig_variacion.update_layout(legend_title_text="")
        fig_variacion.update_yaxes(ticksuffix="%", title="Variación (%)")
        st.plotly_chart(fig_variacion, width="stretch")

with tab_indicadores:
    st.subheader("Metas e indicadores por estudiante")
    st.caption(
        "Cada integrante tiene un gráfico individual con su KGI y sus 3 KPI. "
        "Los resultados son ficticios y se pueden reemplazar."
    )

    filas_kpi = []
    for indicador in INDICADORES_EQUIPO:
        for kpi in indicador["kpis"]:
            filas_kpi.append(
                {
                    "Estudiante": indicador["estudiante"],
                    "KPI": kpi["nombre"],
                    "Resultado": kpi["resultado"],
                    "Meta": kpi["meta"],
                    "Unidad": kpi["unidad"],
                    "Cumplimiento (%)": cumplimiento(
                        kpi["resultado"], kpi["meta"], kpi["direccion"]
                    ),
                    "Estado": (
                        "Alcanzado"
                        if (
                            kpi["resultado"] <= kpi["meta"]
                            if kpi["direccion"] == "menor"
                            else kpi["resultado"] >= kpi["meta"]
                        )
                        else "Pendiente"
                    ),
                }
            )

    datos_kpi = pd.DataFrame(filas_kpi)
    colores = ["#20a486", "#4c78a8", "#f28e2b", "#af7aa1"]
    columnas = st.columns(2)
    for indice, indicador in enumerate(INDICADORES_EQUIPO):
        columna = columnas[indice % 2]
        with columna:
            resultado_kgi = indicador["resultado_kgi"]
            meta_kgi = indicador["meta_kgi"]
            logrado = (
                resultado_kgi <= meta_kgi
                if indicador["direccion_kgi"] == "menor"
                else resultado_kgi >= meta_kgi
            )
            st.markdown(f"### {indicador['estudiante']}")
            st.metric(
                f"KGI · {indicador['kgi']}",
                formato_indicador(resultado_kgi, indicador["unidad_kgi"]),
                delta=f"Meta: {formato_indicador(meta_kgi, indicador['unidad_kgi'])}",
                delta_color="normal" if logrado else "inverse",
            )

            datos_grafico = [
                {
                    "Indicador": f"KGI · {indicador['kgi']}",
                    "Cumplimiento (%)": cumplimiento(
                        resultado_kgi, meta_kgi, indicador["direccion_kgi"]
                    ),
                    "Resultado": resultado_kgi,
                    "Meta": meta_kgi,
                    "Unidad": indicador["unidad_kgi"],
                    "Estado": "Alcanzado" if logrado else "Pendiente",
                }
            ]
            datos_grafico.extend(
                [
                    {
                        "Indicador": f"KPI · {kpi['nombre']}",
                        "Cumplimiento (%)": cumplimiento(
                            kpi["resultado"], kpi["meta"], kpi["direccion"]
                        ),
                        "Resultado": kpi["resultado"],
                        "Meta": kpi["meta"],
                        "Unidad": kpi["unidad"],
                        "Estado": (
                            "Alcanzado"
                            if (
                                kpi["resultado"] <= kpi["meta"]
                                if kpi["direccion"] == "menor"
                                else kpi["resultado"] >= kpi["meta"]
                            )
                            else "Pendiente"
                        ),
                    }
                    for kpi in indicador["kpis"]
                ]
            )
            datos_grafico = pd.DataFrame(datos_grafico)
            avance = datos_grafico["Cumplimiento (%)"].tolist()
            etiquetas = datos_grafico["Indicador"].tolist()
            color = colores[indice]
            titulo = f"KGI y 3 KPI · {indicador['estudiante']}"
            limite = max(120, max(avance) + 10)

            if indicador["tipo_grafico"] == "radar":
                etiquetas = [
                    "KGI · Ventas",
                    "KPI · Clientes",
                    "KPI · Ticket",
                    "KPI · Conversión",
                ]
                fig_indicador = go.Figure(
                    go.Scatterpolar(
                        r=avance,
                        theta=etiquetas,
                        fill="toself",
                        line={"color": color},
                        name="Cumplimiento",
                        customdata=datos_grafico[
                            ["Resultado", "Meta", "Unidad", "Estado"]
                        ].values,
                        hovertemplate=(
                            "%{theta}<br>Cumplimiento: %{r:.1f}%"
                            "<br>Resultado: %{customdata[0]} %{customdata[2]}"
                            "<br>Meta: %{customdata[1]} %{customdata[2]}"
                            "<br>%{customdata[3]}<extra></extra>"
                        ),
                    )
                )
                fig_indicador.update_layout(
                    title=titulo,
                    polar={"radialaxis": {"visible": True, "range": [0, limite]}},
                    showlegend=False,
                )
            elif indicador["tipo_grafico"] == "barras":
                fig_indicador = px.bar(
                    datos_grafico,
                    x="Cumplimiento (%)",
                    y="Indicador",
                    orientation="h",
                    text="Cumplimiento (%)",
                    hover_data=["Resultado", "Meta", "Unidad", "Estado"],
                    title=titulo,
                    range_x=[0, limite],
                    color_discrete_sequence=[color],
                )
                fig_indicador.add_vline(
                    x=100, line_dash="dash", annotation_text="Meta"
                )
                fig_indicador.update_traces(
                    texttemplate="%{x:.1f}%",
                    textposition="outside",
                    cliponaxis=False,
                )
                fig_indicador.update_layout(
                    showlegend=False,
                    xaxis_title="Cumplimiento de la meta (%)",
                    yaxis_title="",
                )
            elif indicador["tipo_grafico"] == "medidores":
                fig_indicador = make_subplots(
                    rows=2,
                    cols=2,
                    specs=[
                        [{"type": "indicator"}, {"type": "indicator"}],
                        [{"type": "indicator"}, {"type": "indicator"}],
                    ],
                    vertical_spacing=0.2,
                )
                for posicion, fila in datos_grafico.iterrows():
                    fig_indicador.add_trace(
                        go.Indicator(
                            mode="gauge+number",
                            value=fila["Cumplimiento (%)"],
                            number={"suffix": "%", "valueformat": ".1f"},
                            title={
                                "text": fila["Indicador"],
                                "font": {"size": 11},
                            },
                            gauge={
                                "axis": {"range": [0, limite]},
                                "bar": {"color": color},
                                "threshold": {
                                    "line": {"color": "#e45756", "width": 3},
                                    "thickness": 0.8,
                                    "value": 100,
                                },
                            },
                        ),
                        row=posicion // 2 + 1,
                        col=posicion % 2 + 1,
                    )
                fig_indicador.update_layout(
                    title=titulo,
                    height=520,
                    margin={"l": 20, "r": 20, "t": 75, "b": 20},
                )
            else:
                etiquetas = [
                    "KGI · Cobro a tiempo",
                    "KPI · Seguimiento",
                    "KPI · Cuentas vencidas",
                    "KPI · Días de cobro",
                ]
                fig_indicador = go.Figure(
                    go.Scatter(
                        x=etiquetas,
                        y=avance,
                        mode="lines+markers+text",
                        text=[f"{valor:.1f}%" for valor in avance],
                        textposition="top center",
                        line={"color": color, "width": 3},
                        marker={"size": 10},
                        customdata=datos_grafico[
                            ["Resultado", "Meta", "Unidad", "Estado"]
                        ].values,
                        hovertemplate=(
                            "%{x}<br>Cumplimiento: %{y:.1f}%"
                            "<br>Resultado: %{customdata[0]} %{customdata[2]}"
                            "<br>Meta: %{customdata[1]} %{customdata[2]}"
                            "<br>%{customdata[3]}<extra></extra>"
                        ),
                    )
                )
                fig_indicador.add_hline(
                    y=100, line_dash="dash", annotation_text="Meta"
                )
                fig_indicador.update_layout(
                    title=titulo,
                    yaxis={"title": "Cumplimiento de la meta (%)", "range": [0, limite]},
                    xaxis_title="",
                )

            fig_indicador.update_layout(
                margin={"l": 10, "r": 20, "t": 65, "b": 20},
            )
            st.plotly_chart(fig_indicador, width="stretch")

    with st.expander("Ver tabla detallada de los 12 KPI"):
        st.dataframe(
            datos_kpi[
                ["Estudiante", "KPI", "Resultado", "Meta", "Unidad", "Cumplimiento (%)", "Estado"]
            ],
            hide_index=True,
            width="stretch",
            column_config={
                "Resultado": st.column_config.NumberColumn(format="%.1f"),
                "Meta": st.column_config.NumberColumn(format="%.1f"),
                "Cumplimiento (%)": st.column_config.NumberColumn(format="%.1f%%"),
            },
        )

with tab_estado:
    st.subheader(f"Estado de situación financiera al 31 de diciembre de {anio}")
    st.caption("Importes expresados en soles (S/).")

    estado = pd.DataFrame(
        [
            ("ACTIVOS", None),
            ("Activos corrientes", None),
            *[(f"  {cuenta}", datos_anio[cuenta]) for cuenta in GRUPOS["Activos corrientes"]],
            ("Total activos corrientes", datos_anio["Total activos corrientes"]),
            ("Activos no corrientes", None),
            *[(f"  {cuenta}", datos_anio[cuenta]) for cuenta in GRUPOS["Activos no corrientes"]],
            ("Total activos no corrientes", datos_anio["Total activos no corrientes"]),
            ("TOTAL ACTIVOS", datos_anio["Total activos"]),
            ("PASIVOS", None),
            ("Pasivos corrientes", None),
            *[(f"  {cuenta}", datos_anio[cuenta]) for cuenta in GRUPOS["Pasivos corrientes"]],
            ("Total pasivos corrientes", datos_anio["Total pasivos corrientes"]),
            ("Pasivos no corrientes", None),
            *[(f"  {cuenta}", datos_anio[cuenta]) for cuenta in GRUPOS["Pasivos no corrientes"]],
            ("Total pasivos no corrientes", datos_anio["Total pasivos no corrientes"]),
            ("TOTAL PASIVOS", datos_anio["Total pasivos"]),
            ("PATRIMONIO", None),
            *[(cuenta, datos_anio[cuenta]) for cuenta in GRUPOS["Patrimonio"]],
            ("TOTAL PATRIMONIO", datos_anio["Total patrimonio"]),
            ("TOTAL PASIVOS Y PATRIMONIO", datos_anio["Total pasivos"] + datos_anio["Total patrimonio"]),
        ],
        columns=["Cuenta", MONEDA],
    )
    st.dataframe(
        estado,
        hide_index=True,
        width="stretch",
        column_config={MONEDA: st.column_config.NumberColumn(format="%,.0f")},
    )
    st.success("Comprobación contable: total activos = total pasivos + total patrimonio.")

with tab_datos:
    st.subheader("Datos comparativos")
    st.caption("Importes ficticios de cierre anual, expresados en soles (S/).")
    st.dataframe(
        df,
        width="stretch",
        column_config={
            cuenta: st.column_config.NumberColumn(format="%,.0f")
            for cuenta in df.columns
        },
    )
    csv = df.to_csv(index=True).encode("utf-8-sig")
    st.download_button(
        "Descargar datos en CSV",
        data=csv,
        file_name="estado_financiero_2021_2025.csv",
        mime="text/csv",
    )
