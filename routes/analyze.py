from fastapi import APIRouter, Header, HTTPException
from services.data_collector import collect_data
from services.ai_analyzer import analyze_data
from services.report_generator import generate_report

router = APIRouter()

API_KEY = "mysecret123"

@router.get("/analyze/{sector}")
def analyze_sector(sector: str, x_api_key: str = Header(...)):
    
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    try:
        data = collect_data(sector)
        analysis = analyze_data(sector, data)
        report = generate_report(sector, analysis)

        return {"report": report}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))