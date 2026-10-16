import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from scraper import scrape_linkedin, scrape_instagram
from agent_engine import analyze_person, simulate_date

app = FastAPI(title="agentic dating api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProfileInput(BaseModel):
    linkedin_url: str
    instagram_url: str

class DateInput(BaseModel):
    agent_a: dict
    agent_b: dict

@app.get("/")
def health_check():
    return {"status": "ok", "service": "agentic dating engine"}

@app.post("/analyze")
async def handle_analyze(data: ProfileInput):
    try:
        li_data = await scrape_linkedin(data.linkedin_url)
        ig_data = await scrape_instagram(data.instagram_url)
        analysis = await analyze_person(li_data, ig_data)
        return {"status": "success", "profile": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/date")
async def handle_date(data: DateInput):
    try:
        match_result = await simulate_date(data.agent_a, data.agent_b)
        return {"status": "success", "result": match_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
