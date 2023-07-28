from dash import Dash , html, dcc, Output, Input, callback

from fastapi import FastAPI
import uvicorn
from starlette.middleware.wsgi import WSGIMiddleware
import pandas as pd
import pickle
import requests
import numpy as np

colors = {
    "text":"#370617"
}

movies = pd.read_csv("/home/abdoun0hocine/devs/fastapi/f_dash/top10K-TMDB-movies.csv")
movies_list = movies['title'].to_list()
#----------------------------------------------------------------------------

def fetch_poster(movie_id):
     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=e2d8b6a27f2fc324f7195d3275cc8917&language=en-US"
     data=requests.get(url)
     data=data.json()
     poster_path = data['poster_path']
     full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
     return full_path






#----------------------------------------------------------------------------


sim = pickle.load(
    open("/home/abdoun0hocine/devs/fastapi/f_dash/content/similarity.pkl", "rb"))


def recommand(movie):
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(sim[index])), reverse = True, key=lambda vec:vec[1])
    recommand_movie = []
    recommend_poster=[]
    for d in distance[1:7]:
        movie_id=movies.iloc[d[0]].id
        recommand_movie.append(movies.iloc[d[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommand_movie, recommend_poster 
  

#----------------------------------------------------------------------------


def reco(movie):
    index = movies[movies['title'] == str(movie)].index[0]
    distance = sorted(list(enumerate(sim[index])), reverse = True, key=lambda vec:vec[1])
    recommand_movie = []
    for d in distance[1:7]:
        recommand_movie.append(movies.iloc[d[0]].title)
    return recommand_movie


imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),]







app = Dash(__name__, requests_pathname_prefix="/")

app.layout=html.Div([
    
html.Div([

    html.Div([
                html.Img(src=imageUrls[1], style={"width":"290px", "height":"450px"}),
                html.Img(src=imageUrls[2], style={"width":"290px"}),
                html.Img(src=imageUrls[3], style={"width":"290px"}),
                html.Img(src=imageUrls[4], style={"width":"290px"}),
                html.Img(src=imageUrls[5], style={"width":"290px"}),
                html.Img(src=imageUrls[0], style={"width":"290px"}),
    ], style={"display":"flex"}),

    


    html.Div([
    html.Label("Choose your movie"),  
    html.Br(), 
    dcc.Dropdown(value = [], options = movies_list, id="input")

]),
    ],
    
            style = {
        "color": colors['text'],
        'flex' : 1  ,
        'fontWeight': 'bold',
        'fontSize':20}
    
    ),

html.Div([  html.Br(),
            html.Label("Recommended movies"), 
            html.Br(),
            html.Br(),
            html.Br(),], 
        style = {
        "color": colors['text'],
        'flex' : 1  ,
        'fontWeight': 'bold',
        'fontSize':30}),


html.Div([




html.Div(id = "output1",children=[
    html.Div(id='tit1', children=[]),
    html.Br(),
    html.Img(id ="img1",  src="", style={"width":"290px"})

]),
html.Div(id = "output2",children=[
    html.Div(id='tit2', children=[]),
    html.Br(),
    html.Img(id ="img2",  src="",style={"width":"290px"})
    

]),

html.Div(id = "output3",children=[
    html.Div(id='tit3', children=[]),
    html.Br(),
    html.Img(id ="img3",  src="",style={"width":"290px"})
]),
html.Div(id = "output4",children=[
    html.Div(id='tit4', children=[]),
    html.Br(),
    html.Img(id ="img4",  src="",style={"width":"290px"})
]),
html.Div(id = "output5",children=[
    html.Div(id='tit5', children=[]),
    html.Br(),
    html.Img(id ="img5",  src="",style={"width":"290px"})
]),
html.Div(id = "output6",children=[
    html.Div(id='tit6', children=[]),
    html.Br(),
    html.Img(id ="img6",  src="",style={"width":"290px"})
]),



],  style={
         'fontWeight': 'bold',   
        'textAlign': 'center',
        "color": colors['text'],
        "display":"flex",
        'flex' : 6,
        'fontSize':18
        
        
        })






])







@callback(
    Output("tit1", "children"),
    Output("tit2", "children"),
    Output("tit3", "children"),
    Output("tit4", "children"),
    Output("tit5", "children"),
    Output("tit6", "children"),


    Output("img1", 'src'),
    Output("img2", 'src'),
    Output("img3", 'src'),
    Output("img4", 'src'),
    Output("img5", 'src'),
    Output("img6", 'src'),
    
    Input('input','value' )
    
    
)

def print_recommendations(input_value):
        movie , poster = recommand(input_value)
        full = []
        for m in movie :
            full.append(m)
        for p in poster:
            full.append(p)    

        return full

if __name__=='__main__':
    app.run_server(debug=True)


''' server = FastAPI()
server.mount("/", WSGIMiddleware(app.server))
uvicorn.run(server) '''

