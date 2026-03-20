# Usage Scenarios

**SC-001** — A user can configure the sample rate and the system validates it
falls within the hardware-supported range before accepting it.

**SC-002** — When the sensor input becomes stale, the controller rejects it
and reports a recoverable fault.

## Trace table

| ID     | Description (short)          | Covering test(s)      | Status  |
|--------|------------------------------|-----------------------|---------|
| SC-001 | Sample rate validated         | tests/test_main.c     | Covered |
| SC-002 | Stale sensor input rejected   | tests/test_main.c     | Covered |
