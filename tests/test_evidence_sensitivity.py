import pytest
from research.evidence_sensitivity import coverage_by_facility, wilson_interval, leave_one_facility_out

ROWS = [
    dict(facility='A', instrument='one', has_primary_reference=True, has_dated_status=True),
    dict(facility='A', instrument='two', has_primary_reference=True, has_dated_status=False),
    dict(facility='B', instrument='three', has_primary_reference=False, has_dated_status=True),
]


def test_facility_denominators():
    groups = coverage_by_facility(ROWS)
    assert groups['A'] == {'n': 2, 'primary': 2, 'dated': 1, 'both': 1}
    assert groups['B']['both'] == 0


def test_deletion_sensitivity():
    assert leave_one_facility_out(ROWS) == {'A': 0., 'B': .5}


def test_wilson_bounds():
    lo, hi = wilson_interval(0, 10)
    assert lo == pytest.approx(0)
    assert 0 < hi < 1


def test_duplicate_rejected():
    with pytest.raises(ValueError):
        coverage_by_facility(ROWS + [ROWS[0]])


def test_one_facility_unidentifiable():
    with pytest.raises(ValueError):
        leave_one_facility_out(ROWS[:2])
