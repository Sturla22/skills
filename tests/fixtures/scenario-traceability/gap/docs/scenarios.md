# Usage Scenarios

**SC-001** — A user can configure the sample rate and the system validates it.

**SC-002** — When the sensor input becomes stale, the controller rejects it.

**SC-003** — When power is lost mid-write, the device recovers to the last
valid state on next boot.

## Trace table

| ID     | Description (short)         | Covering test(s)   | Status    |
|--------|-----------------------------|--------------------|-----------|
| SC-001 | Sample rate validated        | tests/test_main.c  | Covered   |
| SC-002 | Stale sensor rejected        | tests/test_main.c  | Covered   |
| SC-003 | Power-loss recovery          | —                  | Uncovered |
