from datetime import datetime, timedelta, timezone
from sys import stdout

import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from dominate import document
from dominate.tags import (
    a,
    button,
    div,
    h1,
    h4,
    h6,
    header,
    html,
    img,
    li,
    link,
    meta,
    nav,
    p,
    script,
    span,
    ul,
)
from dominate.util import raw
from plotly import express as px
from plotly.subplots import make_subplots


if __debug__:
    macro_dados = pd.read_csv("./data/df_dados_macro_regioes_ceara.csv")
    macro_dados_ba = pd.read_csv("./data/df_dados_macro_regioes_bahia.csv")
else:
    macro_dados = pd.read_csv(
        'https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/dadosMacroRegioes/data/df_dados_macro_regioes.csv')
    macro_dados_ba = pd.read_csv(
        'https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_macro_regioes_bahia.csv')

#MODIFICANDO O NOME DAS COLUNAS last_available_confirmed_per_100k_inhabitants E last_available_deaths_per_100k_inhabitants
macro_dados = macro_dados.rename(columns={'last_available_confirmed_per_100k_inhabitants': 'Confirmados por 100 mil habitantes',
                              'last_available_deaths_per_100k_inhabitants': 'Mortes por 100 mil habitantes'})

#IMPORTANDO SHAPEFILES DO CEARÁ E BAHIA
municipios_CE = gpd.read_file('shapefiles/CE_Municipios_2020.shp')
#MESCLANDO SHAPEFILE E DATASET DOS MUNICÍPIOS
macro_mapa_ceara = municipios_CE.merge(macro_dados, left_on='NM_MUN', right_on='city', suffixes=('','_y')).set_index("city")

macro_fig_ce = px.choropleth_mapbox(macro_mapa_ceara,
                           geojson=macro_mapa_ceara.geometry,
                           locations=macro_mapa_ceara.index,
                           color="Confirmados por 100 mil habitantes",
                           center={"lat": -4.1718, "lon": -38.7491},
                           opacity = 0.7,
                           mapbox_style="carto-positron",
                           title = "Casos confirmados por 100 mil habitantes nos municípios vizinhos aos campi da Unilab no Ceará",
                           labels={"Confirmados por 100 mil habitantes": ""},
                           color_continuous_scale=px.colors.sequential.PuBuGn,
                           zoom=7.85,
                           height=600,
                           width=1000
                           )

macro_fig_ce_ob = px.choropleth_mapbox(macro_mapa_ceara,
                           geojson=macro_mapa_ceara.geometry,
                           locations=macro_mapa_ceara.index,
                           color="Mortes por 100 mil habitantes",
                           center={"lat": -4.1718, "lon": -38.7491},
                           opacity = 0.7,
                           mapbox_style="carto-positron",
                           title = "Óbitos confirmados por 100 mil habitantes nos municípios vizinhos aos campi da Unilab no Ceará",
                           labels={"Mortes por 100 mil habitantes": ""},
                           color_continuous_scale=px.colors.sequential.PuBuGn,
                           zoom=7.85,
                           height=600,
                           width=1000
                           )

macro_dados_ba = macro_dados_ba.rename(columns={'last_available_confirmed_per_100k_inhabitants': 'Confirmados por 100 mil habitantes',
                              'last_available_deaths_per_100k_inhabitants': 'Mortes por 100 mil habitantes'})

municipios_BA = gpd.read_file('shapefiles/BA_Municipios_2020.shp')

macro_mapa_bahia = municipios_BA.merge(macro_dados_ba, left_on='NM_MUN', right_on='city', suffixes=('','_y')).set_index("city")

macro_fig_ba = px.choropleth_mapbox(macro_mapa_bahia,
                           geojson=macro_mapa_bahia.geometry,
                           locations=macro_mapa_bahia.index,
                           color="Confirmados por 100 mil habitantes",
                           center={"lat": -12.6089, "lon": -38.654},
                           opacity = 0.7,
                           mapbox_style="carto-positron",
                           title = "Casos confirmados por 100 mil habitantes nos municípios vizinhos ao campus da Unilab na Bahia",
                           labels={"Confirmados por 100 mil habitantes": ""},
                           color_continuous_scale=px.colors.sequential.PuBuGn,
                           zoom=7.85,
                           height=600,
                           width=1000
                           )

macro_fig_ba_ob = px.choropleth_mapbox(macro_mapa_bahia,
                           geojson=macro_mapa_bahia.geometry,
                           locations=macro_mapa_bahia.index,
                           color="Mortes por 100 mil habitantes",
                           center={"lat": -12.6089, "lon": -38.654},
                           opacity = 0.7,
                           mapbox_style="carto-positron",
                           title = "Óbitos confirmados por 100 mil habitantes nos municípios vizinhos ao campus da Unilab na Bahia",
                           labels={"Mortes por 100 mil habitantes": ""},
                           color_continuous_scale=px.colors.sequential.PuBuGn,
                           zoom=7.85,
                           height=600,
                           width=1000
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
        link(rel="stylesheet", href="css/style.css")
        link(
            href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0/dist/css/bootstrap.min.css",
            rel="stylesheet",
            integrity="sha384-wEmeIV1mKuiNpC+IOBjI7aAzPcEZeedi5yW5f2yOq55WWLwNGmvvx4Um1vskeMj0",
            crossorigin="anonymous",
        )
        meta(encodings="utf-8")

    with doc.body:
        with div(cls="spinner"):
            img(src="images/spinner.gif", alt="Loading...")
        with header():
            with nav(cls="navbar navbar-expand-lg fixed-top navbar-light bg-light"):
                with div(cls="container-fluid"):
                    a(
                        h1("PAINEL COVID-19"),
                        cls="navbar-brand",
                        href=r"https://painelcovid19.github.io",
                    )
                    with button(
                            cls="navbar-toggler",
                            type="button",
                            data_bs_toggle="collapse",
                            data_bs_target="#navbarTogglerDemo01",
                            aria_controls="navbarTogglerDemo01",
                            aria_expanded="false",
                            aria_label="Toggle navigation",
                    ):
                        span(cls="navbar-toggler-icon")

                    with div(cls="collapse navbar-collapse", id="navbarTogglerDemo01"):
                        with ul(cls="navbar-nav me-auto"):
                            with li(cls="nav-item active"):
                                a("Mapas das Macro-Regiões", cls="nav-link", href=r"./macro_regioes.html")
                            with li(cls="nav-item active"):
                                a("Sobre o projeto", cls="nav-link", href=r"./sobre.html")
                            with li(cls="nav-item active"):
                                a("Equipe", cls="nav-link", href=r"./equipe.html")

                        with div(cls="ps-3"):
                            with a(target="_blank", href="http://www.unilab.edu.br"):
                                img(
                                    src="./images/logo-unilab.png",
                                    height="30",
                                    cls="d-inline-block align-top",
                                )

                        with div(cls="ps-3"):
                            with a(
                                    target="_blank",
                                    href="http://www.unilab.edu.br/pro-reitoria-de-extensao-arte-e-cultura",
                            ):
                                img(
                                    src="./images/logo-proex.jpg",
                                    height="30",
                                    cls="d-inline-block align-top",
                                )

                        with div(cls="ps-3"):
                            with a(target="_blank", href="http://www.unilab.edu.br/ieds/"):
                                img(
                                    src="./images/logo-ieds.jpg",
                                    height="30",
                                    cls="d-inline-block align-top",
                                )

        with div(cls="container-fluid bg-light"):
            with div(cls="row", style="padding: 90px 15px 0;"):
                with div(cls="col text-primary"):
                    h4("MAPAS DAS MACRO-REGIÕES DOS CAMPI DA UNILAB")
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(
                                macro_fig_ce.to_html(
                                    full_html=False, include_plotlyjs="cdn"
                                )
                            )
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(
                                macro_fig_ce_ob.to_html(
                                    full_html=False, include_plotlyjs=False
                                )
                            )
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(
                                macro_fig_ba.to_html(
                                    full_html=False, include_plotlyjs=False
                                )
                            )
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(
                                macro_fig_ba_ob.to_html(
                                    full_html=False, include_plotlyjs=False
                                )
                            )

                    with div(cls="row"):
                        with div(cls="text-primary"):
                            p("Fontes:")
                            with p("Casos e óbitos: "):
                                a("Brasil.IO", href="https://brasil.io/")
                            with p("Vacinação: "):
                                a(
                                    "Ministério da Saúde",
                                    href="https://dados.gov.br/dataset/covid-19-vacinacao",
                                )
                            with p("Estimativa da população total: "):
                                a("IBGE", href="https://www.ibge.gov.br/cidades-e-estados")

                    with div(cls="row"):
                        with div(cls="text-primary"):
                            p(f"Última atualização: {now.strftime('%d/%m/%Y %H:%M:%S')}")

        script(
            """
            let spinner = document.querySelector('.spinner');

            window.addEventListener('load', function() {
                spinner.style.display = 'none';
            });
        """
        )

        script(src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js",
               integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p",
               crossorigin="anonymous")
        script(src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js",
               integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF",
               crossorigin="anonymous")

    with open("macro_regioes.html", "w", newline="", encoding="utf-8") as html_file:
        print(str(doc), file=html_file)


criar_pagina()
