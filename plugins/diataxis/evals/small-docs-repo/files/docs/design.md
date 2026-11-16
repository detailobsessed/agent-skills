# Design

snapcap stores chunks rather than files so that a renamed or slightly edited file costs almost nothing in a new snapshot. We chose fixed-size chunks over content-defined chunking to keep the code small; content-defined chunking would deduplicate better when bytes are inserted in the middle of a large file, and we may switch later.

Snapshots are plain JSON records listing chunk hashes per file. Keeping them readable means a repository can be inspected and repaired by hand if snapcap itself is broken.
