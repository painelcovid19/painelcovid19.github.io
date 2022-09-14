from datetime import datetime, timedelta, timezone
from sys import stdout
from calculate_rt import  Calculate_Rt
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


# if __debug__:
#     dados_campis = pd.read_csv("./data/dados_campis.csv", parse_dates=["date"])
# else:
#     dados_campis = pd.read_csv(
#         "https://raw.githubusercontent.com/painelcovid19/painelcovid19.github.io/main/data/df_dados_macro_regioes_ceara.csv"
#     )

dados_campis = pd.read_csv("./data/df_cidades_rt.csv", parse_dates=["date"])


df_redencao = dados_campis[dados_campis["city"] == "Redenção"]
df_acarape = dados_campis[dados_campis["city"] == "Acarape"]
df_SFC = dados_campis[dados_campis["city"] == "São Francisco do Conde"]
df_Fortaleza = dados_campis[dados_campis["city"] == "Fortaleza"]
df_Salvador = dados_campis[dados_campis["city"] == "Salvador"]


# criando os graficos 
rt = Calculate_Rt()

df_reformated_acarape = rt.ajust_numbers(df_acarape)
df_reformated_redencao = rt.ajust_numbers(df_redencao)
df_reformated_SFC = rt.ajust_numbers(df_SFC)
df_reformated_Fortaleza = rt.ajust_numbers(df_Fortaleza)
df_reformated_Salvador = rt.ajust_numbers(df_Salvador)


figure_acarape = rt.estimate_plotly(df_reformated_acarape, city_name="Acarape")
figure_SFC = rt.estimate_plotly(df_reformated_SFC, city_name="São Francisco do Conde")
figure_redencao = rt.estimate_plotly(df_reformated_redencao, city_name="Redenção")
figure_Fortaleza = rt.estimate_plotly(df_reformated_Fortaleza, city_name="Fortaleza")
figure_Salvador = rt.estimate_plotly(df_reformated_Salvador, city_name="Salvador")


# criando o html da página
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
                                a(
                                    "Mapas das Macro-Regiões",
                                    cls="nav-link",
                                    href=r"./macro_regioes.html",
                                )
                            with li(cls="nav-item active"):
                                a("Sobre o projeto", cls="nav-link", href=r"./sobre.html")
                            with li(cls="nav-item active"):
                                a("Equipe", cls="nav-link", href=r"./equipe.html")
                            with li(cls="nav-item active"):
                                a("Estimativa R(t)", cls="nav-link", href=r"./rt.html")

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
                with div(cls="col text-primary justify-content-center"):
                    h4("Indice de Transmisão da covid RT")
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(figure_acarape.to_html(full_html=False, include_plotlyjs="cdn"))
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(figure_redencao.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(figure_SFC.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls="row m-3 justify-content-around"):
                        with div(cls="col d-flex justify-content-center"):
                            raw(figure_Fortaleza.to_html(full_html=False, include_plotlyjs=False))
                    with div(cls="row m-3 justify-content-around"):        
                        with div(cls="col d-flex justify-content-center"):
                            raw(figure_Salvador.to_html(full_html=False, include_plotlyjs=False))

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

        script(
            src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js",
            integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p",
            crossorigin="anonymous",
        )
        script(
            src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js",
            integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF",
            crossorigin="anonymous",
        )

    with open("./rt.html", "w", newline="", encoding="utf-8") as html_file:
        print(str(doc), file=html_file)


criar_pagina()
