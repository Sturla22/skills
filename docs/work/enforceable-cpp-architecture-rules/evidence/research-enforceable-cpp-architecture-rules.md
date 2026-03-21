# Research: Enforceable Architecture Rules for C++ Codebases

**Research question:** Which architecture rules in C++ codebases are mechanically enforceable, and which tooling supports enforcement rather than only visualization or advisory analysis?
**Retrieval date:** 2026-03-21

## Sources consulted

| Source | URL | Version / date context | Notes |
|---|---|---|---|
| `target_include_directories` | https://cmake.org/cmake/help/latest/command/target_include_directories.html | CMake 4.3.0 docs, retrieved 2026-03-21 | Include propagation and usage requirements |
| `target_link_libraries` | https://cmake.org/cmake/help/latest/command/target_link_libraries.html | CMake 4.3.0 docs, retrieved 2026-03-21 | Public/private link interface propagation |
| `CMakeGraphVizOptions` note | https://cmake.org/cmake/help/latest/module/CMakeGraphVizOptions.html | CMake 4.3.0 docs, retrieved 2026-03-21 | Points to `cmake --graphviz` for graph export |
| Bazel visibility | https://bazel.build/concepts/visibility | current web docs, retrieved 2026-03-21 | Target visibility constraints |
| Bazel C/C++ rules | https://bazel.build/reference/be/c-cpp | current web docs, retrieved 2026-03-21 | Header inclusion checking, `implementation_deps`, `layering_check` |
| Clang-tidy contributing guide | https://clang.llvm.org/extra/clang-tidy/Contributing.html | Clang 23.0.0git docs, retrieved 2026-03-21 | Custom and plugin checks |
| Query-based custom checks | https://clang.llvm.org/extra/clang-tidy/QueryBasedCustomChecks.html | Clang 23.0.0git docs, retrieved 2026-03-21 | Query-based lint rules using clang-query syntax |
| include-what-you-use home page | https://include-what-you-use.org/ | current site, retrieved 2026-03-21 | Include hygiene and forward-declare suggestions |
| GitHub CodeQL custom queries | https://docs.github.com/en/code-security/concepts/code-scanning/codeql/custom-codeql-queries | GitHub Docs, retrieved 2026-03-21 | Custom queries for architecture/framework-specific patterns |
| SciTools Understand manual | https://docs.scitools.com/manuals/pdf/understand.pdf | manual retrieved 2026-03-21 | Architecture hierarchies, dependency views, CodeCheck |
| CppDepend dependency cycles | https://www.cppdepend.com/features/dependency-cycles | current site, retrieved 2026-03-21 | Continuous cycle detection |
| CppDepend getting started | https://www.cppdepend.com/Doc/Getting-Started-with-CppDepend.pdf | PDF retrieved 2026-03-21 | Custom rules and highlighted rule violations |
| SonarQube Cloud architecture | https://docs.sonarsource.com/sonarqube-cloud/architecture | docs retrieved 2026-03-21 | Current architecture feature scope and language support |

## Key findings

| Finding | Status | Source | Version | Section |
|---|---|---|---|---|
| CMake can encode component interfaces with `PUBLIC`, `PRIVATE`, and `INTERFACE` usage requirements for include directories and link dependencies. | Definitive | CMake `target_include_directories`, `target_link_libraries` | 4.3.0 | command reference |
| CMake documents target graph export via `cmake --graphviz`, which supports post-processing or custom CI checks over the target graph. | Definitive | `CMakeGraphVizOptions` note | 4.3.0 | module note |
| Bazel can enforce target visibility and warns production users not to disable visibility checks. | Definitive | Bazel visibility docs | current web docs | visibility concepts |
| Bazel `cc_library` distinguishes public headers (`hdrs`) from private headers (`srcs`), documents allowed direct inclusions, and states that inclusion checking is enforced when toolchain support and `layering_check` are enabled. | Definitive | Bazel C/C++ rules | current web docs | `cc_library`, "Header inclusion checking" |
| Bazel `implementation_deps` keeps headers and include paths available when compiling the library itself but not to dependent libraries. | Definitive | Bazel C/C++ rules | current web docs | `implementation_deps` attribute |
| Clang-tidy is appropriate for linter-style and coding-style checks, supports out-of-tree plugins, and supports query-based custom checks using clang-query syntax. | Definitive | Clang-tidy docs | 23.0.0git | "Choosing the Right Place for your Check", "Writing a clang-tidy Check", query-based custom checks |
| include-what-you-use analyzes C/C++ includes, reports missing and superfluous includes, and suggests forward declarations when possible. | Definitive | include-what-you-use site | current site | home page overview |
| GitHub CodeQL custom queries are intended to detect patterns specific to the application's architecture or frameworks and to enforce organization-specific coding standards. | Definitive | GitHub CodeQL custom queries docs | current docs | "When to use custom queries" |
| SciTools Understand provides architecture hierarchies and a CodeCheck mechanism that can report violations through custom checks. | Definitive | Understand manual | current manual retrieved 2026-03-21 | architecture overview; CodeCheck section |
| CppDepend continuously detects dependency cycles and provides custom rule support through CQLinq-style rules. | Definitive | CppDepend site and getting-started PDF | current site / retrieved PDF | dependency cycles; getting started |
| SonarQube Cloud's architecture feature currently supports C#, Java, JavaScript, Python, and TypeScript, not C++. | Definitive | SonarQube Cloud architecture docs | current docs | overview |
| Strongest mechanical enforcement in C++ comes from build-graph controls plus source analyzers; architecture dashboards alone are weaker unless wired to fail CI or raise actionable issues. | Inferred from sources | Cross-source synthesis | N/A | build docs plus analyzer docs plus architecture-tool docs |
| CMake can support architecture boundaries, but native docs show propagation semantics and graph export rather than a first-class architecture policy language; stricter enforcement therefore typically requires custom CI scripts or external analyzers. | Inferred from sources | Cross-source synthesis | N/A | CMake command refs and graph export note |

## Detailed findings by enforcement layer

### 1. Build-graph and compile-time boundary enforcement

- **Bazel has the strongest native build-level enforcement surface among the researched tools.** Its visibility system controls which targets may depend on which other targets, and the docs say target visibility should be used in production and that disabling it with `--check_visibility=false` should only be used for prototyping. In C++, Bazel also documents public versus private headers via `hdrs` and `srcs`, documents allowed direct inclusions, and states that direct include checking depends on toolchain support plus the `layering_check` feature. It further exposes `implementation_deps` so implementation-only dependencies do not leak headers to dependents.
- **CMake can encode boundaries, but its native model is target propagation, not architecture policy.** `target_include_directories` and `target_link_libraries` document `PUBLIC`, `PRIVATE`, and `INTERFACE` propagation, which is enough to structure component interfaces if the repo is target-disciplined. The docs also point to `cmake --graphviz` for graph export. The sources consulted do not show a first-class rule DSL for layer policies or location rules, so stronger enforcement is an inference that requires custom CI checks over the target graph or external tooling.

### 2. Source-level semantic enforcement

- **Clang-tidy is the main open-source hook for semantic architecture rules.** The docs say clang-tidy is the right place for linter-style and coding-style checks, explain how to write full checks, load plugins, and enable query-based custom checks. This makes it suitable for rules such as banning direct use of platform APIs from a domain layer, forbidding certain namespaces or types in selected directories, or requiring specific abstractions at call sites.
- **CodeQL can express codebase-specific architectural or framework rules.** GitHub's docs explicitly say custom queries can detect patterns specific to the application's architecture or frameworks and enforce organization-specific coding standards. That makes CodeQL relevant when the rule depends on semantic relationships, call paths, types, or framework use that a build graph alone cannot encode.
- **include-what-you-use improves physical dependency hygiene, not full architecture policy.** The project states that it analyzes includes, reports missing or superfluous includes, and suggests forward declarations. This is valuable for preventing accidental transitive dependencies and keeping headers honest, but the source does not position IWYU as a general architecture-rule engine.

### 3. Architecture-conformance and dependency-analysis tooling

- **CppDepend is explicitly positioned to detect and continuously monitor dependency cycles.** Its dependency-cycle feature page says it detects cycles between classes, namespaces, projects, or mixtures of them and continuously warns when a cycle is reintroduced. Its documentation also references rule support via CQLinq.
- **SciTools Understand supports architecture views and custom checks.** The manual states that Understand has architecture features for creating hierarchical aggregations of source code units. Later sections describe CodeCheck and violation reporting through custom checks. That makes it useful for architecture understanding plus project-specific checks, though the exact CI gating shape should be confirmed in a concrete evaluation.
- **SonarQube architecture is not currently a C++ answer in the consulted docs.** SonarQube Cloud architecture docs describe intended-architecture enforcement and issue raising, but the current language list excludes C++. This matters because teams often assume architecture-as-code products automatically cover C++.

## Architecture rule types supported by the researched tooling

The following mappings are **inferred from the sources above**:

- **Dependency direction between components or layers**
  Usually strongest at build-graph level with Bazel visibility and dependency declarations; possible in CMake only with disciplined target structure plus custom graph checks or external tooling.
- **Public-versus-private header exposure**
  Directly supported by Bazel's `hdrs` versus `srcs` model and include checking; approximated in CMake through target interface discipline and include propagation.
- **No direct inclusion of non-declared dependencies**
  Strongly supported by Bazel's documented header inclusion model and `layering_check`; partially supported by IWYU for hygiene and by custom analyzers elsewhere.
- **No cycles between components**
  Strong fit for architecture-conformance tools such as CppDepend and likely also external analysis setups built on target graphs.
- **Forbidden APIs, namespaces, types, or concrete dependencies in selected layers**
  Best fit for clang-tidy custom checks or CodeQL custom queries.
- **Location or ownership rules**
  Supported by SonarQube architecture in supported languages, and likely implementable for C++ through custom scripts, clang-tidy checks, CodeQL, or commercial architecture tools, but the exact mechanism depends on the tool.

## Gaps and open items

- CMake's official docs consulted describe propagation and graph export, but do not provide a direct, first-class architecture-rule language. The conclusion that custom CI or external analyzers are needed is a cross-source inference.
- Bazel's `layering_check` depends on toolchain support and is documented as supported by Bazel-provided toolchains only with clang on Unix and macOS. Applicability on other toolchains or platforms needs confirmation.
- CodeQL docs establish that custom queries can target architecture- or framework-specific patterns, but they do not, by themselves, provide a C++ architecture-rule library. Actual rule authoring effort remains an implementation concern.
- The commercial tools consulted clearly support architecture analysis, but CI-fail semantics, edition differences, and pricing were not researched here.
- C++20 modules and module-aware build tooling were not deeply researched in this slice; they may strengthen physical boundary enforcement, but that was not needed to answer the current question.

## Research boundary

Facts established above. Tool-stack selection, rollout shape, custom-rule design, and repo-specific enforcement strategy begin here and should be handled as a planning task, not as additional research in this file.
