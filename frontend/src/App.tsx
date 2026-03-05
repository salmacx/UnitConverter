import { useMemo, useState } from "react";
import "./App.css";

type Conversion = {
  id: string;
  label: string;
  desc: string;
  from: string;
  to: string;
};

type ApiResponse = {
  value?: number;
  from_unit?: string;
  to_unit?: string;
  result?: number;
  tool?: string;
  error?: string;
};

const BACKEND_URL = "http://localhost:8000";

export default function App() {
  const conversions: Conversion[] = useMemo(
    () => [
      { id: "kg_lbs", label: "kg → lbs", desc: "Kilograms to Pounds", from: "kg", to: "lbs" },
      { id: "lbs_kg", label: "lbs → kg", desc: "Pounds to Kilograms", from: "lbs", to: "kg" },

      { id: "m_ft", label: "m → ft", desc: "Meters to Feet", from: "m", to: "ft" },
      { id: "ft_m", label: "ft → m", desc: "Feet to Meters", from: "ft", to: "m" },

      { id: "c_f", label: "°C → °F", desc: "Celsius to Fahrenheit", from: "C", to: "F" },
      { id: "f_c", label: "°F → °C", desc: "Fahrenheit to Celsius", from: "F", to: "C" },

      { id: "gal_l", label: "gal → L", desc: "Gallons to Liters", from: "gallons", to: "liters" },
      { id: "l_gal", label: "L → gal", desc: "Liters to Gallons", from: "liters", to: "gallons" },

      { id: "mph_kmh", label: "mph → km/h", desc: "Miles/hour to Km/hour", from: "mph", to: "km/h" },
      { id: "kmh_mph", label: "km/h → mph", desc: "Km/hour to Miles/hour", from: "km/h", to: "mph" },

      { id: "cm_in", label: "cm → inches", desc: "Centimeters to Inches", from: "cm", to: "inches" },
      { id: "in_cm", label: "inches → cm", desc: "Inches to Centimeters", from: "inches", to: "cm" },
    ],
    []
  );

  const [selectedId, setSelectedId] = useState<string>("kg_lbs");
  const selected = conversions.find((c) => c.id === selectedId)!;

  const [valueText, setValueText] = useState<string>("10");
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<ApiResponse | null>(null);

  const valueNumber = Number(valueText);
  const valueValid = valueText.trim() !== "" && Number.isFinite(valueNumber);

  async function handleConvert() {
    if (!valueValid) {
      setData({ error: "Please enter a valid number." });
      return;
    }

    setLoading(true);
    setData(null);

    try {
      const res = await fetch(`${BACKEND_URL}/convert`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          value: valueNumber,
          from_unit: selected.from,
          to_unit: selected.to,
        }),
      });

      const json = (await res.json()) as ApiResponse;

      if (!res.ok && !json.error) {
        json.error = `Request failed (${res.status})`;
      }

      setData(json);
    } catch {
      setData({ error: "Could not reach backend. Is it running on localhost:8000?" });
    } finally {
      setLoading(false);
    }
  }

  function handleClear() {
    setValueText("");
    setData(null);
  }

  const rows: string[][] = useMemo(
    () => [
      ["kg_lbs", "lbs_kg"],
      ["m_ft", "ft_m"],
      ["c_f", "f_c"],
      ["gal_l", "l_gal"],
      ["mph_kmh", "kmh_mph"],
      ["cm_in", "in_cm"],
    ],
    []
  );

  return (
    <div className="page">
      <div className="container">
        <h1>Conversion Calculator</h1>
        <p className="subtitle">Choose a conversion, then enter a value.</p>

        <div className="grid">
          {/* LEFT: request + result */}
          <div className="leftCol">
            <div className="card">
              <h3>Conversion request</h3>

              <div className="selectedBadge">
                <b>{selected.label}</b>
                <span className="muted">({selected.desc})</span>
              </div>

              <input
                className="input"
                value={valueText}
                onChange={(e) => setValueText(e.target.value)}
                placeholder="Enter value (e.g. 10)"
                inputMode="decimal"
                onKeyDown={(e) => {
                  if (e.key === "Enter") handleConvert();
                }}
              />

              <div className="btnRow">
                <button
                  className="btn primary"
                  onClick={handleConvert}
                  disabled={loading || !valueValid}
                >
                  {loading ? "Converting..." : "Convert"}
                </button>

                <button className="btn" onClick={handleClear} disabled={loading}>
                  Clear
                </button>
              </div>

              <div className="resultBox">
                <h4 className="resultTitle">Result</h4>

                {data?.error && <div className="error">{data.error}</div>}

                {!data && !loading && <p className="muted">Result will appear here.</p>}

                {loading && <p className="muted">Working…</p>}

                {data && !data.error && (
                  <>
                    <div className="resultBig">
                      {(data.value ?? valueNumber).toString()}{" "}
                      {data.from_unit ?? selected.from} →{" "}
                      {(data.result ?? "?").toString()} {data.to_unit ?? selected.to}
                    </div>

                    {data.tool && <p className="muted">Tool used: {data.tool}</p>}
                  </>
                )}
              </div>
            </div>
          </div>

          {/* RIGHT: supported conversions */}
          <div className="rightCol">
            <div className="card">
              <h3>Supported conversions</h3>

              <div className="pairs">
                {rows.map((row, idx) => (
                  <div className="pairRow" key={idx}>
                    {row.map((id) => {
                      const c = conversions.find((x) => x.id === id)!;
                      return (
                        <button
                          key={c.id}
                          className={`chip ${c.id === selectedId ? "chipActive" : ""}`}
                          onClick={() => setSelectedId(c.id)}
                        >
                          {c.label}
                        </button>
                      );
                    })}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}