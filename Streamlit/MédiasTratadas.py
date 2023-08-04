import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from PIL import Image
from prettytable import PrettyTable


#df = pd.read_csv(r"C:\Users\abril\OneDrive\Documentos\Turing\Portfólio\Streamlit\valores.csv")
df = pd.read_csv("Streamlit/valores2.csv")

col1, col2 = st.columns([0.08, 0.85])
with col1:
    st.image(Image.open("Streamlit/Traçado laranja #f1863d.png"))
with col2:
    st.title("Análise das turmas de Cálculo III - 2022 (lembranças de bons tempos)")

#--------------------------------------------- CONTAGENS PARA GRÁFICOS ---------------------------------------------

turmas = [] #do 1 ao 14
P2 = [] #do 0 ao 12
P3 = [] #do 0 ao 12
Sub = [] #do 0 ao 12
Rec = [] #do 0 ao 12
M1 = [] #do 0 ao 12
Msub = [] #do 0 ao 12
M2 = [] #do 0 ao 12


for i in range (1, 14):
    turmas.append(df[df['Turma'] == i])

for i in range (0, 13):
    P2.append(turmas[i].groupby("P2", as_index = False)["NUSP"].count())
    P3.append(turmas[i].groupby("P3", as_index = False)["NUSP"].count())
    Sub.append(turmas[i].groupby("Sub", as_index = False)["NUSP"].count())
    Rec.append(turmas[i].groupby("Rec", as_index = False)["NUSP"].count())
    M1.append(turmas[i].groupby('M1', as_index = False)['NUSP'].count())    
    Msub.append(turmas[i].groupby('MSub', as_index = False)['NUSP'].count())
    M2.append(turmas[i].groupby("M2", as_index = False)['NUSP'].count())


mFinais = [] #0, M1; 1, Msub; 2, M2
mFinais.append(df.groupby("M1", as_index = False)['NUSP'].count().mean()[0])
mFinais.append(df.groupby("MSub", as_index = False)['NUSP'].count().mean()[0])
mFinais.append(df.groupby("M2", as_index = False)['NUSP'].count().mean()[0])

# --------------------------------------------- MÉDIAS ---------------------------------------------

# ----- Valores totais
mProvas = [] #0, P2; 1, P3; 2, Sub; 3, Rec

mProvas.append(round(df['P2'].mean(), 2))
mProvas.append(round(df['P3'].mean(), 2))
mProvas.append(round(df['Sub'].mean(), 2))
mProvas.append(round(df['Rec'].mean(), 2))

medianaProvas = []
medianaProvas.append(round(df['P2'].median(), 2))
medianaProvas.append(round(df['P3'].median(), 2))
medianaProvas.append(round(df['Sub'].median(), 2))
medianaProvas.append(round(df['Rec'].median(), 2))


# ----- Divisão por turmas
mediasM1 = [] #Médias s/ sub
mediasMSub = [] #Médias c/sub
mediasM2 = [] #Médias c/ rec

dvM1= [] #Desvio padrão da média s/sub
dvMsub = [] #Desvio padrão da média c/sub
dvM2 = [] #Desvio padrão da média c/rec

for i in range (1, 13):
    mediasM1.append(df[df['Turma']  == i]['M1'].mean())
    mediasMSub.append(df[df['Turma']  == i]['MSub'].mean())
    mediasM2.append(df[df['Turma']  == i]['M2'].mean())

    dvM1.append(df[df['Turma']  == i]['M1'].std())
    dvMsub.append(df[df['Turma']  == i]['MSub'].std())
    dvM2.append(df[df['Turma']  == i]['M2'].std())

# --------------------------------------------- VISUAL ---------------------------------------------

tab1, tab2, tab3, tab4 = st.tabs(['Visão Geral', 'Visão Detalhada', 'Área Reservada', 'Comparação'])

with tab1:
    st.write("A turma de 2022 de cálculo III passou por algumas adversidades ao longo do semestre. Das 3 provas propostas, uma foi cancelada e outra teve seu peso bastante reduzido, sendo, praticamente, toda a nota da disciplina concentrada na terceira prova.")
    st.write("Esse acúmulo de importância na terceira prova gerou uma reprovação maciça entre os alunos que cursavam a disciplina.")
    st.write("Os índices de reprovação tornaram necessárias a adoção de medidas para tentar reverter o quadro. A prova sub, então, foi declarada aberta e teoricamente facilitada, em relação à P3, por exemplo.")
    st.write("Este streamlit se propõe a analisar brevemente tais impactos e a eficiência das medidas propostas para mitigar os estragos ocasionados.")
    with st.expander("Panorama"):
        criterioM1 = df['M1'] >= 5
        criterioMSub = df['MSub'] >= 5
        criterioM2 = df['M2'] >= 5
        col1, col2, col3, col4, col5 = st.columns([1, 0.125, 2, 2, 2])
        with col1:
            ap1 = df[criterioM1]['NUSP'].count().sum()
            ap2 = (df[criterioMSub]['NUSP'].count().sum() - ap1)
            ap3 = (df[criterioM2]['NUSP'].count().sum() - (ap1 + ap2))
            st.write(str (df['NUSP'].count()), "alunos matriculados")
            st.write(str(ap1), "alunos aprovados sem sub")
            st.write(str(ap2), "alunos aprovados com sub")
            st.write(str(ap3), "alunos aprovados na rec")
            st.write("Números finais:\n")
            st.write(str(ap1 + ap2 + ap3), "alunos aprovados") 
            st.write(str(df['NUSP'].count().sum() - (ap1 + ap2 + ap3)), "alunos reprovados")
        with col2:
            st.write('---\n---\n-----\n----\n----\n----\n----\n-----\n---\n---\n----\n----\n----\n----')

        # ----- Gráficos de pizza
        with col3:
            st.subheader("Aprovações sem sub")
            A1 = pd.DataFrame({"Alunos": [ap1, df[~criterioM1]['NUSP'].count().sum()], "Situação": ["Aprovados", "Reprovados"]})
            fig = px.pie(A1, values = "Alunos", color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
            st.plotly_chart(fig, use_container_width = True)
        with col4:
            st.subheader("Aprovações com sub")
            A2 = pd.DataFrame({"Alunos": [(ap2 + ap1 ), df[~criterioMSub]['NUSP'].count().sum()], "Situação": ["Aprovados", "Reprovados"]})
            fig = px.pie(A2, values = "Alunos", color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
            st.plotly_chart(fig, use_container_width = True)
        with col5:
            st.subheader("Aprovações com rec")
            A3 = pd.DataFrame({"Alunos": [(ap1 + ap2 + ap3), df[~criterioM2]['NUSP'].count().sum()], "Situação": ["Aprovados", "Reprovados"]})
            fig = px.pie(A3, values = "Alunos", color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
            st.plotly_chart(fig, use_container_width = True)    
        st.divider()

        # ----- Tabelas
        st.subheader("Análise por turma")
        col1, col2, col3  = st.columns([1, 2, 2])
        with col2:
            ssub = mediasM1.index(max(mediasM1)) + 1
            csub = mediasMSub.index(max(mediasMSub)) + 1
            crec =mediasM2.index(max(mediasM2)) + 1

            dpssub = dvM1.index(min(dvM1)) + 1
            dpcsub = dvMsub.index(min(dvMsub)) + 1
            dprec = dvM2.index(min(dvM2)) + 1


            tab = PrettyTable()
            tab.field_names = ['---', ' ----', '-----']
            tab.add_row([' ', 'Maior média', 'Mais regular (DesvPad)'])
            tab.add_row(['S/ sub', 'Turma '+ str(ssub) +' - ' + str(round(max(mediasM1), 2)), 'Turma '+ str(dpssub) +' - ' + str(round(min(dvM1), 2))])
            tab.add_row(['C/ sub', 'Turma '+ str(csub) +' - ' + str(round(max(mediasMSub), 2)), 'Turma '+ str(dpcsub) +' - ' + str(round(min(dvMsub), 2))])
            tab.add_row(['C/ rec', 'Turma '+ str(crec) +' - ' + str(round(max(mediasM2), 2)), 'Turma '+ str(dprec) +' - ' + str(round(min(dvM2), 2))])
            tab.align = 'c'
            st.write(tab)
        
        with col3:
            aprovacoes = PrettyTable()
            aprovacoes.field_names =  ['Turma', 'Aprovados', 'Reprovados', '%']

            for i in range(0, 13):
                passou = M2[i][criterioM2]['NUSP'].sum()
                reprovou = M2[i][~criterioM2]['NUSP'].sum()
                porcentagem = passou/M2[i]['NUSP'].sum()*100
                aprovacoes.add_row([i + 1, passou, reprovou, round(porcentagem, 2)])

            st.write(aprovacoes)
        st.divider()

       
    with st.expander("P2"):
        st.write("Número de provas realizadas: " + str(df['P2'].count()))
        st.write("Média global: " + str(round(mProvas[0], 2)))
        st.write("Mediana global: " + str(round(medianaProvas[0], 2)))
        st.bar_chart(data = df.groupby("P2", as_index = False)['NUSP'].count(), x = 'P2', y = 'NUSP')

    with st.expander("P3"):
        st.write("Número de provas realizadas: " + str(df['P3'].count()))
        st.write("Média global: " + str(round(mProvas[1], 2)))
        st.write("Mediana global: " + str(round(medianaProvas[1], 2)))
        st.bar_chart(data = df.groupby("P3", as_index = False)['NUSP'].count(), x = 'P3', y = 'NUSP')

    with st.expander("PSub"):
        st.write("Número de provas realizadas: " + str(df['Sub'].count()))
        st.write("Média global: " + str(round(mProvas[2], 2)))
        st.write("Mediana global: " + str(round(medianaProvas[2], 2)))
        st.bar_chart(data = df.groupby("Sub", as_index = False)['NUSP'].count(), x = 'Sub', y = 'NUSP')

    with st.expander("PRec"):
        st.write("Número de provas realizadas: " + str(df['Rec'].count()))
        st.write("Média global: " + str(round(mProvas[3], 2)))
        st.write("Mediana global: " + str(round(medianaProvas[3], 2)))
        st.bar_chart(data = df.groupby("Rec", as_index = False)['NUSP'].count(), x = 'Rec', y = 'NUSP')

with tab2:
    opcao = st.radio("Escolha uma opção para visualizar:", ("Notas da P2", "Notas da P3", "Notas da Sub", "Notas da Rec", "Médias sem sub", "Médias com sub", "Médias com rec"))

    if opcao == "Notas da P2":
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = P2[turma - 1], x = 'P2', y = 'NUSP')
            st.divider()
            st.write("Foram realizadas", str(P2[turma - 1]['NUSP'].sum()), "provas")
            st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['P2'].mean(), 2)))
            st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['P2'].median(), 2)))
            st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['P2'].std(), 2)))

    elif opcao == 'Notas da P3':
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = P3[turma - 1], x = 'P3', y = 'NUSP')
            st.divider()
            st.write("Foram realizadas", str(P3[turma - 1]['NUSP'].sum()), "provas")
            st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['P3'].mean(), 2)))
            st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['P3'].median(), 2)))
            st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['P3'].std(), 2)))

    elif opcao == 'Notas da Sub':
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = Sub[turma - 1], x = 'Sub', y = 'NUSP')
            st.divider()
            st.write("Foram realizadas", str(Sub[turma - 1]['NUSP'].sum()), "provas")
            st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['Sub'].mean(), 2)))
            st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['Sub'].median(), 2)))
            st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['Sub'].std(), 2)))

    elif opcao == 'Notas da Rec':
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = Rec[turma - 1], x = 'Rec', y = 'NUSP')
            st.divider()
            st.write("Foram realizadas", str(Rec[turma - 1]['NUSP'].sum()), "provas")
            st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['Rec'].mean(), 2)))
            st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['Rec'].median(), 2)))
            st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['Rec'].std(), 2)))

    elif opcao == 'Médias sem sub':
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = M1[turma - 1], x = 'M1', y = 'NUSP')
            st.divider()
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                st.subheader("Informações da turma:")
                st.write(str(M1[turma - 1]['NUSP'].sum()), "alunos matriculados na turma")
                st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['M1'].mean(), 2)))
                st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['M1'].median(), 2)))
                st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['M1'].std(), 2)))
            with col2:
                criterio = M1[turma - 1]['M1'] >= 5
                aprovados = M1[turma - 1][criterio]['NUSP'].sum()
                reprovados = M1[turma - 1][~criterio]['NUSP'].sum()
                dados = pd.DataFrame({"Alunos": [aprovados, reprovados], "Situação": ["Aprovados", "Reprovados"]})
                fig =  px.pie(dados, values = "Alunos", names = "Situação", title = '\tTaxa de aprovação', color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
                st.plotly_chart(fig)

    elif opcao == 'Médias com sub':
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = Msub[turma - 1], x = 'MSub', y = 'NUSP')
            st.divider()
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                st.subheader("Informações da turma:")
                st.write(str(Msub[turma - 1]['NUSP'].sum()), "alunos matriculados na turma")
                st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['MSub'].mean(), 2)))
                st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['MSub'].median(), 2)))
                st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['MSub'].std(), 2)))
            with col2:
                criterio = Msub[turma - 1]['MSub'] >= 5
                aprovados = Msub[turma - 1][criterio]['NUSP'].sum()
                reprovados = Msub[turma - 1][~criterio]['NUSP'].sum()
                dados = pd.DataFrame({"Alunos": [aprovados, reprovados], "Situação": ["Aprovados", "Reprovados"]})
                fig =  px.pie(dados, values = "Alunos", names = "Situação", title = '\tTaxa de aprovação', color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
                st.plotly_chart(fig)

    elif opcao == 'Médias com rec':
        turma = st.selectbox("Selecione a turma", (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13))
        if st.button('Gerar gráfico'):
            st.subheader("Turma " + str(turma))
            st.bar_chart(data = M2[turma - 1], x = 'M2', y = 'NUSP')
            st.divider()
            col1, col2 = st.columns([0.3, 0.7])
            with col1:
                st.subheader("Informações da turma:")
                st.write(str(M2[turma - 1]['NUSP'].sum()), "matriculados na turma")
                st.write("A média da turma é:", str(round(df[df['Turma'] == turma]['M2'].mean(), 2)))
                st.write("A mediana da turma é:", str(round(df[df['Turma'] == turma]['M2'].median(), 2)))
                st.write("O desvio padrão da turma é:", str(round(df[df['Turma'] == turma]['M2'].std(), 2)))
            with col2:
                criterio = M2[turma - 1]['M2'] >= 5
                aprovados = M2[turma - 1][criterio]['NUSP'].sum()
                reprovados = M2[turma - 1][~criterio]['NUSP'].sum()
                dados = pd.DataFrame({"Alunos": [aprovados, reprovados], "Situação": ["Aprovados", "Reprovados"]})
                fig =  px.pie(dados, values = "Alunos", names = "Situação", title = '\tTaxa de aprovação', color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
                st.plotly_chart(fig)
                

with tab3:
    number = st.number_input("Digite a senha")

    if number == 2022:
        st.image(Image.open("https://github.com/CesAug/Portfolio/blob/main/Streamlit/OsCulpados.png"))
        number = 0
    else:
        st.subheader("Senha incorreta")

with tab4:
    dt = pd.read_csv("Streamlit/comparacao.csv")

    st.header("Cálculo III - turma 2023")
    col1, col2 = st.columns(2)

    with col2:
        st.write(str(dt['NUSP'].count().sum()), " alunos matriculados")
        criterio = dt['M1'] >= 5
        aprovados= dt[criterio]['NUSP'].count().sum()
        reprovados = dt[~criterio]['NUSP'].count().sum()
        final = pd.DataFrame({"Alunos": [aprovados, reprovados], "Situação": ["Aprovados", "Reprovados"]})
        fig =  px.pie(final, values = "Alunos", names = "Situação", title = '\tTaxa de aprovação', color = "Situação", color_discrete_map= {"Aprovados": 'blue', "Reprovados": "#DC3912"})
        st.plotly_chart(fig)

    with col1:
        st.subheader("P2")
        st.write("A média é: ", str(round(dt['P2'].mean(), 2)))
        st.write("A mediana da turma é:", str(round(dt['P2'].median(), 2)))
        st.write("O desvio padrão é: ", str(round(dt['P2'].std(), 2)))
        st.bar_chart(data = dt.groupby("P2", as_index = False)['NUSP'].count(), x = 'P2', y = 'NUSP')   
        
        st.subheader("Sub")
        st.write("A média é: ", str(round(dt['Sub'].mean(), 2)))
        st.write("A mediana da turma é:", str(round(dt['Sub'].median(), 2)))
        st.write("O desvio padrão é: ", str(round(dt['Sub'].std(), 2)))
        st.write("Número de provas realizadas: ", str(dt["Sub"].count().sum()))
        st.bar_chart(data = dt.groupby("Sub", as_index = False)['NUSP'].count(), x = 'Sub', y = 'NUSP')   

