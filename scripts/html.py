from plotly import express as px
import pandas as pd
import dominate
import geopandas as gpd
from dominate.tags import *
from dominate.util import raw

url = 'https://raw.githubusercontent.com/painel-covid-19/painel-covid-19.github.io/main/data/df_cidades_campi.csv'

df = pd.read_csv(url)

df_redencao = df.loc[(df['city_ibge_code'] == 2311603)]
df_sfc = df.loc[(df['city_ibge_code'] == 2929206)]
df_acarape = df.loc[(df['city_ibge_code'] == 2300150)]

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
    title='Óbitos acumulados De Redenção',
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
    title='Confirmados Diários De Acarape',
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
    title='Óbitos Acumulados De Acarape',
    yaxis={'title': 'Óbitos Diários'},
    xaxis={'title': ''},
    template="plotly_white",
)

sfc = px.line(
    df_sfc,
    x="date",
    y="last_available_confirmed",
    height=400,
    width=650,
).update_layout(
    title='Confirmados Diários De São Francisco do Conde',
    yaxis={'title': 'Casos'},
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
    title='Óbitos Acumulados De São Francisco do Conde',
    yaxis={'title': 'Óbitos Diários'},
    xaxis={'title': ''},
    template="plotly_white",
)

ceara = df.loc[0:10, ['city_ibge_code','city','last_available_confirmed','last_available_deaths']]

municipios_CE = gpd.read_file('./shapefiles/CE_Municipios_2020.shp')

jf = municipios_CE.merge(ceara, left_on='NM_MUN', right_on='city', suffixes=('', '_y')).set_index("city")

mapa_confirmados_ce = px.choropleth_mapbox(jf,
                                           geojson=jf.geometry,
                                           locations=jf.index,
                                           color="last_available_confirmed",
                                           center={"lat": -4.4118, "lon": -38.7491},
                                           opacity=0.7,
                                           mapbox_style="carto-positron",
                                           title="Casos confirmados no Maciço de Baturité",
                                           color_continuous_scale=px.colors.sequential.PuBuGn,
                                           zoom=8.75,
                                           height=400,
                                           width=650)
mapa_confirmados_ce.update_layout(margin={"r": 250, "t": 100, "l": 250, "b": 100})

mapa_obitos_ce = px.choropleth_mapbox(jf,
                                      geojson=jf.geometry,
                                      locations=jf.index,
                                      color="last_available_deaths",
                                      center={"lat": -4.4118, "lon": -38.7491},
                                      opacity=0.7,
                                      mapbox_style="carto-positron",
                                      title="Óbitos no Maciço de Baturité",
                                      color_continuous_scale=px.colors.sequential.Reds,
                                      zoom=8.75,
                                      height=400,
                                      width=650)
mapa_obitos_ce.update_layout(margin={"r": 250, "t": 100, "l": 250, "b": 100})

municipios_BA = gpd.read_file('./shapefiles/BA_Municipios_2020.shp')

bahia = df.loc[11:23,
        ['city_ibge_code', 'last_available_confirmed_per_100k_inhabitants', 'city', 'last_available_confirmed',
         'last_available_deaths']]

jf1 = municipios_BA.merge(bahia, left_on='NM_MUN', right_on='city', suffixes=('', '_y')).set_index("city")

mapa_obitos_ce = px.choropleth_mapbox(jf1,
                                      geojson=jf1.geometry,
                                      locations=jf1.index,
                                      color="last_available_deaths",
                                      center={"lat": -4.4118, "lon": -38.7491},
                                      opacity=0.7,
                                      mapbox_style="carto-posigit addtron",
                                      title="Óbitos no Maciço de Baturité",
                                      color_continuous_scale=px.colors.sequential.Reds,
                                      zoom=8.75,
                                      height=400,
                                      width=650)
mapa_obitos_ce.update_layout(margin={"r": 250, "t": 100, "l": 250, "b": 100})

mapa_obitos_ba = px.choropleth_mapbox(jf1,
                                      geojson=jf1.geometry,
                                      locations=jf1.index,
                                      color="last_available_deaths",
                                      center={"lat": -12.7089, "lon": -38.3354},
                                      opacity=0.7,
                                      mapbox_style="carto-positron",
                                      title="Óbitos na região metropolitana de Salvador",
                                      color_continuous_scale=px.colors.sequential.Reds,
                                      zoom=8.34,
                                      height=400,
                                      width=650)
mapa_obitos_ba.update_layout(margin={"r": 250, "t": 100, "l": 250, "b": 100})


def criar_pagina():
    doc = dominate.document(title='Painel Covid')

    with doc.head:
        link(href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css", rel="stylesheet",
             integrity="sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0",
             crossorigin="anonymous")
        meta(encodings="utf-8")

    with doc.body:
        with div(cls='container-fluid bg-light'):
            with div(cls='row'):
                with div(cls='col'):
                    with div(cls="text-primary text-center"):
                        h1('Painel Covid-19')
                    with div(cls='row m-1 align-items-center align-content-center'):
                        with div(cls='col-2'):
                            with div(cls='card text-primary text-center'):
                                with div(cls='card-header'):
                                    h6('Óbitos De Acarape')
                                with div(cls='card-body'):
                                    div(f"{df_acarape['last_available_deaths'].iloc[1]}")
                        with div(cls='col-2'):
                            with div(cls='card text-primary text-center'):
                                with div(cls='card-header'):
                                    h6('Confirmados De Acarape')
                                with div(cls='card-body'):
                                    div(f"{df_acarape['last_available_confirmed'].iloc[1]}")
                        with div(cls='col-2'):
                            with div(cls='card text-primary text-center'):
                                with div(cls='card-header'):
                                    h6('Óbitos De Redenção')
                                with div(cls='card-body'):
                                    div(f"{df_redencao['last_available_deaths'].iloc[1]}")
                        with div(cls='col-2'):
                            with div(cls='card text-primary text-center'):
                                with div(cls='card-header'):
                                    h6('Confrimados Redenção')
                                with div(cls='card-body'):
                                    div(f"{df_redencao['last_available_confirmed'].iloc[1]}")
                        with div(cls='col-2'):
                            with div(cls='card text-primary text-center'):
                                with div(cls='card-header'):
                                    h6('Óbitos De São Francisco Do Conde')
                                with div(cls='card-body'):
                                    div(f"{df_sfc['last_available_deaths'].iloc[1]}")
                        with div(cls='col-2'):
                            with div(cls='card text-primary text-center'):
                                with div(cls='card-header'):
                                    h6('Confirmados De São Francisco Do Conde')
                                with div(cls='card-body'):
                                    div(f"{df_sfc['last_available_confirmed'].iloc[1]}")

                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(redencao.to_html(full_html=False, include_plotlyjs='cdn'))
                        with div(cls='col-6'):
                            raw(redencao_obitos.to_html(full_html=False, ))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(acarape.to_html(full_html=False, include_plotlyjs='cdn'))
                        with div(cls='col-6'):
                            raw(acarape_obitos.to_html(full_html=False, ))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(sfc.to_html(full_html=False, include_plotlyjs='cdn'))
                        with div(cls='col-6 '):
                            raw(sfc_obitos.to_html(full_html=False, ))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(mapa_confirmados_ce.to_html(full_html=False, ))
                        with div(cls='col-6'):
                            raw(mapa_obitos_ce.to_html(full_html=False, ))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(mapa_confirmados_ce.to_html(full_html=False, ))
                        with div(cls='col-6'):
                            raw(mapa_obitos_ba.to_html(full_html=False, ))
    print(doc)


criar_pagina()
