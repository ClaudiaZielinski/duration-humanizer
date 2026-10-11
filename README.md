# duration-humanizer

Converts a float of seconds into a compact human-readable string like `3h12m45s`, omitting units that are zero.

```python
from duration_humanizer import humanize, humanize_parts

humanize(11765.0)        # '3h12m45s'
humanize(0.0)            # '0s'
humanize_parts(90.0)     # ['1m', '30s']
```

## Why this exists

Durations in logs, CLIs, and progress lines want to be short and skimmable. `datetime.timedelta` renders as `3:12:45` which is fine in a spreadsheet and noisy in a one-line status. This library gives you the `3h12m45s` form without pulling in a dependency.

The trade-off: it stops at days. Going higher into weeks/months/years forces a decision about what a "month" means, and that decision is always wrong for some caller. If you need coarser buckets, divide your input before calling `humanize`.

## Edge cases

- **Zero duration** returns `0s`, not an empty string. An empty return is almost never what a caller wants when they ask "how long did this take?".
- **Sub-second values are truncated**, not rounded. `59.9s` renders as `59s`, never `1m`. This matches how most log lines behave and avoids surprising jumps near unit boundaries.
- **Negative input** raises `ValueError`.

## Design notes

The window stores values eagerly rather than keeping running aggregates. Running
sums drift with floating point over long streams, and recomputing from a small
buffer is cheap enough that the drift is not worth the speed.

