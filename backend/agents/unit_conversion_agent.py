import json
from typing import Dict, Tuple
from urllib import error, request

from backend.agents.tools.conversion_tools import (
    CToFTool,
    CmToInchesTool,
    FToCTool,
    FtToMTool,
    GallonsToLitersTool,
    InchesToCmTool,
    KgToLbsTool,
    KmhToMphTool,
    LbsToKgTool,
    LitersToGallonsTool,
    MToFtTool,
    MphToKmhTool,
)
from backend.models.schemas import ParsedConversion


class UnitConversionAgent:
    def __init__(self, model: str = "llama3.1:latest") -> None:
        self.model = model
        self.ollama_url = "http://localhost:11434/api/generate"
        self.tools: Dict[Tuple[str, str], object] = {
            ("kg", "lbs"): KgToLbsTool(),
            ("lbs", "kg"): LbsToKgTool(),
            ("m", "ft"): MToFtTool(),
            ("ft", "m"): FtToMTool(),
            ("c", "f"): CToFTool(),
            ("f", "c"): FToCTool(),
            ("gallons", "liters"): GallonsToLitersTool(),
            ("liters", "gallons"): LitersToGallonsTool(),
            ("mph", "km/h"): MphToKmhTool(),
            ("km/h", "mph"): KmhToMphTool(),
            ("cm", "inches"): CmToInchesTool(),
            ("inches", "cm"): InchesToCmTool(),
        }

    def convert(self, natural_language_input: str):
        parsed = self._parse_input(natural_language_input)
        key = (parsed.from_unit.strip().lower(), parsed.to_unit.strip().lower())

        tool = self.tools.get(key)
        if not tool:
            raise ValueError(
                f"Unsupported conversion: {parsed.from_unit} -> {parsed.to_unit}"
            )

        result = tool.run(parsed.value)
        return parsed, round(result, 6), tool.name

    def _parse_input(self, natural_language_input: str) -> ParsedConversion:
        prompt = (
            "Extract the original conversion request from the user's text.\n"
            "Do not solve the conversion.\n"
            "Do not calculate anything.\n"
            "Return ONLY valid JSON with exactly these keys:\n"
            '{"value": number, "from_unit": string, "to_unit": string}\n'
            "The value must be the original number written by the user.\n"
            "Allowed units: kg, lbs, m, ft, c, f, gallons, liters, mph, km/h, cm, inches.\n"
            'Example input: "Convert 10 kg to lbs"\n'
            'Example output: {"value": 10, "from_unit": "kg", "to_unit": "lbs"}\n'
            f"User input: {natural_language_input}"
        )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        req = request.Request(
            self.ollama_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=30) as resp:
                raw_response = json.loads(resp.read().decode("utf-8"))
        except (error.URLError, TimeoutError) as exc:
            raise ValueError(f"Unable to reach Ollama API: {exc}") from exc

        model_text = raw_response.get("response", "")
        try:
            parsed_json = json.loads(model_text)
            return ParsedConversion.model_validate(parsed_json)
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError("Failed to parse model output into conversion JSON") from exc