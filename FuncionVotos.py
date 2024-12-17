
from fastapi import FastAPI, HTTPException
import pandas as pd
import os

# Definir la ruta del archivo CSV
file_path = os.path.join(os.path.dirname(__file__), 'FuncionVotos.csv')

app = FastAPI()

df = pd.read_csv('FuncionVotos.csv')
print(df.head())  # Verifica las primeras filas del DataFrame


@app.get("/votes/")
async def get_movie(title: str):
    print(f"Buscando película: '{title}'")  # Muestra el título buscado
    movie = df[df['title'].str.lower() == title.lower()]
    print(f"Películas encontradas: {movie}")  # Muestra el DataFrame encontrado

    if movie.empty:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    movie_data = movie.iloc[0]
    return {
        "title": movie_data['title'],
        "vote_count": "La pelicula cuenta con menos de 2000 valoraciones" if movie_data['vote_count'] in [0, 1999] else int(movie_data['vote_count']),  # Convert to int with condition
        "vote_average": "" if movie_data['vote_count'] in [0, 1999] else float(movie_data['vote_average'])  # Convert to float
    }

@app.get("/titles/")
async def get_titles():
    print("Llamando al endpoint /titles/")  # Para diagnóstico
    return df['title'].tolist()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

