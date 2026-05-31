"""
RoadWatch — Severity Engine
Computes severity score 1-5 from bounding box area and confidence.
"""


def compute_severity(box: list, img_w: int, img_h: int, confidence: float) -> int:
    """
    Severity 1-5 based on bounding box area ratio and confidence.
    
    Area thresholds:
      < 1%   → 1  (tiny)
      1-3%   → 2  (small)
      3-8%   → 3  (moderate)
      8-15%  → 4  (large)
      > 15%  → 5  (critical)
    """
    if box is None or img_w == 0 or img_h == 0:
        return 3  # default fallback

    x1, y1, x2, y2 = box
    area_ratio = ((x2 - x1) * (y2 - y1)) / (img_w * img_h)

    if area_ratio < 0.01:   severity = 1
    elif area_ratio < 0.03: severity = 2
    elif area_ratio < 0.08: severity = 3
    elif area_ratio < 0.15: severity = 4
    else:                   severity = 5

    if confidence < 0.45:   severity = max(1, severity - 1)
    elif confidence > 0.80: severity = min(5, severity + 1)

    return severity