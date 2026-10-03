"""Core implementation for converting a float of seconds into a compact string."""

from __future__ import annotations

# Order matters: largest unit first so the output reads naturally left-to-right.
# We stop at days. Going higher (weeks/months/years) introduces ambiguity in
# what a "month" or "year" means, so the library declines to guess. A caller
# who needs coarser buckets can divide their input before calling humanize.
_UNITS: tuple[tuple[str, int], ...] = (
    ("d", 86400),
    ("h", 3600),
    ("m", 60),
    ("s", 1),
)


def humanize_parts(seconds: float) -> list[str]:
    """Return a list like ['3h', '12m', '45s'] for the given seconds.

    Zero-valued units are skipped. """
    if seconds < 0:
        raise ValueError("seconds must be non-negative")

    remaining = float(seconds)
    parts: list[str] = []
    for label, size in _UNITS:
        value = int(remaining // size)
        if value > 0:
            parts.append(f"{value}{label}")
            remaining -= value * size

    if not parts:
        # A duration of zero is the one case where "omit zero units" would
        # produce an empty string, which is almost never useful to a caller.
        # Returning "0s" keeps the output always non-empty and unambiguous.
        return ["0s"]

    return parts


def humanize(seconds: float) -> str:
    """Convert a float of seconds into a compact human-readable string.

    Examples:
        humanize(11765.0) -> '3h12m45s'
        humanize(0.0)     -> '0s'
        humanize(90.0)    -> '1m30s'

    Sub-second remainders are truncated, not rounded. This matches how most
    CLI tools and log lines render durations, and avoids surprising jumps
    like '0s' becoming '1s' at 0.999 seconds. If you need rounding, round
    your input first.
    """
    return "".join(humanize_parts(seconds))
