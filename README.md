# Luminaires API – Δήμος Πάργας

FastAPI service exposing geolocation and real-time status for 133 street luminaires in Parga.

**Active schedule: 20:00–06:00 UTC | Inactive: 06:00–20:00 UTC**

---

## Setup

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Interactive docs: `http://localhost:8000/docs`

---

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Health check + current network status |
| `GET` | `/status` | Current active/inactive status + schedule info |
| `GET` | `/luminaires` | All 133 luminaires with geolocation & status |
| `GET` | `/luminaires?status=active` | Filter to active only |
| `GET` | `/luminaires?status=inactive` | Filter to inactive only |
| `GET` | `/luminaires/{mac}` | Single luminaire by MAC address |
| `GET` | `/luminaires/geojson/all` | GeoJSON FeatureCollection (for maps) |

---

## Example responses

### `GET /luminaires`
```json
{
  "utc_time": "2024-11-20T21:00:00Z",
  "current_status": "active",
  "count": 133,
  "luminaires": [
    {
      "mac": "00124B001CE32611",
      "latitude": 39.227253,
      "longitude": 20.57436,
      "wattage": 40,
      "status": "active",
      "schedule": "20:00–06:00 UTC"
    }
  ]
}
```

### `GET /luminaires/geojson/all`
Returns a standard GeoJSON FeatureCollection ready to use in:
- Leaflet.js maps
- QGIS
- Google Maps
- ArcGIS

---

## Deploy to Railway

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/luminaires-api.git
git push -u origin main
```

Then on [railway.app](https://railway.app): New Project → Deploy from GitHub → Generate Domain.

---

## Notes

- Status is computed dynamically from UTC time on every request — no cron jobs needed.
- One luminaire (`00124B001CE32552`) has no latitude recorded in the source data and is excluded from the GeoJSON output but included in all other endpoints.
- To add persistent fault tracking or dimming levels, swap the static `LUMINAIRES` list for a database layer.
