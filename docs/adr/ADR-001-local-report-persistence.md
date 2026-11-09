# ADR-001-local-report-persistence

## Status
Accepted — Ayla reviewed the design and instructed development to proceed.

## Context
UC-001 needs restart-safe local reports, optional original images up to 10 MiB,
and all-or-nothing receipt without introducing a service dependency. Storage is a
consequential choice that may affect later use cases.

## Alternatives
- Local files for images plus a database for reports: requires coordinating failure
  and cleanup across two stores, including interrupted writes.
- Distributed storage or an ORM/migration framework: adds moving parts not needed
  for the local demonstration.

## Decision
Use local SQLite for fictional scenarios and reports, including an
optional original image as a bounded BLOB in the same transaction as its report.
Confirm receipt only after the transaction succeeds. Keep the database behind the
application's repository boundary; the domain and application do not depend on it.
Proposed by the design agent; accepted by Ayla in this session.

## Consequences
- One transactional store avoids orphaned image files and partial report/image saves;
  a writable local database and sufficient disk space are required.
- Images increase database and backup size; the per-image limit does not bound total
  growth. This is appropriate for a small local demo, not a scaling or backup plan.
- Current architecture is recorded in `docs/PROJECT.md`.
  No new durable agent rule is proposed. No ORM or migration tool is selected.

## Supersedes
none
