# snapcap

snapcap takes snapshot backups of a directory and stores them in a repository on local disk or a mounted share. Each file is split into chunks and stored by the hash of its content, so a snapshot only stores what changed since the last one.

- [Getting started](getting-started.md)
- [Usage](usage.md)
- [Configuration](configuration.md)
- [Design](design.md)
