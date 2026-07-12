from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime, timezone

app = FastAPI(
    title="Luminaires API – Δήμος Πάργας",
    description="Real-time status and geolocation for 133 street luminaires in Parga.",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Luminaire registry – all 133 LCU devices from the asset list
# ---------------------------------------------------------------------------
LUMINAIRES: list[dict] = [
    {"sl_id": "PA001", "mac": "00124B001CE32611", "latitude": 39.227253, "longitude": 20.57436, "wattage": 40},
    {"sl_id": "PA002", "mac": "00124B001CE326F5", "latitude": 39.2268944, "longitude": 20.5740986, "wattage": 40},
    {"sl_id": "PA003", "mac": "00124B001CE3274D", "latitude": 39.2270432, "longitude": 20.5743122, "wattage": 40},
    {"sl_id": "PA004", "mac": "00124B001CE32732", "latitude": 39.226696, "longitude": 20.5739, "wattage": 40},
    {"sl_id": "PA005", "mac": "00124B001CE32613", "latitude": 39.22639, "longitude": 20.5734329, "wattage": 40},
    {"sl_id": "PA006", "mac": "00124B001CE32603", "latitude": 39.2264938, "longitude": 20.57367, "wattage": 40},
    {"sl_id": "PA007", "mac": "00124B001CE32602", "latitude": 39.2261848, "longitude": 20.57309, "wattage": 40},
    {"sl_id": "PA008", "mac": "00124B001CE3269F", "latitude": 39.2262535, "longitude": 20.5733433, "wattage": 40},
    {"sl_id": "PA009", "mac": "00124B001CE326C0", "latitude": 39.2266579, "longitude": 20.57409, "wattage": 40},
    {"sl_id": "PA010", "mac": "00124B001CE3262D", "latitude": 39.2264481, "longitude": 20.57373, "wattage": 40},
    {"sl_id": "PA011", "mac": "00124B001CE32689", "latitude": 39.2268448, "longitude": 20.5744267, "wattage": 40},
    {"sl_id": "PA012", "mac": "00124B001CDE9598", "latitude": 39.22671, "longitude": 20.5746574, "wattage": 40},
    {"sl_id": "PA013", "mac": "00124B001CE325D7", "latitude": 39.22665, "longitude": 20.57473, "wattage": 40},
    {"sl_id": "PA014", "mac": "00124B001CE32631", "latitude": 39.2257652, "longitude": 20.57481, "wattage": 40},
    {"sl_id": "PA015", "mac": "00124B001CE32701", "latitude": 39.22599, "longitude": 20.5747261, "wattage": 40},
    {"sl_id": "PA016", "mac": "00124B001CE3275C", "latitude": 39.2262955, "longitude": 20.5747337, "wattage": 40},
    {"sl_id": "PA017", "mac": "00124B001CE32681", "latitude": 39.2266235, "longitude": 20.57482, "wattage": 40},
    {"sl_id": "PA018", "mac": "00124B001CDE9605", "latitude": 39.2268524, "longitude": 20.5747051, "wattage": 40},
    {"sl_id": "PA019", "mac": "00124B001CDE9673", "latitude": 39.2269974, "longitude": 20.574564, "wattage": 40},
    {"sl_id": "PA020", "mac": "00124B001CE32572", "latitude": 39.22709, "longitude": 20.5744762, "wattage": 40},
    {"sl_id": "PA021", "mac": "00124B001CDE9672", "latitude": 39.22743, "longitude": 20.5745811, "wattage": 40},
    {"sl_id": "PA022", "mac": "00124B001CDE95AB", "latitude": 39.22772, "longitude": 20.5746326, "wattage": 40},
    {"sl_id": "PA023", "mac": "00124B001CDE960D", "latitude": 39.2280579, "longitude": 20.5745773, "wattage": 40},
    {"sl_id": "PA024", "mac": "00124B001CDE965C", "latitude": 39.2282562, "longitude": 20.5745716, "wattage": 40},
    {"sl_id": "PA025", "mac": "00124B001CDE9599", "latitude": 39.2284431, "longitude": 20.5745182, "wattage": 40},
    {"sl_id": "PA026", "mac": "00124B001CE325E7", "latitude": 39.22916, "longitude": 20.574419, "wattage": 40},
    {"sl_id": "PA027", "mac": "00124B001CE325BD", "latitude": 39.2289467, "longitude": 20.57442, "wattage": 40},
    {"sl_id": "PA028", "mac": "00124B001CE3277A", "latitude": 39.2286568, "longitude": 20.5744476, "wattage": 40},
    {"sl_id": "PA029", "mac": "00124B001CE326AC", "latitude": 39.22856, "longitude": 20.57441, "wattage": 40},
    {"sl_id": "PA030", "mac": "00124B001CE32591", "latitude": 39.2282181, "longitude": 20.5744762, "wattage": 40},
    {"sl_id": "PA031", "mac": "00124B001CE326A3", "latitude": 39.2280235, "longitude": 20.5744743, "wattage": 40},
    {"sl_id": "PA032", "mac": "00124B001CE325B2", "latitude": 39.2277, "longitude": 20.5744324, "wattage": 40},
    {"sl_id": "PA033", "mac": "00124B001CE327E9", "latitude": 39.2274323, "longitude": 20.57442, "wattage": 40},
    {"sl_id": "PA034", "mac": "00124B001CE325AF", "latitude": 39.24092, "longitude": 20.5864658, "wattage": 40},
    {"sl_id": "PA035", "mac": "00124B001CDE964C", "latitude": 39.24034, "longitude": 20.5857277, "wattage": 40},
    {"sl_id": "PA036", "mac": "00124B001CE326BF", "latitude": 39.24053, "longitude": 20.585783, "wattage": 40},
    {"sl_id": "PA037", "mac": "00124B001CE3267C", "latitude": 39.2405434, "longitude": 20.5855961, "wattage": 40},
    {"sl_id": "PA038", "mac": "00124B001CE32755", "latitude": 39.2406731, "longitude": 20.5856819, "wattage": 40},
    {"sl_id": "PA039", "mac": "00124B001CE32786", "latitude": 39.2404022, "longitude": 20.5856247, "wattage": 40},
    {"sl_id": "PA040", "mac": "00124B001CE3276F", "latitude": 39.2403259, "longitude": 20.5856018, "wattage": 40},
    {"sl_id": "PA041", "mac": "00124B001CE32662", "latitude": 39.2398834, "longitude": 20.5843754, "wattage": 40},
    {"sl_id": "PA042", "mac": "00124B001CE326C1", "latitude": 39.2397461, "longitude": 20.5841484, "wattage": 40},
    {"sl_id": "PA043", "mac": "00124B001CE326EA", "latitude": 39.23959, "longitude": 20.5838642, "wattage": 40},
    {"sl_id": "PA044", "mac": "00124B001CE325E5", "latitude": 39.23945, "longitude": 20.5835781, "wattage": 40},
    {"sl_id": "PA045", "mac": "00124B001CE32596", "latitude": 39.239315, "longitude": 20.5832138, "wattage": 40},
    {"sl_id": "PA046", "mac": "00124B001CE326BC", "latitude": 39.2391472, "longitude": 20.5829811, "wattage": 40},
    {"sl_id": "PA047", "mac": "00124B001CE32669", "latitude": 39.2391434, "longitude": 20.582613, "wattage": 40},
    {"sl_id": "PA048", "mac": "00124B001CE324FF", "latitude": 39.238884, "longitude": 20.5823727, "wattage": 40},
    {"sl_id": "PA049", "mac": "00124B001CE3265B", "latitude": 39.23872, "longitude": 20.5820751, "wattage": 40},
    {"sl_id": "PA050", "mac": "00124B001CE32523", "latitude": 39.23851, "longitude": 20.5817966, "wattage": 40},
    {"sl_id": "PA051", "mac": "00124B001CE326AA", "latitude": 39.2383766, "longitude": 20.58151, "wattage": 40},
    {"sl_id": "PA052", "mac": "00124B001CE3266A", "latitude": 39.2383, "longitude": 20.5812569, "wattage": 40},
    {"sl_id": "PA053", "mac": "00124B001CE3268E", "latitude": 39.2380676, "longitude": 20.5808525, "wattage": 40},
    {"sl_id": "PA054", "mac": "00124B001CE2DB9A", "latitude": 39.237957, "longitude": 20.5806389, "wattage": 40},
    {"sl_id": "PA055", "mac": "00124B001CE32621", "latitude": 39.2379, "longitude": 20.5803757, "wattage": 40},
    {"sl_id": "PA056", "mac": "00124B001CE327DF", "latitude": 39.237812, "longitude": 20.5800686, "wattage": 40},
    {"sl_id": "PA057", "mac": "00124B001CE32780", "latitude": 39.2376671, "longitude": 20.5796432, "wattage": 40},
    {"sl_id": "PA058", "mac": "00124B001CE326C4", "latitude": 39.2376442, "longitude": 20.57935, "wattage": 40},
    {"sl_id": "PA059", "mac": "00124B001CE3271B", "latitude": 39.23748, "longitude": 20.5790272, "wattage": 40},
    {"sl_id": "PA060", "mac": "00124B001CE3269C", "latitude": 39.2375259, "longitude": 20.5786724, "wattage": 40},
    {"sl_id": "PA061", "mac": "00124B001CE326FE", "latitude": 39.23737, "longitude": 20.5783653, "wattage": 40},
    {"sl_id": "PA062", "mac": "00124B001CE32771", "latitude": 39.23727, "longitude": 20.578022, "wattage": 40},
    {"sl_id": "PA063", "mac": "00124B001CE3268D", "latitude": 39.2371521, "longitude": 20.5776844, "wattage": 40},
    {"sl_id": "PA064", "mac": "00124B001CE32619", "latitude": 39.23716, "longitude": 20.5773525, "wattage": 40},
    {"sl_id": "PA065", "mac": "00124B001CE32856", "latitude": 39.236927, "longitude": 20.5770569, "wattage": 40},
    {"sl_id": "PA066", "mac": "00124B001CE326CA", "latitude": 39.2369232, "longitude": 20.5767174, "wattage": 40},
    {"sl_id": "PA067", "mac": "00124B001CE327EF", "latitude": 39.23687, "longitude": 20.5764446, "wattage": 40},
    {"sl_id": "PA068", "mac": "00124B001CE32729", "latitude": 39.23677, "longitude": 20.5761032, "wattage": 40},
    {"sl_id": "PA069", "mac": "00124B001CE324B7", "latitude": 39.2366867, "longitude": 20.575737, "wattage": 40},
    {"sl_id": "PA070", "mac": "00124B001CE326AE", "latitude": 39.2365952, "longitude": 20.5753326, "wattage": 40},
    {"sl_id": "PA071", "mac": "00124B001CE32688", "latitude": 39.2364769, "longitude": 20.57504, "wattage": 40},
    {"sl_id": "PA072", "mac": "00124B001CE325BA", "latitude": 39.23638, "longitude": 20.574749, "wattage": 40},
    {"sl_id": "PA073", "mac": "00124B001CE326E2", "latitude": 39.2362328, "longitude": 20.5743618, "wattage": 40},
    {"sl_id": "PA074", "mac": "00124B001CE325F6", "latitude": 39.23612, "longitude": 20.5741253, "wattage": 40},
    {"sl_id": "PA075", "mac": "00124B001CE32746", "latitude": 39.2361031, "longitude": 20.5739269, "wattage": 40},
    {"sl_id": "PA076", "mac": "00124B001CE32739", "latitude": 39.2356758, "longitude": 20.57344, "wattage": 40},
    {"sl_id": "PA077", "mac": "00124B00193F3FA5", "latitude": 39.2354355, "longitude": 20.573204, "wattage": 40},
    {"sl_id": "PA078", "mac": "00124B001CE32628", "latitude": 39.2352753, "longitude": 20.5729885, "wattage": 40},
    {"sl_id": "PA079", "mac": "00124B001CE3259D", "latitude": 39.2350121, "longitude": 20.5727959, "wattage": 40},
    {"sl_id": "PA080", "mac": "00124B001CE326C6", "latitude": 39.23469, "longitude": 20.5727272, "wattage": 40},
    {"sl_id": "PA081", "mac": "00124B001CE3254D", "latitude": 39.2344933, "longitude": 20.5725746, "wattage": 40},
    {"sl_id": "PA082", "mac": "00124B001CDE9644", "latitude": 39.2343178, "longitude": 20.5725346, "wattage": 40},
    {"sl_id": "PA083", "mac": "00124B001CE3264E", "latitude": 39.2337151, "longitude": 20.5724125, "wattage": 40},
    {"sl_id": "PA084", "mac": "00124B001CE3268B", "latitude": 39.2334633, "longitude": 20.5724735, "wattage": 40},
    {"sl_id": "PA085", "mac": "00124B001CE325AD", "latitude": 39.23315, "longitude": 20.5725212, "wattage": 40},
    {"sl_id": "PA086", "mac": "00124B001CE3264F", "latitude": 39.2417221, "longitude": 20.58653, "wattage": 40},
    {"sl_id": "PA087", "mac": "00124B001CE325A2", "latitude": 39.2418671, "longitude": 20.58622, "wattage": 40},
    {"sl_id": "PA088", "mac": "00124B001CE3254A", "latitude": 39.2420921, "longitude": 20.5857754, "wattage": 40},
    {"sl_id": "PA089", "mac": "00124B001CE324E4", "latitude": 39.24227, "longitude": 20.5853672, "wattage": 40},
    {"sl_id": "PA090", "mac": "00124B001CDE95E5", "latitude": 39.24241, "longitude": 20.5849438, "wattage": 40},
    {"sl_id": "PA091", "mac": "00124B001CE32601", "latitude": 39.24265, "longitude": 20.5845966, "wattage": 40},
    {"sl_id": "PA092", "mac": "00124B001CE324CF", "latitude": 39.24275, "longitude": 20.5843468, "wattage": 40},
    {"sl_id": "PA093", "mac": "00124B001CE32487", "latitude": 39.2429161, "longitude": 20.5839214, "wattage": 40},
    {"sl_id": "PA094", "mac": "00124B001CDE95A7", "latitude": 39.24308, "longitude": 20.5835686, "wattage": 40},
    {"sl_id": "PA095", "mac": "00124B001CE3263A", "latitude": 39.2432022, "longitude": 20.5832024, "wattage": 40},
    {"sl_id": "PA096", "mac": "00124B001CE326C2", "latitude": 39.2433434, "longitude": 20.5828743, "wattage": 40},
    {"sl_id": "PA097", "mac": "00124B001CE32717", "latitude": 39.24348, "longitude": 20.5825081, "wattage": 40},
    {"sl_id": "PA098", "mac": "00124B001CE32752", "latitude": 39.2436676, "longitude": 20.58217, "wattage": 40},
    {"sl_id": "PA099", "mac": "00124B001CE325CA", "latitude": 39.24379, "longitude": 20.5818787, "wattage": 40},
    {"sl_id": "PA100", "mac": "00124B001CE32651", "latitude": 39.24396, "longitude": 20.5815258, "wattage": 40},
    {"sl_id": "PA101", "mac": "00124B001CE32513", "latitude": 39.24402, "longitude": 20.5811749, "wattage": 40},
    {"sl_id": "PA102", "mac": "00124B001CDE95D3", "latitude": 39.2442055, "longitude": 20.58091, "wattage": 40},
    {"sl_id": "PA103", "mac": "00124B001CE3258B", "latitude": 39.2420654, "longitude": 20.5879536, "wattage": 40},
    {"sl_id": "PA104", "mac": "00124B001CE3277F", "latitude": 39.242, "longitude": 20.5876312, "wattage": 40},
    {"sl_id": "PA105", "mac": "00124B001CE32592", "latitude": 39.2419434, "longitude": 20.5874252, "wattage": 40},
    {"sl_id": "PA106", "mac": "00124B001CE3253E", "latitude": 39.2418, "longitude": 20.5872059, "wattage": 40},
    {"sl_id": "PA107", "mac": "00124B001CDE9687", "latitude": 39.24166, "longitude": 20.5869789, "wattage": 40},
    {"sl_id": "PA108", "mac": "00124B001CE326CB", "latitude": 39.2416573, "longitude": 20.5868073, "wattage": 40},
    {"sl_id": "PA109", "mac": "00124B001CE3256A", "latitude": 39.2420921, "longitude": 20.5856342, "wattage": 40},
    {"sl_id": "PA110", "mac": "00124B00193F63F7", "latitude": 39.24195, "longitude": 20.5859413, "wattage": 40},
    {"sl_id": "PA111", "mac": "00124B001CDE95EA", "latitude": 39.2417641, "longitude": 20.5863438, "wattage": 40},
    {"sl_id": "PA112", "mac": "00124B001CE32568", "latitude": 39.2416229, "longitude": 20.5866184, "wattage": 40},
    {"sl_id": "PA113", "mac": "00124B001CE324C2", "latitude": 39.2415428, "longitude": 20.5868053, "wattage": 40},
    {"sl_id": "PA114", "mac": "00124B001CE32744", "latitude": 39.2329063, "longitude": 20.5724716, "wattage": 40},
    {"sl_id": "PA115", "mac": "00124B001CE32709", "latitude": 39.2326431, "longitude": 20.5724869, "wattage": 40},
    {"sl_id": "PA116", "mac": "00124B001CE3257F", "latitude": 39.2323952, "longitude": 20.5724773, "wattage": 40},
    {"sl_id": "PA117", "mac": "00124B00193F3F9C", "latitude": 39.2291527, "longitude": 20.6119862, "wattage": 40},
    {"sl_id": "PA118", "mac": "00124B001CE325F8", "latitude": 39.22921, "longitude": 20.6125622, "wattage": 40},
    {"sl_id": "PA119", "mac": "00124B001CE32499", "latitude": 39.2292557, "longitude": 20.61301, "wattage": 40},
    {"sl_id": "PA120", "mac": "00124B001CE32724", "latitude": 39.22925, "longitude": 20.6133327, "wattage": 40},
    {"sl_id": "PA121", "mac": "00124B001CE3253A", "latitude": 39.2294655, "longitude": 20.6138363, "wattage": 40},
    {"sl_id": "PA122", "mac": "00124B001CDE9662", "latitude": 39.2295647, "longitude": 20.6142826, "wattage": 40},
    {"sl_id": "PA123", "mac": "00124B001CDE9613", "latitude": 39.22949, "longitude": 20.6147861, "wattage": 40},
    {"sl_id": "PA124", "mac": "00124B001CE32494", "latitude": 39.2294121, "longitude": 20.6151943, "wattage": 40},
    {"sl_id": "PA125", "mac": "00124B001CE32577", "latitude": 39.2293625, "longitude": 20.61558, "wattage": 40},
    {"sl_id": "PA126", "mac": "00124B001CE325A0", "latitude": 39.2292862, "longitude": 20.6160183, "wattage": 40},
    {"sl_id": "PA127", "mac": "00124B001CDE95B0", "latitude": 39.2294121, "longitude": 20.6165047, "wattage": 40},
    {"sl_id": "PA128", "mac": "00124B001CDE95CD", "latitude": 39.2307663, "longitude": 20.6151962, "wattage": 40},
    {"sl_id": "PA129", "mac": "00124B001CE3255C", "latitude": 39.23058, "longitude": 20.6154881, "wattage": 40},
    {"sl_id": "PA130", "mac": "00124B001CE32552", "latitude": None, "longitude": 20.61537, "wattage": 40},
    {"sl_id": "PA131", "mac": "00124B001CE3286A", "latitude": 39.22977, "longitude": 20.6153259, "wattage": 40},
    {"sl_id": "PA132", "mac": "00124B001CE3269E", "latitude": 39.2412567, "longitude": 20.5869446, "wattage": 40},
    {"sl_id": "PA133", "mac": "00124B001CE32813", "latitude": 39.2410469, "longitude": 20.5867157, "wattage": 40},
]

# Fast MAC lookup
LUMINAIRE_MAP: dict[str, dict] = {l["mac"]: l for l in LUMINAIRES}
LUMINAIRE_MAP_BY_SL: dict[str, dict] = {l["sl_id"]: l for l in LUMINAIRES}


# ---------------------------------------------------------------------------
# Status logic: active 20:00–06:00, inactive 06:00–20:00
# ---------------------------------------------------------------------------
def is_active_now() -> bool:
    now = datetime.now(timezone.utc)
    hour = now.hour
    return hour >= 20 or hour < 6


def luminaire_status(now_active: bool) -> str:
    return "active" if now_active else "inactive"


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
    now = datetime.now(timezone.utc)
    active = is_active_now()
    return {
        "status": "ok",
        "service": "Luminaires API – Δήμος Πάργας",
        "utc_time": now.isoformat(),
        "luminaires_active": active,
        "total_luminaires": len(LUMINAIRES),
    }


@app.get("/luminaires", tags=["Luminaires"])
def get_all_luminaires(
    status: Optional[str] = Query(None, description="Filter by status: 'active' or 'inactive'"),
):
    """
    Return all luminaires with their geolocation and current status.
    Status is computed from the current UTC time (active 20:00–06:00).
    Optionally filter by status=active or status=inactive.
    """
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


@app.get("/luminaires/{mac}", tags=["Luminaires"])
def get_luminaire(mac: str):
    """
    Return a single luminaire by MAC address with its geolocation and status.
    """
    lum = LUMINAIRE_MAP.get(mac.upper()) or LUMINAIRE_MAP_BY_SL.get(mac.upper())
    if not lum:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Luminaire '{mac}' not found.")

    active = is_active_now()
    return enrich(lum, active)


@app.get("/luminaires/geojson/all", tags=["GeoJSON"])
def get_geojson():
    """
    Return all luminaires as a GeoJSON FeatureCollection.
    Ready to drop into any mapping tool (Leaflet, QGIS, Google Maps, etc.)
    """
    active = is_active_now()
    features = []
    for lum in LUMINAIRES:
        if lum["latitude"] is None or lum["longitude"] is None:
            continue
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lum["longitude"], lum["latitude"]],
            },
            "properties": {
                "mac": lum["mac"],
                "wattage": lum["wattage"],
                "status": luminaire_status(active),
                "schedule": "20:00–06:00 UTC",
            },
        })

    return {
        "type": "FeatureCollection",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "feature_count": len(features),
        "features": features,
    }


@app.get("/status", tags=["Status"])
def get_current_status():
    """
    Returns the current global status of the luminaire network and a summary.
    """
    active = is_active_now()
    now = datetime.now(timezone.utc)
    return {
        "utc_time": now.isoformat(),
        "status": luminaire_status(active),
        "schedule": "Active: 20:00–06:00 UTC | Inactive: 06:00–20:00 UTC",
        "total_luminaires": len(LUMINAIRES),
        "note": "All luminaires follow the same schedule. Individual device faults not tracked in this version.",
    }
