import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel  # Import BaseModel from pydantic
from supabase import create_client, Client
from typing import Optional, List

# Replace these with your actual Supabase URL and API key
supabase_url: str = "https://ufbqvjyfkiqdctvdvzsr.supabase.co"
supabase_key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVmYnF2anlma2lxZGN0dmR2enNyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTIyOTgzMDAsImV4cCI6MjAyNzg3NDMwMH0.zT8tWhhi3xM-7WysTAAW7fUj-iUIMaQHvjnO13eXgCE"

# Create the Supabase client
supabase: Client = create_client(supabase_url, supabase_key)

class Movie(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    rating: Optional[float] = None
    votes: Optional[int] = None
    gross: Optional[float] = None
    genre: Optional[List[str]] = None
    metascore: Optional[int] = None
    certificate: Optional[str] = None
    director: Optional[str] = None
    year: Optional[int] = None
    description: Optional[str] = None
    runtime: Optional[int] = None
    

app = FastAPI()

@app.post("/movies/", response_model=Movie)
def create_movie(movie: Movie):
    data = movie.dict(exclude_unset=True)
    inserted_data = supabase.table("movies").insert(data).execute()
    if inserted_data.data:
        return inserted_data.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error inserting data")

@app.get("/movies/", response_model=List[Movie])
def read_movies():
    data = supabase.table("movies").select("*").execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=400, detail="Error reading data")
    

@app.put("/movies/{movie_id}", response_model=Movie)
def update_movie(movie_id: int, movie: Movie):
    data = movie.dict(exclude_unset=True)
    updated_data = supabase.table("movies").update(data).eq("id", movie_id).execute()
    if updated_data.data:
        return updated_data.data[0]
    else:
        raise HTTPException(status_code=400, detail="Error updating data")

@app.delete("/movies/{movie_id}", response_model=List[Movie])
def delete_movie(movie_id: int):
    deleted_data = supabase.table("movies").delete().eq("id", movie_id).execute()
    if deleted_data.data:
        return deleted_data.data
    else:
        raise HTTPException(status_code=400, detail="Error deleting data")

# Get the port from the PORT environment variable or use a default value
port = int(os.getenv("PORT", 8000))

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
