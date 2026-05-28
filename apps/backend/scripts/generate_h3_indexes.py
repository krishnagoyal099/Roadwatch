"""
RoadWatch — H3 Index Generator
Compute H3 resolution 9 indexes for Bengaluru demo road locations.
Run: python scripts/generate_h3_indexes.py
"""
import h3

LOCATIONS = [
    {"name": "MG Road",             "lat": 12.9756, "lng": 77.6066},
    {"name": "Brigade Road",         "lat": 12.9716, "lng": 77.6066},
    {"name": "Church Street",        "lat": 12.9746, "lng": 77.6046},
    {"name": "Residency Road",       "lat": 12.9706, "lng": 77.6026},
    {"name": "Infantry Road",        "lat": 12.9786, "lng": 77.6026},
    {"name": "Cubbon Road",          "lat": 12.9800, "lng": 77.6050},
    {"name": "Lavelle Road",         "lat": 12.9690, "lng": 77.5980},
    {"name": "Vittal Mallya Road",   "lat": 12.9710, "lng": 77.5950},
    {"name": "Kasturba Road",        "lat": 12.9760, "lng": 77.5930},
    {"name": "Hudson Circle",        "lat": 12.9740, "lng": 77.5970},
]

RESOLUTION = 9


def main():
    print(f"H3 Indexes at Resolution {RESOLUTION}")
    print("-" * 65)
    for loc in LOCATIONS:
        h3_index = h3.latlng_to_cell(loc["lat"], loc["lng"], RESOLUTION)
        print(f"{loc['name']:<22}  lat={loc['lat']}  lng={loc['lng']}  h3={h3_index}")
    print("-" * 65)
    print("Copy these H3 indexes into your seed.py script.")


if __name__ == "__main__":
    main()
