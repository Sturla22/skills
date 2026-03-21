# Usage Scenarios

<!-- PROJECT or WORK-PACKET level — delete the line that does not apply.     -->
<!-- Project level : docs/scenarios.md                                        -->
<!-- Work-packet   : docs/work/<work-id>/scenarios.md                         -->

<!-- HOW TO USE                                                               -->
<!-- 1. Add one scenario per entry. Keep the language non-technical.          -->
<!-- 2. Assign the next available SC-NNN ID. Never renumber existing entries. -->
<!-- 3. In each covering test add a comment: Covers: SC-NNN                   -->
<!-- 4. Run `python tools/cli.py check-coverage` to verify coverage.  -->
<!-- 5. Update the trace table below when you add or cover a scenario.        -->

## Scenarios

**SC-001** — A user can configure the sample rate and the system validates it
falls within the hardware-supported range before accepting it.

**SC-002** — When the sensor input becomes stale, the controller rejects it,
reports a recoverable fault, and continues operating on the last known good value.

<!-- Add new scenarios below. Use the next integer; do not reuse or renumber. -->

## Trace table

<!-- Updated by hand or regenerated with: python tools/cli.py check-coverage --root . -->
<!-- Status: Covered | Uncovered | Partial                                    -->

| ID     | Description (short)                  | Covering test(s)                    | Status    |
|--------|--------------------------------------|-------------------------------------|-----------|
| SC-001 | Sample rate validated on config      | tests/unit/test_config.c            | Covered   |
| SC-002 | Stale sensor input rejected          | tests/unit/test_sensor.c            | Covered   |
