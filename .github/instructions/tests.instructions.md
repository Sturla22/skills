---
applyTo: "**/test*/**,**/*test*.c,**/*test*.cc,**/*test*.cpp,**/*test*.py,**/*_test.py,**/tests/**/*.py,**/tests/**/*.c,**/tests/**/*.cpp"
---
# Test-specific instructions

- Treat tests as executable specifications.
- Prefer deterministic tests with fake time, fake I/O, and explicit fixtures.
- Before refactoring risky code, add characterization tests for current behavior.
- Cover failure cases, not just happy paths.
- Use precise names that describe the scenario and expected behavior.
- If hardware is required, separate host-simulatable logic from target-only checks.
- When a bug is fixed, pin it down with a test if practical.
