# oracle-db-skills mapping used in this project

This project was updated to align its prompts, operational framing, and best-practice guidance with the public `krisrice/oracle-db-skills` repository.

## Tool mappings

- Tool 1 AWR/ASH slowdown analysis
  - performance/awr-reports.md
  - performance/ash-analysis.md
  - performance/wait-events.md

- Tool 2 Top SQL by DB time + plan changes
  - performance/awr-reports.md
  - performance/explain-plan.md
  - performance/optimizer-stats.md

- Tool 3 Blocking sessions
  - appdev/locking-concurrency.md
  - performance/wait-events.md

- Tool 4 Active sessions by wait class
  - performance/wait-events.md
  - appdev/locking-concurrency.md

- Tool 5 Performance vs yesterday
  - performance/awr-reports.md
  - performance/wait-events.md

- Tool 6 Risky query patterns
  - performance/index-strategy.md
  - performance/explain-plan.md
  - performance/optimizer-stats.md

- Tool 7 Workload spikes
  - performance/awr-reports.md
  - performance/ash-analysis.md

- Tool 8 Early warning scan
  - performance/memory-tuning.md
  - performance/wait-events.md
  - performance/optimizer-stats.md
  - admin/undo-management.md

- Tool 9 Tablespace capacity
  - admin/undo-management.md
  - admin/backup-recovery.md

- Tool 10 Data Guard health
  - admin/dataguard.md
  - admin/redo-log-management.md

## Project updates made
- AWR/ASH tool expanded to include snapshot window, top wait classes, top wait events, ASH wait profile, and top SQL by ASH samples.
- Early warning tool now includes undo-health signals in addition to parsing, temp, memory, and concurrency indicators.
- Risky query tool now flags larger full scans at a lower threshold suitable for demo data.
- Tools metadata now stores repo reference paths for future expansion.
- UI supports add/edit for non-built-in tools with SQL safety checks.
- Redwood-inspired light UI styling added.
