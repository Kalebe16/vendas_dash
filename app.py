from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server
# SEMPRE FAZER ESSE PROCESSO QUANDO CRIAR UM PROJETO COM DASH

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.read_excel("Vendas.xlsx")


# CRIANDO O GRÁFICO
fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

opcoes = list(df['ID Loja'].unique()) # criou uma lista com os itens da coluna ID Loja da tabela vendas
                                      # unique() serve para ter 2 valores repetidos na lista
opcoes.append("Todas as Lojas")

app.layout = html.Div(children=[
    html.H1(children='Vendas das lojas'),
    html.H2(children='Gráfico com o numero de vendas de Todos os Produtos separados por loja'),


    html.Div(children='''
        Obs: Esse gráfico mostra a quantidade de produtos vendidos, não o faturamento.
    '''),


    dcc.Dropdown(opcoes, value='Todas as Lojas', id='lista_lojas'),
                # OPCOES     |  VALOR INICIAL    |  NOME DO BOTÃO

    dcc.Graph(
        id='grafico_quantidade_vendas',
        figure=fig
    )
])


@app.callback(
    Output('grafico_quantidade_vendas', 'figure'), # QUEM VAI SER MODIFICADO | parametro children modifica o texto
    Input('lista_lojas', 'value')  # QUEM VAI SELECIONAR A INFORMAÇÃO
)
def update_output(value): 
    if value == "Todas as Lojas":
        fig = px.bar(df, x="Produto", y="Quantidade", color="ID Loja", barmode="group")
    else:
        # tabela_filtrada = df.loc[linha, coluna]
        tabela_filtrada = df.loc[df['ID Loja']==value, :] 
        fig = px.bar(tabela_filtrada, x="Produto", y="Quantidade", color="ID Loja", barmode="group")

        
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
