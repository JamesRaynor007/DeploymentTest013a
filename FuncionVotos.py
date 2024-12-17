from fastapi import FastAPI, HTTPException, Request
import pandas as pd
import os

# Definir la ruta del archivo CSV
file_path = os.path.join(os.path.dirname(__file__), 'FuncionVotos.csv')

app = FastAPI(
    title="API de Votaciones de Películas",
    description="Esta API permite consultar información sobre películas y sus votaciones.",
    version="1.0.0",
)

df = pd.read_csv(file_path)
print(df.head())  # Verifica las primeras filas del DataFrame


@app.get("/")
async def read_root(request: Request):
    base_url = str(request.url).rstrip('/')
    return {
        "message": "Bienvenido a la API de Votaciones de Películas!",
        "description": "Utiliza los siguientes endpoints para interactuar con la API:",
        "endpoints": {
            f"{base_url}/votes/?title=<nombre_pelicula>": "Devuelve información sobre la película especificada.",
            f"{base_url}/titles/": "Devuelve una lista de todos los títulos de películas disponibles."
        },
        "example": {
            "Buscar película": f"{base_url}/votes/?title=Inception",
            "Listar títulos": f"{base_url}/titles/"
        }
    }


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