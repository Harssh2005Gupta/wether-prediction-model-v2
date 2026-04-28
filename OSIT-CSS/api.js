/**
 * api.js — SWIF Intelligence API Layer
 * Handles all communication with the OSIT FastAPI backend.
 * Base URL: http://localhost:8000
 */

const API_BASE = 'http://localhost:8000';
const API_TIMEOUT_MS = 15000;

// Default location (India center — overridable via localStorage)
let _userLat = parseFloat(localStorage.getItem('swif_lat') || '20.5937');
let _userLon = parseFloat(localStorage.getItem('swif_lon') || '78.9629');

/**
 * Set user coordinates for all subsequent API calls.
 */
export function setUserLocation(lat, lon) {
    _userLat = lat;
    _userLon = lon;
    localStorage.setItem('swif_lat', lat);
    localStorage.setItem('swif_lon', lon);
}

export function getUserLocation() {
    return { lat: _userLat, lon: _userLon };
}

// ============================================================
// Internal helpers
// ============================================================

async function apiFetch(path, options = {}) {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), API_TIMEOUT_MS);

    try {
        const res = await fetch(`${API_BASE}${path}`, {
            ...options,
            signal: controller.signal,
        });
        clearTimeout(timer);

        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: res.statusText }));
            throw new Error(err.detail || `HTTP ${res.status}`);
        }
        return await res.json();
    } catch (err) {
        clearTimeout(timer);
        if (err.name === 'AbortError') {
            throw new Error('Request timed out. Please check your connection.');
        }
        throw err;
    }
}

function locParams() {
    return `lat=${_userLat}&lon=${_userLon}`;
}

// ============================================================
// Public API Functions
// ============================================================

/**
 * Fetch real-time weather data.
 * @returns {{ temperature, humidity, rainfall, rain_probability, lat, lon }}
 */
export async function fetchWeather() {
    return apiFetch(`/weather?${locParams()}`);
}

/**
 * Fetch soil analysis data.
 * @returns {{ ph, nitrogen, phosphorus, potassium, soc, clay, sand, cec, moisture }}
 */
export async function fetchSoilData() {
    return apiFetch(`/soil?${locParams()}`);
}

/**
 * Fetch smart irrigation recommendations.
 * @returns {{ soil_moisture, temperature, humidity, rainfall, needs_irrigation,
 *             recommendation, priority, next_window, efficiency, water_savings }}
 */
export async function fetchIrrigation() {
    return apiFetch(`/irrigation?${locParams()}`);
}

/**
 * Fetch AI-generated farming alerts.
 * @returns {{ alerts: string[], count: number }}
 */
export async function fetchAlerts() {
    return apiFetch(`/alerts?${locParams()}`);
}

/**
 * Send a crop image for disease detection.
 * @param {File} imageFile  — File object from <input type="file"> or canvas capture
 * @returns {{ disease, confidence, severity, causes, treatment, prevention }}
 */
export async function detectCropDisease(imageFile) {
    const formData = new FormData();
    formData.append('file', imageFile, imageFile.name || 'crop.jpg');
    return apiFetch('/crop-detect', { method: 'POST', body: formData });
}

/**
 * Run full ML + LLM prediction pipeline.
 * @param {{ lat, lon, N?, P?, K?, ph?, image? }} params
 * @returns {{ final_crops, ml_recommendations, llm_recommendations, advisory, disease, alerts }}
 */
export async function runFullPrediction(params = {}) {
    return apiFetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            lat: _userLat,
            lon: _userLon,
            ...params,
        }),
    });
}
