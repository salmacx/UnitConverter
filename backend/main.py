from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.agents.unit_conversion_agent import UnitConversionAgent
from backend.models.schemas import ConvertRequest, ConvertResponse


app = FastAPI(title="Unit Converter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = UnitConversionAgent()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/convert", response_model=ConvertResponse)
def convert(payload: ConvertRequest):
    try:
        parsed, result, tool_name = agent.convert(payload.input)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return ConvertResponse(
        value=parsed.value,
        from_unit=parsed.from_unit,
        to_unit=parsed.to_unit,
        result=result,
        tool=tool_name,
    )