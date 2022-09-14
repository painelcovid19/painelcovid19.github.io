import pandas as pd
import matplotlib.pyplot as plt
import epyestim
import epyestim.covid19 as covid19
import plotly.graph_objects as go


class Calculate_Rt:
    
    def ajust_numbers(self, dataframe:pd.core.frame.DataFrame) -> pd.core.series.Series:
        dataframe = dataframe.sort_values(by=["date"], ascending=True)
        df_cases = dataframe[["date", "new_confirmed"]]
        df_cases.columns = ["Date", "Cases"]
        df_cases = df_cases.set_index("Date")["Cases"]
        # rever a questão do tratamento dos cosos negativos
        df_cases = df_cases.apply(lambda case: case * (-1) if case < 0 else case)
        return df_cases

    def estimate(self, dataframe:pd.core.series.Series, city_name:str, ):
        df_time_varying_r = covid19.r_covid(dataframe)
        fig, ax = plt.subplots(1,1, figsize=(12, 5))
        df_time_varying_r.loc[:,'Q0.5'].plot(ax=ax, color='red')
        ax.fill_between(df_time_varying_r.index, 
                            df_time_varying_r['Q0.025'], 
                            df_time_varying_r['Q0.975'], 
                            color='red', alpha=0.2)
        ax.set_xlabel('date')
        ax.set_ylabel('R(t) with 95%-CI')
        ax.set_ylim([0,6])
        ax.axhline(y=1)
        ax.set_title(f'Estimate of time-varying effective reproduction number of {city_name} ')
        plt.show()
    
    def estimate_by_windows(self, dataframe:pd.core.frame.DataFrame,windows:int, city_name:str ):
        df_time_varying_r = covid19.r_covid(dataframe, smoothing_window=windows)
        fig, ax = plt.subplots(1,1, figsize=(12, 5))
        df_time_varying_r.loc[:,'Q0.5'].plot(ax=ax, color='red')
        ax.fill_between(df_time_varying_r.index, 
                            df_time_varying_r['Q0.025'], 
                            df_time_varying_r['Q0.975'], 
                            color='red', alpha=0.2)
        ax.set_xlabel('date')
        ax.set_ylabel('R(t) with 95%-CI')
        ax.set_ylim([0,10])
        ax.axhline(y=1)
        ax.set_title(f'Estimate of time-varying effective reproduction number of {city_name} smoothing windows of 7 days')
        plt.show()

    def estimate_plotly(self, dataframe:pd.core.series.Series, city_name:str ):
        df_time_varying_r = covid19.r_covid(dataframe)

        fig = go.Figure(
            layout=go.Layout(
            title=f"Número de reprodução efetiva R(t) para {city_name}",
            yaxis={"title": "R(t) com 95%-CI"},
            xaxis={"title": "data"},
            template="plotly_white",
            legend=dict(
                yanchor="top", y=0.99, xanchor="right", x=1.2, bordercolor="lightgrey", borderwidth=.8
            ))
        )
        fig.add_trace(go.Scatter(x=df_time_varying_r.index, y=df_time_varying_r.loc[:,'Q0.5'], name="rt", mode="lines", line_color="blue",
        line=dict(width = 3)))

        fig.add_trace(go.Scatter(
            x=df_time_varying_r.index,
            y=df_time_varying_r['Q0.975'],
            fill='tonexty',
            name="erro superior",
            mode='none',))

        fig.add_trace(go.Scatter(
            x=df_time_varying_r.index,
            y=df_time_varying_r['Q0.025'],
            fill='tonexty',
            name="erro inferior",
            mode='none'))

        fig.add_trace(go.Scatter(x=[df_time_varying_r.index.min(), df_time_varying_r.index.max()] , y= [1, 1], name="rt = 1", mode="lines", 
                                line_color="black", opacity=.35))
        return fig

if __name__ == "__main__":
    df = pd.read_csv("./data/df_cidades_campi.csv", parse_dates=["date"])
    df_redencao = df[df["city"] == "Redenção"]
    df_acarape = df[df["city"] == "Acarape"]
    df_SFC = df[df["city"] == "São Francisco do Conde"]

    print(df.head())
    print(type(df))
    rt = Calculate_Rt()

    # formatação e preparação dos dados para a construção dos gráficos
    df_reformated_acarape = rt.ajust_numbers(df_acarape)
    df_reformated_redencao = rt.ajust_numbers(df_redencao)
    df_reformated_SFC = rt.ajust_numbers(df_SFC)
    # print(df_reformated.head())
    # print(type(df_reformated))

    # gerando os gráficos das cidades de acarape, redenção e São Francisco do Conde com a janela padrão
    # rt.estimate(df_reformated_acarape, "Acarape")
    # fig = rt.estimate_plotly(df_reformated_acarape, "Redenção")
    # fig.to_html("novo3.html")

    rt.estimate_plotly(df_reformated_SFC, "São Francisco do Conde")

    # rt.estimate_by_windows(dataframe=df_reformated_acarape, city_name="Acarape", windows=14)
    # rt.estimate_by_windows(dataframe=df_reformated_redencao, city_name="Redênção", windows=14)
    # rt.estimate_by_windows(dataframe=df_reformated_SFC, city_name="São Francisco do Conde", windows=7)