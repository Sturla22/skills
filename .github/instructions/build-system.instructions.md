---
applyTo: "**/CMakeLists.txt,**/*.cmake,**/west.yml,**/module.yml,**/board*.yml,**/boards/**/*.yml,**/toolchain*.cmake"
---
# Build-system instructions

- Keep build logic declarative and readable.
- Prefer target-based structure over global mutable settings.
- Avoid hidden side effects in helper functions and macros.
- Keep host-test, simulation, and target-build paths explicit.
- When adding flags or definitions, scope them to the smallest relevant target.
- Document why non-obvious linker, toolchain, or board settings exist.
- Prefer CI workflows that call repo-tracked scripts or Make targets under `tools/` instead of embedding substantial shell logic directly in workflow YAML.
