from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

# Supabase credentials
url: str = "https://edtyayokddrqlygguwnz.supabase.co"
key: str = "your_supabase_key_here"

supabase: Client = create_client(url, key)

app = FastAPI()

class Health(BaseModel):
    Id: int
    Name: str
    Age: int
    Gender: str
    Blood_Type: str
    Medical_Condition: str
    Date_of_Admission: str
    Doctor: str
    Hospital: str
    Insurance_Provider: str
    Billing_Amount: float
    Room_Number: int
    Admission_Type: str
    Discharge_Date: str
    Medication: str
    Test_Result: str

class HealthUpdate(BaseModel):
    Age: int
    Gender: str

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health_data/")
def read_items():
    data = supabase.table("df").select("*").order("Id", desc=True).limit(100).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Health data not found")

@app.put("/health_data/{Id}")
def update_health(Id: int, update: HealthUpdate):
    data = supabase.table("df").update(update.dict()).eq("Id", Id).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Health data not found")

@app.get("/highest_billing/")
def get_highest_billing():
    data = supabase.table("df").select("*").order("Billing_Amount", desc=True).limit(1).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Health data not found")

@app.get("/lowest_billing/")
def get_lowest_billing():
    data = supabase.table("df").select("*").order("Billing_Amount", asc=True).limit(1).execute()
    if data.data:
        return data.data
    else:
        raise HTTPException(status_code=404, detail="Health data not found")

@app.get("/blood_type_counts/")
def get_blood_type_counts():
    data = supabase.table("df").select("*").execute()
    if data.data:
        blood_type_counts = {}
        for item in data.data:
            blood_type = item["Blood_Type"]  # Replace "Blood_Type" with your actual column name
            if blood_type in blood_type_counts:
                blood_type_counts[blood_type] += 1
            else:
                blood_type_counts[blood_type] = 1
        return blood_type_counts
    else:
        raise HTTPException(status_code=404, detail="Health data not found")

@app.delete("/health_data/{Id}")
def delete_item(Id: int):
    data = supabase.table("df").delete().eq("Id", Id).execute()
    if data.data:
        return {"message": "Health data deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Health data not found")
