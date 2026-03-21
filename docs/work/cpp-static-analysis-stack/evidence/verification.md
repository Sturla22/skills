# Verification

## Commands

```bash
python3 -m pip install --user pre-commit
make install-pre-commit
make check-static-analysis
python3 -m pre_commit validate-config
python3 -m pre_commit run --all-files static-analysis
python3 tools/cli.py sync
make ci-checks
python3 tools/cli.py check-work cpp-static-analysis-stack
```

## Result

- `make check-static-analysis` passed on 2026-03-21.
- `make install-pre-commit` passed on 2026-03-21.
- `python3 -m pre_commit validate-config` passed on 2026-03-21.
- `python3 -m pre_commit run --all-files static-analysis` passed on 2026-03-21.
- `python3 tools/cli.py sync` updated generated files, including `.claude/CLAUDE.md`.
- `make ci-checks` passed on 2026-03-21.
- `python3 tools/cli.py check-work cpp-static-analysis-stack` passed on 2026-03-21.

## Notes

- The analyzer script explicitly discovers host and Arm GNU C++ include paths and passes them to `clang-tidy`, which was necessary for reliable analysis of both host-test and target-side C++ files in this environment.
- The analyzer entrypoint is implemented in Python rather than Bash because the logic grew beyond a short shell wrapper.
- The enforced check set excludes `bugprone-reserved-identifier` because the starter’s linker and runtime startup symbols intentionally use reserved names that would otherwise create persistent false positives.
- The repo now uses the actual `pre-commit` package for the local hook path, with a minimal local hook that delegates back to `make check-static-analysis`.
- `make install-pre-commit` now handles the case where `core.hooksPath` is explicitly set to the default `.git/hooks` location, which would otherwise cause `pre-commit install` to refuse the install.
