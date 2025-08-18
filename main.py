# main.py (Final Version with CORS Enabled)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import json

# STEP 1: Import the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

# Use 'scrapper' or 'scraper' depending on your filename
from scrapper import get_profile_data, search_for_prospects 
from ai_core import generate_personalized_message

app = FastAPI(
    title="LinkedIn Sales Automation Tool",
    description="An AI-powered tool to generate personalized outreach messages."
)

# STEP 2: Add the CORS middleware to your application
# This tells the browser that it's okay for your frontend to talk to this backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)


class ProspectingRequest(BaseModel):
    ideal_job_roles: str = Field(..., example="Head of HR, HR Manager")
    region_location: str = Field(..., example="India")
    product_description: str = Field(..., example="An AI tool that simplifies employee onboarding.")
    target_industry: str = Field(..., example="SaaS, EdTech")
    outreach_goal: str = Field(..., example="Book a discovery call")
    brand_voice: str = Field(..., example="Friendly and direct")

@app.post("/api/start-campaign")
async def start_campaign_endpoint(request: ProspectingRequest):
    campaign_details = request.model_dump()
    print(f"--- Campaign Started ---")
    print(f"Searching for prospects with job role: '{request.ideal_job_roles}' in '{request.region_location}'")

    prospect_urls = search_for_prospects(
        job_title=request.ideal_job_roles,
        location=request.region_location,
        max_results=3
    )

    if not prospect_urls:
        raise HTTPException(status_code=404, detail="Could not find any prospects matching the criteria.")
    
    print(f"Found {len(prospect_urls)} prospects. Now analyzing each profile.")
    
    all_results = []
    for url in prospect_urls:
        print(f"\n--- Processing Profile: {url} ---")
        
        profile_text = get_profile_data(url)
        
        if len(profile_text) < 200:
             print(f"Skipping profile {url} due to insufficient data scraped.")
             continue

        print(f"Successfully scraped profile. Length: {len(profile_text)} chars. Calling AI...")

        try:
            generated_json_str = generate_personalized_message(profile_text, campaign_details)
            generated_data = json.loads(generated_json_str)
            
            generated_data['profile_url'] = url
            all_results.append(generated_data)
            print(f"Successfully generated message for {url}")

        except Exception as e:
            print(f"Skipping profile {url} due to AI generation error: {e}")
            continue

    print(f"\n--- Campaign Finished ---")
    return all_results

@app.get("/")
def read_root():
    return {"status": "LinkedIn Automation API is running!"}