from datetime import datetime, timezone, timedelta

import geopandas as gpd
import pandas as pd
from dominate import document
from dominate.tags import div, h1, h6, html, link, meta, p, script, nav, ul, a, li, h2, h3, img
from dominate.util import raw
from plotly import express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from six import with_metaclass

df_cidades_campi = pd.read_csv(
    "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_cidades_campi.csv"
)

df_mapas = pd.read_csv(
    "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_acumulados.csv"
)

df_cidades_campi["MovingMeanConfirmed"] = df_cidades_campi["new_confirmed"].rolling(14).mean()
df_cidades_campi["MovingMeanDeaths"] = df_cidades_campi["new_deaths"].rolling(14).mean()

df_redencao = df_cidades_campi.loc[(df_cidades_campi["city_ibge_code"] == 2311603)]
df_sfc = df_cidades_campi.loc[(df_cidades_campi["city_ibge_code"] == 2929206)]
df_acarape = df_cidades_campi.loc[(df_cidades_campi["city_ibge_code"] == 2300150)]

# GRÁFICOS DE VACINADOS

dados_redencao = pd.read_csv('https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/vaccines-redencao-ce.csv')
dados_redencao['vacina_descricao_dose'] = dados_redencao['vacina_descricao_dose'].str.replace('\xa0', '')
dados_acarape = pd.read_csv('https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/vaccines-acarape-ce.csv')
dados_acarape['vacina_descricao_dose'] = dados_acarape['vacina_descricao_dose'].str.replace('\xa0', '')
dados_sfc = pd.read_csv('https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/vaccines-sao-francisco-do-conde-ba.csv')
dados_acarape['vacina_descricao_dose'] = dados_acarape['vacina_descricao_dose'].str.replace('\xa0', '')

vacina_acarape = dados_acarape
vacina_redencao = dados_redencao
vacina_SFC = dados_sfc

dose_1_acarape =vacina_acarape[vacina_acarape['vacina_descricao_dose']=='1ª Dose']
dose_2_acarape =vacina_acarape[vacina_acarape['vacina_descricao_dose']=='2ª Dose']
dose_acarape_unica =vacina_acarape[vacina_acarape['vacina_descricao_dose']=='Dose']

dose_1_redencao =vacina_redencao[vacina_redencao['vacina_descricao_dose']=='1ª Dose']
dose_2_redencao =vacina_redencao[vacina_redencao['vacina_descricao_dose']=='2ª Dose']
dose_redencao_unica =vacina_redencao[vacina_redencao['vacina_descricao_dose'] == 'Dose']

dose_1_sfc =vacina_SFC[vacina_SFC['vacina_descricao_dose']=='1ª Dose']
dose_2_sfc =vacina_SFC[vacina_SFC['vacina_descricao_dose']=='2ª Dose']
dose_sfc =vacina_SFC[vacina_SFC['vacina_descricao_dose'] == 'Dose']

# primeira dose acarape
falta_acarape_1 = 15338 - len(dose_1_acarape.index)
labels_acarape_1 = ['Não vacinados', '1ª Dose']
values_acarape_1 = [falta_acarape_1, len(dose_1_acarape.index)]
# segunda dose acarape
falta_acarape_2 = 15338 - len(dose_2_acarape.index)
labels_acarape_2 = ['Não vacinados', '2ª Dose', 'Única dose']
values_acarape_2 = [falta_acarape_1, len(dose_2_acarape.index), len(dose_acarape_unica.index)]

# primeira dose redençao
falta_redencao_1 = 29146 - len(dose_1_redencao.index)
labels_redencao_1 = ['Não vacinados', '1ª Dose']
values_redencao_1 = [falta_redencao_1, len(dose_1_redencao.index)]
# segunda dose redencao
falta_redencao_2 = 29146 - len(dose_2_redencao.index)
labels_redencao_2 = ['Não vacinados', '2ª Dose', 'Única dose']
values_redencao_2 = [falta_redencao_1, len(dose_2_redencao.index), len(dose_redencao_unica.index)]

# primeira dose SFC
falta_SFC_1 = 40245 - len(dose_1_sfc.index)
labels_SFC_1 = ['Não vacinados', '1ª Dose']
values_SFC_1 = [falta_SFC_1, len(dose_1_sfc.index)]
# segunda dose SFC
falta_SFC_2 = 40245 - len(dose_2_sfc.index)
labels_SFC_2 = ['Não vacinados', '2ª Dose', 'Única dose']
values_SFC_2 = [falta_SFC_2, len(dose_2_sfc.index), len(dose_sfc.index)]
c = ['#dee1e3', '#0793f0']

acarape_vac = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
acarape_vac.add_trace(
    go.Pie(labels=labels_acarape_1, values=values_acarape_1, marker_colors=['#f2f7f7', '#7FFFD4'], name=" "),
    1, 1)
acarape_vac.add_trace(
    go.Pie(labels=labels_acarape_2, values=values_acarape_2, marker_colors=['#f2f7f7', '#00FA9A', '#40E0D0'], name=" "),
    1, 2)

# Use `hole` to create a donut-like pie chart
acarape_vac.update_traces(hole=.7, hoverinfo="label+percent+name")

acarape_vac.update_layout(showlegend=False, height=350, width=500,
                          title_text="Vacinados em Acarape",
                          # Add annotations in the center of the donut pies.
                          annotations=[dict(text='1ª dose', x=0.125, y=0.5, font_size=20, showarrow=False),
                                       dict(text='2ª dose e única', x=0.935, y=0.5, font_size=20, showarrow=False)])

# Create subplots: use 'domain' type for Pie subplot
redencao_vac = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
redencao_vac.add_trace(
    go.Pie(labels=labels_redencao_1, values=values_redencao_1, marker_colors=['#f2f7f7', '#7FFFD4'], name=" "),
    1, 1)
redencao_vac.add_trace(
    go.Pie(labels=labels_redencao_2, values=values_redencao_2, marker_colors=['#f2f7f7', '#00FA9A', '#40E0D0'],
           name=" "),
    1, 2)

# Use `hole` to create a donut-like pie chart
redencao_vac.update_traces(hole=.7, hoverinfo="label+percent+name")

redencao_vac.update_layout(showlegend=False, height=350, width=500,
                           title_text="Vacinados em Redenção",
                           # Add annotations in the center of the donut pies.
                           annotations=[dict(text='1ª dose', x=0.125, y=0.5, font_size=20, showarrow=False),
                                        dict(text='2ª dose e única', x=0.935, y=0.5, font_size=20, showarrow=False)])

# Create subplots: use 'domain' type for Pie subplot
sfc_vac = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]])
sfc_vac.add_trace(go.Pie(labels=labels_SFC_1, values=values_SFC_1, marker_colors=['#f2f7f7', '#7FFFD4'], name=" "),
                  1, 1)
sfc_vac.add_trace(
    go.Pie(labels=labels_SFC_2, values=values_SFC_2, marker_colors=['#f2f7f7', '#00FA9A', '#40E0D0'], name=" "),
    1, 2)

# Use `hole` to create a donut-like pie chart
sfc_vac.update_traces(hole=.7, hoverinfo="label+percent+name")

sfc_vac.update_layout(showlegend=False, height=350, width=500,
                      title_text="Vacinados em São Francisco do Conde",
                      # Add annotations in the center of the donut pies.
                      annotations=[dict(text='1ª dose', x=0.125, y=0.5, font_size=20, showarrow=False),
                                   dict(text='2ª dose e única', x=0.935, y=0.5, font_size=20, showarrow=False)])

# TESTE
vacinas = make_subplots(rows=2, cols=3,
                        specs=[[{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}],
                               [{'type': 'domain'}, {'type': 'domain'}, {'type': 'domain'}]])

# ACARAPE
vacinas.add_trace(go.Pie(labels=labels_acarape_1, values=values_acarape_1,
                         marker_colors=['#f2f7f7', '#7FFFD4'], name=" ", ), 1, 1)

vacinas.add_trace(go.Pie(labels=labels_acarape_2, values=values_acarape_2,
                         marker_colors=['#f2f7f7', '#00FA9A', '#40E0D0'], name=" "), 2, 1)

# REDENÇÃO
vacinas.add_trace(go.Pie(labels=labels_redencao_1, values=values_redencao_1,
                         marker_colors=['#f2f7f7', '#7FFFD4'], name=" ", ), 1, 2)

vacinas.add_trace(go.Pie(labels=labels_redencao_2, values=values_redencao_2,
                         marker_colors=['#f2f7f7', '#00FA9A', '#40E0D0'], name=" "), 2, 2)

# SFC
vacinas.add_trace(go.Pie(labels=labels_SFC_1, values=values_SFC_1,
                         marker_colors=['#f2f7f7', '#7FFFD4'], name=" "), 1, 3)

vacinas.add_trace(go.Pie(labels=labels_SFC_2, values=values_SFC_2,
                         marker_colors=['#f2f7f7', '#00FA9A', '#40E0D0'], name=" "), 2, 3)

# Use `hole` to create a donut-like pie chart
vacinas.update_traces(hole=.7, hoverinfo="label+percent+name")
vacinas.update_layout(height=800,
                      width=1000, legend=dict(orientation="h", yanchor="bottom", y=-.09, xanchor="right", x=.75),
                      title_text=" ",
                      # Add annotations in the center of the donut pies.
                      annotations=[dict(text='1ª dose', x=0.11, y=.8, font_size=15, showarrow=False),
                                   dict(text='1ª dose', x=0.5, y=.8, font_size=15, showarrow=False),
                                   dict(text='1ª dose', x=0.89, y=.8, font_size=15, showarrow=False),
                                   dict(text='2ª dose e única', x=0.078, y=0.19, font_size=15, showarrow=False),
                                   dict(text='2ª dose e única', x=0.5, y=0.19, font_size=15, showarrow=False),
                                   dict(text='2ª dose e única', x=0.93, y=0.19, font_size=15, showarrow=False),
                                   dict(text='Acarape', x=0.071, y=1.1, font_size=30, showarrow=False),
                                   dict(text='Redenção', x=0.5, y=1.1, font_size=30, showarrow=False),
                                   dict(text='SFC', x=0.88, y=1.1, font_size=30, showarrow=False)])

# Casos Confirmados de Acarape e a Media Movel
trace1 = px.line(df_acarape,
    x="date",
    y="MovingMeanConfirmed",
    color_discrete_sequence=["orange"],
    height=400,
    width=650,
)
trace1.update_layout(
    title="Casos Confirmados e a Media Movel em Acarape",
    yaxis={"title": "Casos Confrimados e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace2 = px.bar(df_acarape,
    x="date",
    y="new_confirmed",
    color_discrete_sequence=["darkblue"],
    height=400,
    width=650,
)
trace2.update_layout(
    title="Casos Confirmados em Acarape",
    yaxis={"title": "Casos Confrimados e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace1.add_trace(trace2.data[0])

# Obitos de Acarape e a Media Movel

trace3 = px.line(df_acarape,
    x="date",
    y="MovingMeanDeaths",
    color_discrete_sequence=["orange"],
    height=400,
    width=650,
)
trace3.update_layout(
    title="Óbitos e Media Movel em Acarape",
    template="plotly_white",
    yaxis={"title": "Óbitos e Media Movel"},
    xaxis={"title": ""},
)
trace4 = px.bar(df_acarape,
    x="date",
    y="new_deaths",
    color_discrete_sequence=["darkblue"],
    height=400,
    width=650,
)
trace4.update_layout(
    title="Óbitos e Media Movel em Acarape",
    template="plotly_white",
    yaxis={"title": "Óbitos e Media Movel"},
    xaxis={"title": ""},
)
trace3.add_trace(trace4.data[0])

# Casos Confirmados de Redenção e a Media Movel

trace5 = px.line(df_redencao,
    x="date",
    y="MovingMeanConfirmed",
    color_discrete_sequence=["orange"],
    height=400,
    width=650,
)
trace5.update_layout(
    title="Media Movel em Redenção",
    template="plotly_white",
    yaxis={"title": "Casos Confrimados e Media Movel"},
    xaxis={"title": ""},
)
trace6 = px.bar(df_redencao,
    x="date",
    y="new_confirmed",
    color_discrete_sequence=["darkblue"],
    height=400,
    width=650,
)
trace6.update_layout(
    title="Casos Confrimados Media Movel em Redenção",
    yaxis={"title": "Casos Confrimados e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace5.add_trace(trace6.data[0])

# Obitos de Redenção e Media Movel

trace7 = px.line(df_redencao,
    x="date",
    y="MovingMeanDeaths",
    color_discrete_sequence=["orange"],
    height=400,
    width=650,
)
trace7.update_layout(
    title="Óbitos e Media Movel em Redenção",
    template="plotly_white",
    yaxis={"title": "Óbitos e Media Movel"},
    xaxis={"title": ""},
)
trace8 = px.bar(df_redencao,
    x="date",
    y="new_deaths",
    color_discrete_sequence=["darkblue"],
    height=400,
    width=650,
)
trace8.update_layout(
    title="Óbitos e Media Movel em Redenção",
    yaxis={"title": "Óbitos e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace7.add_trace(trace8.data[0])

# Casos Confirmados de São Francisco de Conde e a Media Movel

trace9 = px.line(df_sfc,
    x="date",
    y="MovingMeanConfirmed",
    color_discrete_sequence=["orange"],
    height=400,
    width=650,
)
trace9.update_layout(
    title="Casos Confrimados Media Movel em São Francisco do Conde",
    yaxis={"title": "Casos Confirmados e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace10 = px.bar(df_sfc,
    x="date",
    y="new_confirmed",
    color_discrete_sequence=["darkblue"],
    height=400,
    width=650,
)
trace10.update_layout(
    title="Casos Confrimados e Media Movel em São Francisco de Conde",
    yaxis={"title": "Casos Confirmados e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace9.add_trace(trace10.data[0])

# Obitos de São Francsico de Conde e Media Movel

trace11 = px.line(df_sfc,
    x="date",
    y="MovingMeanDeaths",
    color_discrete_sequence=["orange"],
    height=400,
    width=650,
)
trace11.update_layout(
    title="Óbitos e Media Movel em São Francisco do Conde",
    yaxis={"title": "Óbitos e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace12 = px.bar(df_sfc,
    x="date",
    y="new_deaths",
    color_discrete_sequence=["darkblue"],
    height=400,
    width=650,
)
trace12.update_layout(
    title="Óbitos e Media Movel em São Francisco de Conde",
    yaxis={"title": "Óbitos e Media Movel"},
    xaxis={"title": ""},
    template="plotly_white",
)
trace11.add_trace(trace12.data[0])
"""
redencao = px.line(
    df_redencao,
    x="date",
    y="last_available_confirmed",
    height=400,
    width=650,
).update_layout(
    title='Confirmados Diários de Redenção',
    yaxis={'title': 'Casos Confirmados'},
    xaxis={'title': ''},
    template="plotly_white",
)

redencao_obitos = px.line(
    df_redencao,
    x="date",
    y="last_available_deaths",
    height=400,
    width=650,
).update_layout(
    title='Óbitos acumulados em Redenção',
    yaxis={'title': 'Óbitos Diários'},
    xaxis={'title': ''},
    template="plotly_white",
)

acarape = px.line(
    df_acarape,
    x="date",
    y="last_available_confirmed",
    height=400,
    width=650,
).update_layout(
    title='Confirmados Diários em Acarape',
    yaxis={'title': 'Casos Confirmados'},
    xaxis={'title': ''},
    template="plotly_white",
)

acarape_obitos = px.line(
    df_acarape,
    x="date",
    y="last_available_deaths",
    height=400,
    width=650,
).update_layout(
    title='Óbitos Acumulados em Acarape',
    yaxis={'title': 'Óbitos Diários'},
    xaxis={'title': ''},
    template="plotly_white",
)


sfc_obitos = px.line(
    df_sfc,
    x="date",
    y="last_available_deaths",
    height=400,
    width=650,
).update_layout(
    title='Óbitos Acumulados em São Francisco do Conde',
    yaxis={'title': 'Óbitos Diários'},
    xaxis={'title': ''},
    template="plotly_white",
)
"""

ceara = df_mapas[df_mapas["state"] == "CE"]
municipios_CE = gpd.read_file("shapefiles/CE_Municipios_2020.shp")
campi_CE = municipios_CE.merge(
    ceara, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
).set_index("city")

mapa_confirmados_ce = px.choropleth_mapbox(
    campi_CE,
    geojson=campi_CE.geometry,
    locations=campi_CE.index,
    color="last_available_confirmed_per_100k_inhabitants",
    labels={"last_available_confirmed_per_100k_inhabitants": ""},
    center={"lat": -4.4118, "lon": -38.7491},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Casos confirmados no Maciço de Baturité (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.75,
    height=400,
    width=650,
)

mapa_obitos_ce = px.choropleth_mapbox(
    campi_CE,
    geojson=campi_CE.geometry,
    locations=campi_CE.index,
    color="last_available_deaths_per_100k_inhabitants",
    labels={"last_available_deaths_per_100k_inhabitants": ""},
    center={"lat": -4.4118, "lon": -38.7491},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Óbitos no Maciço de Baturité (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.Reds,
    zoom=7.75,
    height=400,
    width=650,
)

bahia = df_mapas[df_mapas["state"] == "BA"]
municipios_BA = gpd.read_file("shapefiles/BA_Municipios_2020.shp")
campi_BA = municipios_BA.merge(
    bahia, left_on="NM_MUN", right_on="city", suffixes=("", "_y")
).set_index("city")

mapa_confirmados_ba = px.choropleth_mapbox(
    campi_BA,
    geojson=campi_BA.geometry,
    locations=campi_BA.index,
    color="last_available_confirmed_per_100k_inhabitants",
    labels={"last_available_confirmed_per_100k_inhabitants": ""},
    center={"lat": -12.7089, "lon": -38.3354},
    opacity=0.7,
    mapbox_style="carto-positron",
    title="Casos confirmados na Região Metropolitana <br>de Salvador (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.PuBuGn,
    zoom=7.75,
    height=400,
    width=650,
)

mapa_obitos_ba = px.choropleth_mapbox(
    campi_BA,
    geojson=campi_BA.geometry,
    locations=campi_BA.index,
    color="last_available_deaths_per_100k_inhabitants",
    labels={"last_available_deaths_per_100k_inhabitants": ""},
    center={"lat": -12.7089, "lon": -38.3354},
    opacity=0.7,
    mapbox_style="carto-positron",
    # mapbox_style="stamen-toner",
    title="Óbitos na Região Metropolitana <br>de Salvador (por 100 mil hab.)",
    color_continuous_scale=px.colors.sequential.Reds,
    zoom=7.75,
    height=400,
    width=650,
)


def criar_pagina():
    now = datetime.now(timezone(timedelta(hours=-3)))

    doc = document(title="Painel Covid")

    with doc.head:
        html(lang="pt-br")
        script(src="https://www.googletagmanager.com/gtag/js?id=G-SNWM62XYE3", _async=True)
        script(
            """window.dataLayer = window.dataLayer || [];
               function gtag(){dataLayer.push(arguments);}
               gtag('js', new Date());
               gtag('config', 'G-SNWM62XYE3');"""
        )
        link(
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css",
            rel="stylesheet",
            integrity="sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0",
            crossorigin="anonymous",
        )
        meta(encodings="utf-8")

    with doc.body:
        with div(cls="container-fluid bg-light"):
            with nav(cls="navbar navbar-expand-lg navbar-light"):
                    with div(cls="container-fluid"):
                        a("PAINEL COVID-19", href="index.html", cls="navbar-brand text-primary")
                        with ul(cls="navbar-nav justify-content-start"):
                            with li(cls="nav-item p-2"):
                                a("EQUIPE", href="equipe.html", style="text-decoration: none;")
                            with li(cls="nav-item p-2"):
                                a("SOBRE O PROJETO", href="sobreNos.html", style="text-decoration: none;")
                            with li(cls="nav-item p-2"):
                                a(img(src="imagens/proex.jpg", width="25%"), href="https://unilab.edu.br/editais-proex/")

            with div(cls="row"):
                with div(cls="col"):
                    with div(cls="row row-cols-1 row-cols-md-3 g-4"):
                        with div(cls="col"):
                            with div(cls="card text-primary text-center"):
                                with div(cls="card-header"):
                                    h6("Confirmados em Acarape")
                                with div(cls="card-body"):
                                    div(f"{df_acarape['last_available_confirmed'].iloc[1]}")
                        with div(cls="col"):
                            with div(cls="card text-primary text-center"):
                                with div(cls="card-header"):
                                    h6("Confirmados em Redenção")
                                with div(cls="card-body"):
                                    div(f"{df_redencao['last_available_confirmed'].iloc[1]}")
                        with div(cls="col"):
                            with div(cls="card text-primary text-center"):
                                with div(cls="card-header"):
                                    h6("Confirmados em São Francisco Do Conde")
                                with div(cls="card-body"):
                                    div(f"{df_sfc['last_available_confirmed'].iloc[1]}")
                        with div(cls="col"):
                            with div(cls="card text-primary text-center"):
                                with div(cls="card-header"):
                                    h6("Óbitos em Acarape")
                                with div(cls="card-body"):
                                    div(f"{df_acarape['last_available_deaths'].iloc[1]}")
                        with div(cls="col"):
                            with div(cls="card text-primary text-center"):
                                with div(cls="card-header"):
                                    h6("Óbitos em Redenção ")
                                with div(cls="card-body"):
                                    div(f"{df_redencao['last_available_deaths'].iloc[1]}")
                        with div(cls="col"):
                            with div(cls="card text-primary text-center"):
                                with div(cls="card-header"):
                                    h6("Óbitos em São Francisco Do Conde")
                                with div(cls="card-body"):
                                    div(f"{df_sfc['last_available_deaths'].iloc[1]}")

                    with div(cls="row my-5"):
                        with div(cls="col"):
                            with div(cls="row m-1"):
                                with div(cls="col text-primary"):
                                    h3("GRAFICOS DOS VACINADOS")
                            with div(cls="container"):
                                with div(cls='row'):
                                    with div(cls='col-sm'):
                                        raw(vacinas.to_html(full_html=False, include_plotlyjs="cdn", ))
                                    # with div(cls='col-sm'):
                                    # raw(redencao_vac.to_html(full_html=False,include_plotlyjs="cdn",))
                                    # with div(cls='col-sm'):
                                    # raw(sfc_vac.to_html(full_html=False,include_plotlyjs="cdn",))

                    with div(cls="row my-5"):
                        with div(cls="col"):
                            with div(cls="row m-1"):
                                with div(cls="col text-primary"):
                                    h3("GRAFICOS DOS CASOS TOTAIS E OBITOS")
                            with div(cls="row m-1"):
                                with div(cls="col-6 mr-1"):
                                    raw(
                                        trace1.to_html(
                                            full_html=False,
                                            include_plotlyjs="cdn",
                                        )
                                    )
                                with div(cls="col-6"):
                                    raw(trace3.to_html(full_html=False, include_plotlyjs=False))
                            with div(cls="row m-1"):
                                with div(cls="col-6 mr-1"):
                                    raw(trace5.to_html(full_html=False, include_plotlyjs=False))
                                with div(cls="col-6"):
                                    raw(trace7.to_html(full_html=False, include_plotlyjs=False))
                            with div(cls="row m-1"):
                                with div(cls="col-6 mr-1"):
                                    raw(trace9.to_html(full_html=False, include_plotlyjs=False))
                                with div(cls="col-6 "):
                                    raw(trace11.to_html(full_html=False, include_plotlyjs=False))

                    with div(cls="row my-5"):
                        with div(cls="col"):
                            with div(cls="row m-1"):
                                with div(cls="col text-primary"):
                                    h3("MAPAS DAS REGIÕES SEDE DOS CAMPI DA UNILAB")
                            with div(cls="row m-1"):
                                with div(cls="col-6 mr-1"):
                                    raw(
                                        mapa_confirmados_ce.to_html(
                                            full_html=False, include_plotlyjs=False
                                        )
                                    )
                                with div(cls="col-6"):
                                    raw(mapa_obitos_ce.to_html(full_html=False, include_plotlyjs=False))
                            with div(cls="row m-1"):
                                with div(cls="col-6 mr-1"):
                                    raw(
                                        mapa_confirmados_ba.to_html(
                                            full_html=False, include_plotlyjs=False
                                        )
                                    )
                                with div(cls="col-6"):
                                    raw(mapa_obitos_ba.to_html(full_html=False, include_plotlyjs=False))

                    with div(cls="row m-1"):
                        with div(cls="text-primary text-center"):
                            p(f"Última atualização: {now.strftime('%d/%m/%Y %H:%M:%S')}")

    with open("index.html", "w", newline="", encoding="utf-8") as html_file:
        print(str(doc), file=html_file)


criar_pagina()
