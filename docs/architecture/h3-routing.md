# H3 Spatial Indexing

RoadWatch uses Uber's **H3** hexagonal hierarchical spatial index to map coordinates to road segments. This approach allows for incredibly fast database queries without requiring a heavy PostGIS extension.

## Why H3?
Instead of performing complex bounding-box or radius searches (e.g., "find roads within 5km of lat/lng"), we convert coordinates into a static string ID (an H3 hex address). Database lookups simply become an exact string match: `WHERE h3_index = '89283082803ffff'`.

## Implementation Details

1. **Resolution Configuration**: 
   - We use **Resolution 9** (configurable via `H3_RESOLUTION` in `.env`).
   - Resolution 9 hexagons have an edge length of roughly 174 meters, which perfectly encompasses a standard road segment or city block.

2. **K-Ring Expansion**:
   - When a citizen reports a location (e.g., lat: 28.6139, lng: 77.2090), we convert it to its H3 index.
   - If there is no exact road segment mapped to that exact hexagon in the database, we perform a **K-Ring expansion** (`k=1`).
   - This checks the 6 immediately adjacent neighboring hexagons to find the closest registered road segment.

3. **Service Integration**:
   - H3 utility functions are located in `apps/backend/app/utils/h3_utils.py`.
   - Used extensively by the `QualityService` and `ComplaintService` to tie citizen reports to specific government infrastructure nodes.
