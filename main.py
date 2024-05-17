from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from typing import List, Optional

# Supabase credentials
supabase_url: str = "https://ufbqvjyfkiqdctvdvzsr.supabase.co"
supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYnF2anlma2lxZGN0dmR2enNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIyOTgzMDAsImV4cCI6MjAyNzg3NDMwMH0.zT8tWhhi3xM-7WysTAAW7fUj-iUIMaQHvjnO13eXgCE"

supabase: Client = create_client(supabase_url, supabase_key)

class AnimatedMovie(BaseModel):
    title: Optional[str] = None
    rating: Optional[float] = None
    votes: Optional[int] = None
    gross: Optional[float] = None
    genre: Optional[str] = None
    metascore: Optional[int] = None
    certificate: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    runtime: Optional[int] = None

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Animated Movies API"}

@app.post("/movies/", response_model=AnimatedMovie)
def create_movie(movie: AnimatedMovie):
    data = movie.dict(exclude_unset=True)
    inserted_data = supabase.table("movies").insert(data).execute()
    if inserted_data.data:
        return inserted_data.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error inserting data")

@app.get("/movies/", response_model=List[AnimatedMovie])
def read_movies():
    data = supabase.table("movies").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Error reading data")

@app.get("/movies/search/{search_term}", response_model=List[AnimatedMovie])
def search_movies(search_term: str):
    data = supabase.table("movies").select("*").execute()
    if data.data:
        return [movie for movie in data.data if search_term.lower() in movie["title"].lower()]
    else:
        raise HTTPException(status_code=400, detail="Error searching data")

@app.get("/movies/filter/{genre}", response_model=List[AnimatedMovie])
def filter_movies(genre: str):
    data = supabase.table("movies").select("*").execute()
    if data.data:
        return [movie for movie in data.data if movie["genre"].lower() == genre.lower()]
    else:
        raise HTTPException(status_code=400, detail="Error filtering data")

@app.get("/movies/sort/{sort_by}/{sort_order}", response_model=List[AnimatedMovie])
def sort_movies(sort_by: str, sort_order: str):
    data = supabase.table("movies").select("*").execute()
    if data.data:
        if sort_by.lower() == "title":
            if sort_order.lower() == "asc":
                return sorted(data.data, key=lambda x: x["title"])
            elif sort_order.lower() == "desc":
                return sorted(data.data, key=lambda x: x["title"], reverse=True)
        elif sort_by.lower() == "metascore":
            if sort_order.lower() == "asc":
                return sorted(data.data, key=lambda x: x["metascore"])
            elif sort_order.lower() == "desc":
                return sorted(data.data, key=lambda x: x["metascore"], reverse=True)
        else:
            raise HTTPException(status_code=400, detail="Invalid sort_by or sort_order")
    else:
        raise HTTPException(status_code=400, detail="Error sorting data")
