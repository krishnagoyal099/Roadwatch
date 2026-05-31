"""
RoadWatch — ML Pipeline Tests
Basic smoke tests for CV inference pipeline.
"""
import sys
from pathlib import Path

# Add ml/ to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_preprocess_import():
    from inference.preprocess import decode_base64_image
    assert callable(decode_base64_image)


def test_severity_engine_import():
    from inference.severity_engine import compute_severity
    assert callable(compute_severity)


def test_severity_logic():
    from inference.severity_engine import compute_severity
    # Large box = high severity
    assert compute_severity([0, 0, 400, 400], 1000, 1000, 0.9) == 5
    # Tiny box = low severity
    assert compute_severity([0, 0, 50, 50], 1000, 1000, 0.9) == 2
    # None box returns default
    assert compute_severity(None, 1000, 1000, 0.5) == 3


def test_severity_confidence_modifier():
    from inference.severity_engine import compute_severity
    # Low confidence pulls severity down
    sev_low_conf = compute_severity([0, 0, 100, 100], 1000, 1000, 0.3)
    sev_high_conf = compute_severity([0, 0, 100, 100], 1000, 1000, 0.9)
    assert sev_high_conf >= sev_low_conf


def test_class_names():
    from inference.predictor import CLASS_NAMES
    assert len(CLASS_NAMES) == 5
    assert "Pothole" in CLASS_NAMES
    assert "Surface Crack" in CLASS_NAMES