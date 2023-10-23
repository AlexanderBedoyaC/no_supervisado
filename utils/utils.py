import numpy as np
import pandas as pd
import scipy.stats as stats
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
    
#Función para gráfico de caja, histograma y curva normal
def graficar_distribucion(data, cols):

    df = data[cols]
    specs = [[{"type": "box"}, {"type": "histogram"},{"type": "scatter"}]  for i in range(len(cols))]
    fig = make_subplots(
        rows = len(cols), cols = 3,
        specs = specs,
        subplot_titles = [c for c in cols for i in range(3)]
    )
    colors = [
        'rgb(72, 152, 202)',  # Azul suave
        'rgb(244, 162, 97)',  # Naranja suave
        'rgb(129, 196, 116)',  # Verde suave
        'rgb(235, 107, 86)',  # Rojo suave
        'rgb(190, 117, 202)'  # Morado suave
    ]*3
    for i in range(len(cols)):
        fig.add_trace(go.Box(y = df.iloc[:,i], marker_color=colors[i], name=""),
                row = i+1, col = 1)
    for i in range(len(cols)):
        x = np.sort(df.iloc[:,i])
        media = np.mean(x)
        sd = np.std(x)
        pdf = stats.norm.pdf(x, loc = media, scale = sd)
        fig.add_trace(go.Histogram(x = x, marker_color=colors[i]),
                row = i+1, col = 2)
        fig.add_trace(go.Scatter(x = x, y = pdf, mode ='lines', line=dict(color=colors[i], width=2),),
                row = i+1, col = 3)
        
    fig.update_layout(height=1200, showlegend=False)
    fig.show()
    
#Genera tabla de frecuencias para una variable
def tabla_frecuencias(df, col):
    
    n = df.shape[0]
    tabla = df.groupby([col])[[col]].count().rename(columns={col:'Frecuencia Absoluta'}).reset_index()
    tabla['Frecuencia Relativa'] = tabla['Frecuencia Absoluta'].apply(lambda x: str(round(100*x/n, 3))+' %')
    
    return tabla.sort_values(by='Frecuencia Absoluta', ascending=True)

#Genera tabla de frecuencias y gráfico de barras para una variable
def univariado_barras(df, col, orientation='v', h=400,n=10):
    
    if orientation=='v':
        x = col
        y = ['Frecuencia Absoluta']
    else:
        x = ['Frecuencia Absoluta']
        y = col
    
    tabla = tabla_frecuencias(df, col)
    
    fig = px.bar(tabla.iloc[-n:,:],
             x = x,
             y = y,
             text_auto = True,
             title = col.capitalize().replace('_', ' '),
             height = h,
             labels = {'value': 'Total', col:col},
             text = 'Frecuencia Relativa', orientation=orientation)
    fig.layout.update(showlegend=False)
    fig.show()
    
    return tabla.iloc[-n:,:].sort_values(by='Frecuencia Absoluta', ascending=False)

#Obtener tablas de contingencia y graficarlas
def Analisisbivariado(df,variables,orient,mode,color=px.colors.qualitative.Plotly):
    contingency_table=pd.crosstab(df[variables[0]],df[variables[1]])
    contingency_table = contingency_table.div(contingency_table.sum(axis=1), axis=0)
    fig=px.bar(contingency_table,orientation=orient,barmode=mode,color_discrete_sequence=color)
    fig.update_layout(title=dict(x=0.5))
    fig.update_traces(texttemplate='%{value:.2%}', textposition='outside')
    fig.show()
    print("Tabla de contingencia:")
    return contingency_table

#Obtener correlaciones de variables categóricas
def corr_cat(df):
    from scipy.stats import chi2_contingency
    
    cols = df.columns
    df_corr_cat = pd.DataFrame()

    corrs = []
    for col in cols:
        tabla_contingencia = pd.crosstab(df['attrition'], df[col])
        chi2, p, _, _ = chi2_contingency(tabla_contingencia)
        corrs.append(p)
    df_corr_cat['attrition'] = corrs
    df_corr_cat.index = cols
    
    return df_corr_cat