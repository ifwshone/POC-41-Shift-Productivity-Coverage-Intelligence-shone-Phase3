from assistant.core.output_validator import validate_grounded_response

PKG = {"answer_data": {"avg": 93.6, "gap": -25.8, "overtime": 40, "rank": 1, "n": 5}, "metadata": {"data_version": "1.0.0"}}


def test_accepts_evidence_numbers():
    assert validate_grounded_response("Average 93.6, gap -25.8, overtime 40 hours, rank 1, n=5.", PKG)


def test_accepts_int_float_format_difference():
    assert validate_grounded_response("Overtime was 40.0 hours.", PKG)


def test_rejects_invented_values():
    for bad in ["Output was 119.9.", "Overtime was 28 hours.", "Across 7 days.", "In 2026 the gap was 100.0."]:
        assert not validate_grounded_response(bad, PKG), bad


def test_rejects_empty():
    assert not validate_grounded_response("", PKG)
