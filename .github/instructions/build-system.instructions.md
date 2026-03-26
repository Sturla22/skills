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
- Prefer Python over Bash for repo-owned build and CI automation once the logic grows beyond a short shell wrapper.
- When the project has vendored or submodule dependencies in `external/`, scan them for known vulnerabilities as part of CI. Prefer automated tooling (e.g., `osv-scanner`, Dependabot, or Trivy) over manual audit.
- For release builds, generate an SBOM (Software Bill of Materials) in CycloneDX or SPDX format. Track it alongside the release artifact.
