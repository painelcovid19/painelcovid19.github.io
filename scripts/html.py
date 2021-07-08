import geopandas as gpd
import pandas as pd
from dominate import document
from dominate.tags import div, h1, h6, html, link, meta, script
from dominate.util import raw
from plotly import express as px

df_cidades_campi = pd.read_csv(
    'https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_cidades_campi.csv')

df_mapas = pd.read_csv(
    'https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_acumulados.csv')

df_cidades_campi['MovingMean14'] = df_cidades_campi['new_confirmed'].rolling(14).mean()
df_cidades_campi['MovingMeanObitos14'] = df_cidades_campi['last_available_deaths'].rolling(14).mean()

df_redencao = df_cidades_campi.loc[(df_cidades_campi['city_ibge_code'] == 2311603)]
df_sfc = df_cidades_campi.loc[(df_cidades_campi['city_ibge_code'] == 2929206)]
df_acarape = df_cidades_campi.loc[(df_cidades_campi['city_ibge_code'] == 2300150)]

# Casos Confirmados de Acarape e a Media Movel
trace1 = px.line(x = df_acarape["date"],
                 y = df_acarape["MovingMean14"],
                 height=400,
                 width=650,)
trace1.update_layout(
    title='Media Movel De Acarape',
    yaxis={'title': 'Media Movel'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace2 = px.bar(x = df_acarape['date'],
                y = df_acarape['new_confirmed'],
                height=400,
                width=650,
                )
trace2.update_layout(
    title='Casos Confirmados De Acarape',
    yaxis={'title': 'Casos Confrimados'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace1.add_trace(trace2.data[0])
# data = [trace1, trace2]

# Obitos de Acarape e a Media Movel

trace3 = px.line(x = df_acarape["date"],
                 y = df_acarape["MovingMeanObitos14"],
                 height=400,
                 width=650,)
trace3.update_layout(
    title='Media Movel De Acarape',
    yaxis={'title': 'Media Movel Dos Obitos'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace4 = px.bar(x = df_redencao['date'],
                y = df_redencao['last_available_deaths'],
                height=400,
                width=650,
                )
trace4.update_layout(
    title='Óbitos De Redenção',
    yaxis={'title': 'Óbitos'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace3.add_trace(trace4.data[0])
# data = [trace3, trace4]

# Casos Confirmados de Redenção e a Media Movel

trace5 = px.line(x = df_redencao["date"],
                 y = df_redencao["MovingMean14"],
                 height=400,
                 width=650,)
trace5.update_layout(
    title='Media Movel De Redenção',
    yaxis={'title': 'Media Movel'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace6 = px.bar(x = df_redencao['date'],
                y = df_redencao['new_confirmed'],
                height=400,
                width=650,
                )
trace6.update_layout(
    title='Casos Confirmados De Redenção',
    yaxis={'title': 'Casos Confrimados'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace5.add_trace(trace6.data[0])
# data = [trace5, trace6]

# Obitos de Redenção e Media Movel

trace7 = px.line(x = df_redencao["date"],
                 y = df_redencao["MovingMeanObitos14"],
                 height=400,
                 width=650,)
trace7.update_layout(
    title='Media Movel De Redenção',
    yaxis={'title': 'Media Movel'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace8 = px.bar(x = df_redencao['date'],
                y = df_redencao['last_available_deaths'],
                height=400,
                width=650,
                )
trace8.update_layout(
    title='Casos Confirmados Redenção',
    yaxis={'title': 'Casos Confrimados'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace7.add_trace(trace8.data[0])
# data = [trace7, trace8]

# Casos Confirmados de São Francisco de Conde e a Media Movel

trace9 = px.line(x = df_sfc["date"],
                 y = df_sfc["MovingMean14"],
                 height=400,
                 width=650,)
trace9.update_layout(
    title='Media Movel De São Francisco do Conde',
    yaxis={'title': 'Media Movel'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace10 = px.bar(x = df_sfc['date'],
                y = df_sfc['new_confirmed'],
                height=400,
                width=650,
                )
trace10.update_layout(
    title='Casos Confirmados De São Francisco de Conde',
    yaxis={'title': 'Casos Confirmados'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace9.add_trace(trace10.data[0])
# data = [trace9, trace10]

# Obitos de São Francsico de Conde e Media Movel

trace11 = px.line(x = df_sfc["date"],
                 y = df_sfc["MovingMeanObitos14"],
                 height=400,
                 width=650,)
trace11.update_layout(
    title='Media Movel De São Francisco do Conde',
    yaxis={'title': 'Media Movel'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace12 = px.bar(x = df_sfc['date'],
                y = df_sfc['last_available_deaths'],
                height=400,
                width=650,
                )
trace12.update_layout(
    title='Casos Confirmados De São Francisco de Conde',
    yaxis={'title': 'Casos Confrimados'},
    xaxis={'title': ''},
    template="plotly_white",
)
trace11.add_trace(trace12.data[0])
# data = [trace11, trace12]

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
"""
ceara = df_mapas.loc[0:10, ['city_ibge_code', 'city', 'last_available_confirmed', 'last_available_deaths',
                            'last_available_confirmed_per_100k_inhabitants',
                            'last_available_deaths_per_100k_inhabitants']]
municipios_CE = gpd.read_file('./shapefiles/CE_Municipios_2020.shp')
campi_CE = municipios_CE.merge(ceara, left_on='NM_MUN', right_on='city', suffixes=('', '_y')).set_index("city")

mapa_confirmados_ce = px.choropleth_mapbox(campi_CE,
                                           geojson=campi_CE.geometry,
                                           locations=campi_CE.index,
                                           color="last_available_confirmed_per_100k_inhabitants",
                                           center={"lat": -4.4118, "lon": -38.7491},
                                           opacity=0.7,
                                           mapbox_style="carto-positron",
                                           title="Casos confirmados no Maci�o de Baturit�",
                                           color_continuous_scale=px.colors.sequential.PuBuGn,
                                           zoom=7.75,
                                           height=400,
                                           width=650
                                           )
# mapa_confirmados_ce.update_layout(margin={"r":250,"t":50,"l":250,"b":50})

mapa_obitos_ce = px.choropleth_mapbox(campi_CE,
                                      geojson=campi_CE.geometry,
                                      locations=campi_CE.index,
                                      color="last_available_deaths_per_100k_inhabitants",
                                      center={"lat": -4.4118, "lon": -38.7491},
                                      opacity=0.7,
                                      mapbox_style="carto-positron",
                                      title="Óbitos no Maciço de Baturité",
                                      color_continuous_scale=px.colors.sequential.Reds,
                                      zoom=7.75,
                                      height=400,
                                      width=650)
# mapa_obitos_ce.update_layout(margin={"r": 250, "t": 50, "l": 250, "b": 50})

bahia = df_mapas.loc[11:23, ['city_ibge_code', 'city', 'last_available_confirmed', 'last_available_deaths',
                             'last_available_confirmed_per_100k_inhabitants',
                             'last_available_deaths_per_100k_inhabitants']]
municipios_BA = gpd.read_file('./shapefiles/BA_Municipios_2020.shp')
campi_BA = municipios_BA.merge(bahia, left_on='NM_MUN', right_on='city', suffixes=('', '_y')).set_index("city")

mapa_confirmados_ba = px.choropleth_mapbox(campi_BA,
                                           geojson=campi_BA.geometry,
                                           locations=campi_BA.index,
                                           color="last_available_confirmed_per_100k_inhabitants",
                                           center={"lat": -12.7089, "lon": -38.3354},
                                           opacity=0.7,
                                           mapbox_style="carto-positron",
                                           title="Casos confirmados na regi�o metropolitana de Salvador",
                                           color_continuous_scale=px.colors.sequential.PuBuGn,
                                           zoom=7.75,
                                           height=400,
                                           width=650)
# mapa_confirmados_ba.update_layout(margin={"r": 250, "t": 50, "l": 250, "b": 50})

mapa_obitos_ba = px.choropleth_mapbox(campi_BA,
                                      geojson=campi_BA.geometry,
                                      locations=campi_BA.index,
                                      color="last_available_deaths_per_100k_inhabitants",
                                      center={"lat": -12.7089, "lon": -38.3354},
                                      opacity=0.7,
                                      mapbox_style="carto-positron",
                                      # mapbox_style="stamen-toner",
                                      title="�bitos na regi�o metropolitana de Salvador",
                                      color_continuous_scale=px.colors.sequential.Reds,
                                      zoom=7.75,
                                      height=400,
                                      width=650)


# mapa_obitos_ba.update_layout(margin={"r": 250, "t": 50, "l": 250, "b": 50})


def criar_pagina():
    doc = document(title='Painel Covid')

    with doc.head:
        html(lang="pt-br")
        script(src="https://www.googletagmanager.com/gtag/js?id=G-SNWM62XYE3", _async=True)
        script(
            """window.dataLayer = window.dataLayer || [];
               function gtag(){dataLayer.push(arguments);}
               gtag('js', new Date());
               gtag('config', 'G-SNWM62XYE3');"""
        )
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
                            raw(trace1.to_html(full_html=False, include_plotlyjs='cdn',))
                        with div(cls='col-6'):
                            raw(trace3.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(trace5.to_html(full_html=False, include_plotlyjs=False))
                        with div(cls='col-6'):
                            raw(trace7.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(trace9.to_html(full_html=False, include_plotlyjs=False))
                        with div(cls='col-6 '):
                            raw(trace11.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(mapa_confirmados_ce.to_html(full_html=False, include_plotlyjs=False))
                        with div(cls='col-6'):
                            raw(mapa_obitos_ce.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls='row m-1'):
                        with div(cls='col-6 mr-1'):
                            raw(mapa_confirmados_ba.to_html(full_html=False, include_plotlyjs=False))
                        with div(cls='col-6'):
                            raw(mapa_obitos_ba.to_html(full_html=False, include_plotlyjs=False))

    with open("index.html", "w", newline="", encoding="utf-8") as html_file:
        print(str(doc), file=html_file)


criar_pagina()
