from collections import defaultdict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

EMAIL = "24f2009226@ds.study.iitm.ac.in"
API_KEY = "ak_wxbs0cy00mo96y1far658zil"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analytics")
async def analytics(request: Request):
    if request.headers.get("x-api-key") != API_KEY:
        return JSONResponse(status_code=401, content={"error": "unauthorized"})

    try:
        body = await request.json()
        events = body.get("events", []) if isinstance(body, dict) else []
    except Exception:
        events = []

    users = set()
    totals = defaultdict(float)
    revenue = 0.0
    for e in events:
        if not isinstance(e, dict):
            continue
        user = e.get("user")
        users.add(user)
        try:
            amount = float(e.get("amount", 0))
        except (TypeError, ValueError):
            amount = 0.0
        if amount > 0:
            revenue += amount
            totals[user] += amount

    top_user = max(totals, key=totals.get) if totals else None

    return {
        "email": EMAIL,
        "total_events": len(events),
        "unique_users": len(users),
        "revenue": round(revenue, 6),
        "top_user": top_user,
    }


@app.get("/")
async def root():
    return {"status": "ok"}
