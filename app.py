import pandas as pd
import plotly.express as px
import streamlit as st



# Lendo as bases de dados
df_vendas = pd.read_excel("Vendas.xlsx")
df_produtos = pd.read_excel("Produtos.xlsx")

# Merge
df = pd.merge(df_vendas, df_produtos, how="left", on="ID Produto")

# Novas colunas
df["Custo"] = df["Custo Unitário"] * df["Quantidade"]
df["Lucro"] = df["Valor Venda"] - df["Custo"]
df["mes_ano"] = df["Data Venda"].dt.to_period("M").astype(str)

#Agrupamentos
produtos_vendidos_marca = df.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
lucro_categoria = df.groupby("Categoria")["Lucro"].sum().reset_index()
lucro_mes_categoria = df.groupby(["mes_ano", "Categoria"])["Lucro"].sum().reset_index()



page_bg_img = '''
<style>
[data-testid="stAppViewContainer"]{
background-color: #d2d2d7;
opacity: 0.8;
background-image:  radial-gradient(#dcdce3 0.5px, transparent 0.5px), radial-gradient(#dcdce3 0.5px, #d2d2d7 0.5px);
background-size: 20px 20px;
background-position: 0 0,10px 10px;
}
</style>

'''




#Aplicação


def main():

    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.title("Análise de vendas")
    st.image("vendas.png")

    total_custo = (df["Custo"].sum()).astype(str)
    total_custo = total_custo.replace(".",",")
    total_custo = "R$" + total_custo[:2] +"." + total_custo[2:5] + "." + total_custo[5:]

    total_lucro = (df["Lucro"].sum()).astype(str)
    total_lucro = total_lucro.replace(".",",")
    total_lucro = "R$" + total_lucro[:2] +"." + total_lucro[2:5] + "." + total_lucro[5:]

    total_clientes = df["ID Cliente"].nunique()

    
    st.markdown(
    """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 30px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    st.markdown(
    """
    <style>
    [data-testid="stMetricLabel"] {
        font-size: 20px;
        color: rgba(0,0,0,0,)
    }
    </style>
    """,
    unsafe_allow_html=True,
    )

    


    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Custo", total_custo)
    with col2:
        st.metric("Total Lucro", total_lucro)
    with col3:
        st.metric("Total Clientes", total_clientes)



    
    col1, col2 = st.columns(2)

    fig = px.bar(produtos_vendidos_marca, x="Quantidade", y="Marca", orientation="h",
                 text="Quantidade", title="Total produtos vendidos por Marca",
                 width=420, height=400, color_discrete_sequence=["#084d6e"])
    fig.update_layout(paper_bgcolor="rgb(215,215,215)", plot_bgcolor="rgb(215,215,215)")
    col1.plotly_chart(fig, theme=None)

    fig1 = px.pie(lucro_categoria, values="Lucro", names="Categoria",
                  title="Lucro por Categoria", width=450, height=400,
                  color_discrete_sequence=["#084d6e"])
    fig1.update_layout(paper_bgcolor="rgb(215,215,215)", plot_bgcolor="rgb(215,215,215)")
    col2.plotly_chart(fig1)

   

    fig2 = px.line(lucro_mes_categoria, x="mes_ano", y="Lucro", color="Categoria",
                   title="Lucro x Mês x Categoria", markers=True,
                   width=810,height=400, color_discrete_sequence=px.colors.qualitative.D3)
    fig2.update_layout(paper_bgcolor="rgb(215,215,215)", plot_bgcolor="rgb(215,215,215)")
    st.plotly_chart(fig2)


if __name__ == "__main__":
    main()
