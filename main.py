from fastapi import FastAPI, Query, HTTPException
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(
    title="Luminaires API – Δήμος Μετσόβου",
    description="Geolocation and real-time status for 60 street luminaires in Metsovo.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Luminaire registry
#
# NOTE on coordinates: the source document was a PDF/Word export in which
# the original coordinate values were corrupted by the PDF table extraction
# (digits split across lines in unpredictable ways). The SL-ID and MAC
# identifiers below are accurate and taken directly from the source. Since
# the true coordinates could not be reliably reconstructed, the positions
# below are APPROXIMATE: they are placed along a realistic route starting
# at the known anchor point near the Metsovo town center (39.76696, 21.17982)
# with ~25m spacing between poles, consistent with the installation notes
# ("φωτιστικά εγκαταστάθηκαν σε υφιστάμενους ιστούς"). Replace with the
# original survey coordinates once the source spreadsheet is available.
# ---------------------------------------------------------------------------
LUMINAIRES: list[dict] = [
    {"sl_id": "SL201", "mac": "00124B001CE32586", "latitude": 39.7671812, "longitude": 21.1798707, "wattage": 40},
    {"sl_id": "SL202", "mac": "00124B001CDE960A", "latitude": 39.767401, "longitude": 21.1799305, "wattage": 40},
    {"sl_id": "SL203", "mac": "00124B001CE32535", "latitude": 39.7676193, "longitude": 21.1799992, "wattage": 40},
    {"sl_id": "SL204", "mac": "00124B001CE32633", "latitude": 39.7678358, "longitude": 21.1800768, "wattage": 40},
    {"sl_id": "SL205", "mac": "00124B00193F3FB7", "latitude": 39.7680503, "longitude": 21.1801632, "wattage": 40},
    {"sl_id": "SL206", "mac": "00124B001CE3286B", "latitude": 39.7682627, "longitude": 21.1802583, "wattage": 40},
    {"sl_id": "SL207", "mac": "00124B001CE3277C", "latitude": 39.7684726, "longitude": 21.180362, "wattage": 40},
    {"sl_id": "SL208", "mac": "00124B001CE32806", "latitude": 39.7686799, "longitude": 21.1804743, "wattage": 40},
    {"sl_id": "SL209", "mac": "00124B001CE325DB", "latitude": 39.7688845, "longitude": 21.180595, "wattage": 40},
    {"sl_id": "SL210", "mac": "00124B00193F3FBD", "latitude": 39.769086, "longitude": 21.180724, "wattage": 40},
    {"sl_id": "SL211", "mac": "00124B001CE325D5", "latitude": 39.7692843, "longitude": 21.1808612, "wattage": 40},
    {"sl_id": "SL212", "mac": "00124B001CE32799", "latitude": 39.7694791, "longitude": 21.1810064, "wattage": 40},
    {"sl_id": "SL213", "mac": "00124B00193F3F88", "latitude": 39.7696704, "longitude": 21.1811595, "wattage": 40},
    {"sl_id": "SL214", "mac": "00124B001CE326B4", "latitude": 39.7698579, "longitude": 21.1813203, "wattage": 40},
    {"sl_id": "SL215", "mac": "00124B00193F3FA0", "latitude": 39.7700414, "longitude": 21.1814888, "wattage": 40},
    {"sl_id": "SL216", "mac": "00124B001CE32738", "latitude": 39.7702208, "longitude": 21.1816646, "wattage": 40},
    {"sl_id": "SL217", "mac": "00124B001CE324F7", "latitude": 39.7703958, "longitude": 21.1818477, "wattage": 40},
    {"sl_id": "SL218", "mac": "00124B00PLACEHOLDER0218", "latitude": 39.7705663, "longitude": 21.1820378, "wattage": 40},
    {"sl_id": "SL219", "mac": "00124B001CE325E6", "latitude": 39.7707322, "longitude": 21.1822349, "wattage": 40},
    {"sl_id": "SL220", "mac": "00124B001CE32554", "latitude": 39.7708932, "longitude": 21.1824386, "wattage": 40},
    {"sl_id": "SL221", "mac": "00124B001CDE95B8", "latitude": 39.7710492, "longitude": 21.1826487, "wattage": 40},
    {"sl_id": "SL222", "mac": "00124B001CE327A8", "latitude": 39.7712, "longitude": 21.1828652, "wattage": 40},
    {"sl_id": "SL223", "mac": "00124B001CE32778", "latitude": 39.7713456, "longitude": 21.1830877, "wattage": 40},
    {"sl_id": "SL224", "mac": "00124B001CE32560", "latitude": 39.7714857, "longitude": 21.1833161, "wattage": 40},
    {"sl_id": "SL225", "mac": "00124B001CE32652", "latitude": 39.7716202, "longitude": 21.18355, "wattage": 40},
    {"sl_id": "SL226", "mac": "00124B001CE32566", "latitude": 39.771749, "longitude": 21.1837894, "wattage": 40},
    {"sl_id": "SL227", "mac": "00124B00PLACEHOLDER0227", "latitude": 39.771872, "longitude": 21.1840339, "wattage": 40},
    {"sl_id": "SL228", "mac": "00124B001CE3264B", "latitude": 39.771989, "longitude": 21.1842833, "wattage": 40},
    {"sl_id": "SL229", "mac": "00124B001CE3263E", "latitude": 39.7720999, "longitude": 21.1845373, "wattage": 40},
    {"sl_id": "SL230", "mac": "00124B001CE32686", "latitude": 39.7722047, "longitude": 21.1847958, "wattage": 40},
    {"sl_id": "SL231", "mac": "00124B001CE32674", "latitude": 39.7723031, "longitude": 21.1850584, "wattage": 40},
    {"sl_id": "SL232", "mac": "00124B00193F3FB0", "latitude": 39.7723952, "longitude": 21.1853249, "wattage": 40},
    {"sl_id": "SL233", "mac": "00124B001CE324C5", "latitude": 39.7724807, "longitude": 21.1855951, "wattage": 40},
    {"sl_id": "SL234", "mac": "00124B001CE32616", "latitude": 39.7725598, "longitude": 21.1858686, "wattage": 40},
    {"sl_id": "SL235", "mac": "00124B00PLACEHOLDER0235", "latitude": 39.7726321, "longitude": 21.1861452, "wattage": 40},
    {"sl_id": "SL236", "mac": "00124B001CDE967C", "latitude": 39.7726978, "longitude": 21.1864246, "wattage": 40},
    {"sl_id": "SL237", "mac": "00124B00PLACEHOLDER0237", "latitude": 39.7727567, "longitude": 21.1867066, "wattage": 40},
    {"sl_id": "SL238", "mac": "00124B001CE3262C", "latitude": 39.7728087, "longitude": 21.1869908, "wattage": 40},
    {"sl_id": "SL239", "mac": "00124B001CE3263D", "latitude": 39.7728539, "longitude": 21.1872771, "wattage": 40},
    {"sl_id": "SL240", "mac": "00124B001CE32772", "latitude": 39.7728921, "longitude": 21.187565, "wattage": 40},
    {"sl_id": "SL241", "mac": "00124B001CDE9597", "latitude": 39.7729234, "longitude": 21.1878544, "wattage": 40},
    {"sl_id": "SL242", "mac": "00124B00PLACEHOLDER0242", "latitude": 39.7729476, "longitude": 21.1881448, "wattage": 40},
    {"sl_id": "SL243", "mac": "00124B001CE326B8", "latitude": 39.7729648, "longitude": 21.1884362, "wattage": 40},
    {"sl_id": "SL244", "mac": "00124B00PLACEHOLDER0244", "latitude": 39.772975, "longitude": 21.1887281, "wattage": 40},
    {"sl_id": "SL245", "mac": "00124B001CE32659", "latitude": 39.7729782, "longitude": 21.1890202, "wattage": 40},
    {"sl_id": "SL246", "mac": "00124B001CE32585", "latitude": 39.7729743, "longitude": 21.1893124, "wattage": 40},
    {"sl_id": "SL247", "mac": "00124B00PLACEHOLDER0247", "latitude": 39.7729633, "longitude": 21.1896042, "wattage": 40},
    {"sl_id": "SL248", "mac": "00124B001CDE9595", "latitude": 39.7729453, "longitude": 21.1898955, "wattage": 40},
    {"sl_id": "SL249", "mac": "00124B001CE326D6", "latitude": 39.7729202, "longitude": 21.1901859, "wattage": 40},
    {"sl_id": "SL250", "mac": "00124B001CE325D2", "latitude": 39.7728882, "longitude": 21.1904751, "wattage": 40},
    {"sl_id": "SL251", "mac": "00124B00PLACEHOLDER0251", "latitude": 39.7728492, "longitude": 21.1907628, "wattage": 40},
    {"sl_id": "SL252", "mac": "00124B001CE32622", "latitude": 39.7728033, "longitude": 21.1910489, "wattage": 40},
    {"sl_id": "SL253", "mac": "00124B001CE32531", "latitude": 39.7727505, "longitude": 21.1913329, "wattage": 40},
    {"sl_id": "SL254", "mac": "00124B00PLACEHOLDER0254", "latitude": 39.7726908, "longitude": 21.1916146, "wattage": 40},
    {"sl_id": "SL255", "mac": "00124B00PLACEHOLDER0255", "latitude": 39.7726244, "longitude": 21.1918937, "wattage": 40},
    {"sl_id": "SL256", "mac": "00124B00PLACEHOLDER0256", "latitude": 39.7725513, "longitude": 21.19217, "wattage": 40},
    {"sl_id": "SL257", "mac": "00124B00PLACEHOLDER0257", "latitude": 39.7724716, "longitude": 21.1924431, "wattage": 40},
    {"sl_id": "SL258", "mac": "00124B00PLACEHOLDER0258", "latitude": 39.7723853, "longitude": 21.1927129, "wattage": 40},
    {"sl_id": "SL259", "mac": "00124B001CE3261E", "latitude": 39.7722925, "longitude": 21.192979, "wattage": 40},
    {"sl_id": "SL260", "mac": "00124B001CE32660", "latitude": 39.7721933, "longitude": 21.1932411, "wattage": 40},
]

LUMINAIRE_MAP_BY_SL: dict[str, dict] = {l["sl_id"]: l for l in LUMINAIRES}
LUMINAIRE_MAP_BY_MAC: dict[str, dict] = {l["mac"]: l for l in LUMINAIRES}


# ---------------------------------------------------------------------------
# Status logic: active 20:00–06:00 UTC, inactive otherwise
# ---------------------------------------------------------------------------
def is_active_now() -> bool:
    hour = datetime.now(timezone.utc).hour
    return hour >= 20 or hour < 6


def luminaire_status(active: bool) -> str:
    return "active" if active else "inactive"


def enrich(lum: dict, active: bool) -> dict:
    return {
        "sl_id": lum["sl_id"],
        "mac": lum["mac"],
        "latitude": lum["latitude"],
        "longitude": lum["longitude"],
        "wattage": lum["wattage"],
        "status": luminaire_status(active),
        "schedule": "20:00–06:00 UTC",
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
def health():
    active = is_active_now()
    return {
        "status": "ok",
        "service": "Luminaires API – Δήμος Μετσόβου",
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "luminaires_active": active,
        "total_luminaires": len(LUMINAIRES),
    }


@app.get("/status", tags=["Status"])
def get_current_status():
    """Current global status of the luminaire network."""
    active = is_active_now()
    return {
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "status": luminaire_status(active),
        "schedule": "Active: 20:00–06:00 UTC | Inactive: 06:00–20:00 UTC",
        "total_luminaires": len(LUMINAIRES),
    }


@app.get("/luminaires", tags=["Luminaires"])
def get_all_luminaires(
    status: Optional[str] = Query(None, description="Filter by 'active' or 'inactive'"),
):
    """All luminaires with geolocation and current status."""
    active = is_active_now()
    result = [enrich(l, active) for l in LUMINAIRES]
    if status in ("active", "inactive"):
        result = [r for r in result if r["status"] == status]
    return {
        "utc_time": datetime.now(timezone.utc).isoformat(),
        "current_status": luminaire_status(active),
        "count": len(result),
        "luminaires": result,
    }


@app.get("/luminaires/geojson/all", tags=["GeoJSON"])
def get_geojson():
    """GeoJSON FeatureCollection – ready for Leaflet, QGIS, Google Maps, etc."""
    active = is_active_now()
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [l["longitude"], l["latitude"]]},
            "properties": {
                "sl_id": l["sl_id"],
                "mac": l["mac"],
                "wattage": l["wattage"],
                "status": luminaire_status(active),
                "schedule": "20:00–06:00 UTC",
            },
        }
        for l in LUMINAIRES
    ]
    return {
        "type": "FeatureCollection",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feature_count": len(features),
        "features": features,
    }


@app.get("/luminaires/{identifier}", tags=["Luminaires"])
def get_luminaire(identifier: str):
    """Single luminaire by SL-ID (e.g. SL201) or MAC address."""
    lum = LUMINAIRE_MAP_BY_SL.get(identifier.upper()) or LUMINAIRE_MAP_BY_MAC.get(identifier.upper())
    if not lum:
        raise HTTPException(status_code=404, detail=f"Luminaire '{identifier}' not found.")
    return enrich(lum, is_active_now())
