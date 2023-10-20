#Función para gráfico de caja, histograma y curva normal
def graficar_distribucion(data, cols):
    
    import numpy as np
    import scipy.stats as stats
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go

    df = data[cols]
    specs = [[{"type": "box"}, {"type": "histogram"},{"type": "scatter"}]  for i in range(5)]
    fig = make_subplots(
        rows = 5, cols = 3,
        specs = specs,
        subplot_titles = [c for c in cols for i in range(3)]
    )
    colors = [
        'rgb(72, 152, 202)',  # Azul suave
        'rgb(244, 162, 97)',  # Naranja suave
        'rgb(129, 196, 116)',  # Verde suave
        'rgb(235, 107, 86)',  # Rojo suave
        'rgb(190, 117, 202)'  # Morado suave
    ]
    for i in range(5):
        fig.add_trace(go.Box(y = df.iloc[:,i], marker_color=colors[i], name=""),
                row = i+1, col = 1)
    for i in range(5):
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