# Code Review Checklist

Use as a lens-based guide for the `reviewer` role. Not every lens applies to every change — skip inapplicable sections with a brief reason.

## Correctness

- [ ] Does the change do what the brief / acceptance criteria require?
- [ ] Are edge cases and error paths handled?
- [ ] Are assumptions documented?

## Security

- [ ] Are inputs validated at trust boundaries?
- [ ] Are secrets handled safely (no plaintext in source or flash)?
- [ ] Is authentication and authorization correct where applicable?

## Performance and resources

- [ ] Is resource impact acceptable (stack, RAM, flash, CPU, latency)?
- [ ] Are allocations bounded and deterministic?
- [ ] Is the cost model explicit for performance-sensitive paths?

## Contract preservation

- [ ] Does the change preserve existing interface contracts?
- [ ] If a contract changed, is it documented and versioned?
- [ ] Are callers updated?

## Test coverage

- [ ] Are new behaviors covered by tests?
- [ ] Are failure paths tested, not just happy paths?
- [ ] Is the test at the right level of the pyramid?

## Documentation

- [ ] Are ADRs or docs updated if design truth changed?
- [ ] Are non-obvious decisions explained in code or commit message?
