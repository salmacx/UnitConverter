from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI(title="Unit Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertRequest(BaseModel):
    value: float = Field(..., description="Numeric value to convert")
    from_unit: str = Field(..., min_length=1)
    to_unit: str = Field(..., min_length=1)


class ConvertResponse(BaseModel):
    value: float
    from_unit: str
    to_unit: str
    result: float
    tool: str
    error: Optional[str] = None


SUPPORTED = {
    ("kg", "lbs"): ("kg_to_lbs", 2.2046226218),
    ("lbs", "kg"): ("lbs_to_kg", 1 / 2.2046226218),
    ("m", "ft"): ("m_to_ft", 3.280839895),
    ("ft", "m"): ("ft_to_m", 1 / 3.280839895),
    ("C", "F"): ("c_to_f", None),
    ("F", "C"): ("f_to_c", None),
    ("gallons", "liters"): ("gal_to_l", 3.785411784),
    ("liters", "gallons"): ("l_to_gal", 1 / 3.785411784),
    ("mph", "km/h"): ("mph_to_kmh", 1.609344),
    ("km/h", "mph"): ("kmh_to_mph", 1 / 1.609344),
    ("cm", "inches"): ("cm_to_in", 0.3937007874),
    ("inches", "cm"): ("in_to_cm", 1 / 0.3937007874),
}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/convert", response_model=ConvertResponse)
def convert(payload: ConvertRequest):
    value = payload.value
    from_u = payload.from_unit.strip()
    to_u = payload.to_unit.strip()

    key = (from_u, to_u)
    if key not in SUPPORTED:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported conversion: {from_u} -> {to_u}",
        )

    tool, factor = SUPPORTED[key]

    if from_u == "C" and to_u == "F":
        result = (value * 9 / 5) + 32
    elif from_u == "F" and to_u == "C":
        result = (value - 32) * 5 / 9
    else:
        result = value * factor

    return ConvertResponse(
        value=value,
        from_unit=from_u,
        to_unit=to_u,
        result=round(result, 6),
        tool=tool,
    )