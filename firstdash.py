from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Création de l'application avec suppress_callback_exceptions=True
app = Dash(__name__, suppress_callback_exceptions=True)
df = pd.read_csv("https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv", error_bad_lines=False)
top_10_books = df.head(10)

fig = px.bar(top_10_books, x='title', y='  num_pages', color='average_rating',
             title='Les 10 premiers Livres',
             hover_data=['  num_pages'])

app.layout = html.Div([
    html.H1("Les 10 premiers Livres"),
    dcc.Graph(id='graph', figure=fig),
    html.I('Choisis un auteur :'),
    dcc.Dropdown(id='author-dropdown', options=[{'label': author, 'value': author} for author in df['authors'].unique()],
                 multi=False, value=df['authors'].unique()[0]),
    html.I('Choisis un nombre de pages :'),
    dcc.Input(id="input1", type="text", placeholder=""),
])

# Callback pour le filtrage par auteur et nombre de pages
@app.callback(
    Output('graph', 'figure'),
    [Input('author-dropdown', 'value'),
     Input('input1', 'value')]
)
def update_graph(selected_author, max_pages):
    filtered_df = df.copy()

    if selected_author:
        filtered_df = filtered_df[filtered_df['authors'] == selected_author]

    if max_pages and max_pages.isdigit():
        max_pages = int(max_pages)
        filtered_df = filtered_df[filtered_df['  num_pages'] <= max_pages]

    updated_fig = px.bar(filtered_df, x='title', y='  num_pages', color='average_rating',
                         title=f'Livres filtrés',
                         hover_data=['  num_pages'])
    return updated_fig

if __name__ == '__main__':
    app.run_server(debug=True)
