# Verification

## Commands

```bash
make format-cpp
make check-clang-format
python3 -m pre_commit run --all-files clang-format
make run-pre-commit
make ci-checks
python3 tools/cli.py check-work cpp-clang-format-integration
```

## Result

- `make format-cpp` passed on 2026-03-21.
- `make check-clang-format` passed on 2026-03-21.
- `python3 -m pre_commit run --all-files clang-format` passed on 2026-03-21.
- `make run-pre-commit` passed on 2026-03-21.
- `make ci-checks` passed on 2026-03-21.
- `python3 tools/cli.py check-work cpp-clang-format-integration` passed on 2026-03-21.

## Notes

- The formatter is intentionally scoped to checked-in starter C/C++ sources under `libs/`, `src/`, and `tests/`, not generated build trees.
- The local `pre-commit` hook auto-formats changed starter C/C++ files, while CI uses the non-mutating `make check-clang-format` path.
- The chosen `.clang-format` profile preserves the starter’s Allman-style brace layout and avoids a larger style migration.
