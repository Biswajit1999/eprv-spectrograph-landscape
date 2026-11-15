"""Conditional catalogue evidence-coverage diagnostics; no performance ranking.

Each row is an instrument record with facility, instrument, and boolean
has_primary_reference / has_dated_status fields. No source is inferred.
"""
import math


def coverage_by_facility(rows):
    """Return denominators and evidence coverage, grouped by facility."""
    result = {}
    seen = set()
    for row in rows:
        facility = row['facility']
        name = row['instrument']
        key = (facility, name)
        if not facility or not name or key in seen:
            raise ValueError('nonempty unique facility/instrument pairs required')
        seen.add(key)
        group = result.setdefault(facility, {'n': 0, 'primary': 0, 'dated': 0, 'both': 0})
        primary, dated = row['has_primary_reference'], row['has_dated_status']
        if not isinstance(primary, bool) or not isinstance(dated, bool):
            raise ValueError('evidence flags must be booleans')
        group['n'] += 1
        group['primary'] += int(primary)
        group['dated'] += int(dated)
        group['both'] += int(primary and dated)
    return result


def wilson_interval(successes, n, z=1.959963984540054):
    """Descriptive independent-Bernoulli Wilson interval; not cluster-adjusted."""
    if not isinstance(successes, int) or not isinstance(n, int) or n <= 0 or not 0 <= successes <= n or z <= 0 or not math.isfinite(z):
        raise ValueError('invalid binomial interval arguments')
    p = successes / n
    den = 1 + z*z/n
    center = (p + z*z/(2*n))/den
    half = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/den
    return center-half, center+half


def leave_one_facility_out(rows):
    """Compare overall complete-evidence fraction after each facility deletion."""
    groups = coverage_by_facility(rows)
    n = sum(g['n'] for g in groups.values())
    complete = sum(g['both'] for g in groups.values())
    if len(groups) < 2:
        raise ValueError('at least two facilities required')
    return {facility: (complete-g['both'])/(n-g['n']) for facility, g in groups.items()}
