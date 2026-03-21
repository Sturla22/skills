# Research: C++ Static Analysis

**Research question:** What major categories of static analysis exist for C++ today, and what do mainstream tools officially claim to cover? This summary is intentionally narrowed to the current mainstream tool landscape rather than an exhaustive catalog of every analyzer.
**Retrieval date:** 2026-03-21

## Sources consulted

| Source | URL | Version / date context | Notes |
|---|---|---|---|
| Clang-Tidy docs | https://clang.llvm.org/extra/clang-tidy/ | Extra Clang Tools 23.0.0git docs, retrieved 2026-03-21 | Lint-style checks, diagnostics, fixes, compile database usage |
| Query-based custom clang-tidy checks | https://clang.llvm.org/extra/clang-tidy/QueryBasedCustomChecks.html | Extra Clang Tools 23.0.0git docs, retrieved 2026-03-21 | Custom AST-query-driven checks |
| Clang Static Analyzer docs | https://clang.llvm.org/docs/ClangStaticAnalyzer.html | Clang 23.0.0git docs, retrieved 2026-03-21 | Path-sensitive interprocedural analysis |
| Clang Static Analyzer command-line usage | https://clang.llvm.org/docs/analyzer/user-docs/CommandLineUsage.html | Clang 23.0.0git docs, retrieved 2026-03-21 | `scan-build`, CodeChecker, CTU context |
| Clang Thread Safety Analysis | https://clang.llvm.org/docs/ThreadSafetyAnalysis.html | Clang 23.0.0git docs, retrieved 2026-03-21 | Attribute-based concurrency analysis |
| Clang C++ Safe Buffers | https://clang.llvm.org/docs/SafeBuffers.html | Clang 23.0.0git docs, retrieved 2026-03-21 | Buffer-safety programming model and warnings |
| GCC static analyzer options | https://gcc.gnu.org/onlinedocs/gcc/Static-Analyzer-Options.html | current manual page, retrieved 2026-03-21 | `-fanalyzer` scope and caveats |
| GCC 14 changes | https://gcc.gnu.org/gcc-14/changes.html | GCC 14 release docs, retrieved 2026-03-21 | Explicit C++ suitability caveat |
| Cppcheck home page | https://cppcheck.sourceforge.io/ | current site, retrieved 2026-03-21 | Scope, design goals, false-positive emphasis |
| Cppcheck manual | https://cppcheck.sourceforge.io/manual.html | current manual page, retrieved 2026-03-21 | Compilation database and project integration |
| CodeQL C/C++ built-in queries | https://docs.github.com/en/code-security/code-scanning/managing-your-code-scanning-configuration/c-cpp-built-in-queries | current GitHub Docs, retrieved 2026-03-21 | Built-in C/C++ query suites |
| CodeQL custom queries | https://docs.github.com/en/code-security/how-tos/scan-code-for-vulnerabilities/scan-from-vs-code/creating-a-custom-query | current GitHub Docs, retrieved 2026-03-21 | Project-specific custom queries |
| CodeQL packs | https://docs.github.com/code-security/codeql-cli/about-codeql-packs | current GitHub Docs, retrieved 2026-03-21 | Query packs and model packs |
| SonarQube Server CFamily overview | https://docs.sonarsource.com/sonarqube/latest/analyzing-source-code/languages/c-family | current docs, retrieved 2026-03-21 | Supported C++ versions and overview |
| SonarQube CFamily analysis modes | https://docs.sonarsource.com/sonarqube-cloud/advanced-setup/languages/c-family/analysis-modes | current docs, retrieved 2026-03-21 | Auto vs compile-database modes |
| SonarQube running CFamily analysis | https://docs.sonarsource.com/sonarqube-server/2025.4/analyzing-source-code/languages/c-family/running-the-analysis/ | 2025.4 docs, retrieved 2026-03-21 | `sonar.cfamily.compile-commands` |
| PVS-Studio product page | https://pvs-studio.com/en/pvs-studio/ | current site, retrieved 2026-03-21 | Product scope, rule count, CI positioning |
| PVS-Studio manual | https://pvs-studio.com/en/docs/ | docs updated 2026-02-06, retrieved 2026-03-21 | Analyzer scope and integration areas |
| PVS-Studio MISRA compliance docs | https://pvs-studio.com/en/docs/manual/6966/ | docs retrieved 2026-03-21 | MISRA mapping for diagnostics |

## Key findings

| Finding | Status | Source | Version | Section |
|---|---|---|---|---|
| `clang-tidy` is a Clang-based C++ linter tool with many check families, fix-it support, and recommended use with a compile command database. | Definitive | Clang-Tidy docs | 23.0.0git | overview |
| `clang-tidy` supports query-based custom checks that can be enabled like built-in checks. | Definitive | Query-based custom clang-tidy checks | 23.0.0git | introduction and configuration |
| Clang Static Analyzer performs path-sensitive, interprocedural analysis based on symbolic execution and supports project-scale use via `scan-build` and CodeChecker. | Definitive | Clang Static Analyzer docs; command-line usage docs | 23.0.0git | introduction; command-line usage |
| Clang Thread Safety Analysis is a compile-time C++ analysis that warns about potential race conditions using attributes and capability annotations. | Definitive | Thread Safety Analysis docs | 23.0.0git | introduction and basic concepts |
| Clang Safe Buffers is a C++-focused buffer-safety analysis and hardening model built around warnings such as `-Wunsafe-buffer-usage` and safe container/view usage. | Definitive | C++ Safe Buffers docs | 23.0.0git | introduction and programming model |
| GCC’s `-fanalyzer` is a bug-finding tool based on symbolic execution, but the current official docs say it is only suitable for C code in this release. | Definitive | GCC static analyzer options; GCC 14 changes | current manual / GCC 14 docs | `-fanalyzer`; changes page |
| Cppcheck is a static analysis tool for C/C++ focused on undefined behavior and dangerous constructs, with an explicit goal of few false positives and support for non-standard syntax common in embedded code. | Definitive | Cppcheck home page | current site | home page overview |
| Cppcheck can analyze projects through `compile_commands.json` and can optionally import Clang ASTs using the experimental `--clang` mode. | Definitive | Cppcheck manual | current manual page | compilation database; Clang parser |
| CodeQL ships built-in C/C++ query suites and supports custom queries, query packs, and model packs for extending analysis. | Definitive | CodeQL C/C++ queries; custom query docs; packs docs | current GitHub Docs | built-in queries; custom queries; packs |
| SonarQube CFamily supports C++ analysis, distinguishes analysis modes, and documents compilation-database-based analysis as the highest-quality mode. | Definitive | SonarQube CFamily overview; analysis modes; running analysis | current / 2025.4 docs | overview; analysis modes; running analysis |
| PVS-Studio positions itself as a static analyzer/SAST tool for C and C++, offers CLI and CI integration, and documents MISRA mapping support. | Definitive | PVS-Studio product page; manual; MISRA docs | current docs | product overview; manual; MISRA compliance |
| The practical C++ static-analysis landscape is a stack, not a single tool: linting, path-sensitive bug finding, security query analysis, platform reporting, and specialized analyses each cover different defect classes. | Inferred from sources | Cross-source synthesis | N/A | all sources above |
| `compile_commands.json` is a recurring integration substrate across multiple C++ analyzers and analysis platforms. | Inferred from sources | Clang-Tidy docs; Cppcheck manual; SonarQube CFamily docs | N/A | tool usage sections |

## Detailed findings by category

### 1. Linting and coding-guideline enforcement

- **`clang-tidy`** is best understood as a lint-style, AST-based analysis tool with many check families rather than as a deep path-sensitive bug finder. Its docs describe it as a Clang-based tool with broad check families and fix-it support. The docs also say it works best when the project has a compile command database.
- The same toolchain now supports **query-based custom checks**, which makes `clang-tidy` more relevant when a team wants project-specific style or API usage rules without writing a full LLVM checker.

### 2. Path-sensitive bug finding

- **Clang Static Analyzer** explicitly documents path-sensitive, interprocedural analysis based on symbolic execution. The command-line docs distinguish `scan-build` from CodeChecker and note that CodeChecker is the more actively maintained, feature-rich collaborative path.
- **GCC `-fanalyzer`** also documents symbolic-execution-based bug finding, but the key current caveat for C++ is explicit: the GCC docs say it is only suitable for C in this release. For a C++-specific landscape summary, that makes GCC analyzer a boundary case rather than a mainstream C++ answer.
- **Cppcheck** positions itself differently again: it is a standalone C/C++ static analyzer focused on undefined behavior and dangerous constructs, with low false positives as an explicit design goal.

### 3. Security and query-driven analysis

- **CodeQL** documents built-in C/C++ queries in default and extended suites, and also documents custom queries, query packs, and model packs. This places CodeQL squarely in the “queryable security and semantic analysis platform” category rather than in linting.
- The official docs also make clear that CodeQL is designed to be extended for project-specific patterns, which is important when the required checks are domain- or framework-specific.

### 4. Quality-platform and policy-layer analysis

- **SonarQube CFamily** is documented as a platform-layer analysis offering rather than a single standalone command-line checker. Its docs cover supported C++ language versions, analysis modes, and the `sonar.cfamily.compile-commands` setting for compilation-database mode.
- The analysis-modes docs explicitly recommend compilation-database mode when the user wants the highest CFamily analysis quality.

### 5. Commercial analyzer and standards mapping

- **PVS-Studio** documents itself as a static analyzer/SAST tool for C and C++, with CLI/CI integration and MISRA compliance mapping support. The docs also emphasize cross-platform analysis and report formats for integration into quality services.
- This makes it materially different from a pure linter: the official framing is broader code quality, security, and safety analysis with workflow integration.

### 6. Specialized static analyses inside the Clang ecosystem

- **Thread Safety Analysis** is a specialized, attribute-driven C++ compile-time analysis focused on lock/capability correctness and race-risk detection.
- **C++ Safe Buffers** is a specialized static-analysis and programming-model effort for buffer safety in C++, tied to safer containers/views and warning-based migration.
- These are not just “more warnings”; they are targeted analysis systems for specific defect classes.

## Gaps and open items

- This summary does not exhaustively cover every commercial analyzer. Tools such as Coverity were not researched in depth in this slice.
- Safety-certified, avionics-oriented, or MISRA-first analyzers likely deserve a separate deeper pass if the real decision context is regulated software.
- The scope here is mainstream tool families, not performance benchmarks, false-positive-rate measurement, or cost comparison.
- The line between compiler diagnostics, static analysis, and code-quality platforms varies by vendor; categories here are a practical synthesis, not a universal taxonomy.

## Research boundary

Facts established above. Tool-stack recommendation, rollout design, CI policy, and per-repo selection begin here and should be handled as planning work, not as additional research in this file.
