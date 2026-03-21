# Work Plan

## Storage

- Work ID: `cpp-static-analysis-stack`
- File path: `docs/work/cpp-static-analysis-stack/plan.md`
- Source brief: `docs/work/cpp-static-analysis-stack/brief.md`

## Problem statement
Choose and document a concrete C++ static-analysis operating model for this repo, then expose it through the repo’s normal script and Make surfaces.

## Stakeholders / system context
- Immediate consumer is the requester
- Secondary consumers are maintainers and adopters of the embedded CMake starter
- Existing context comes from the earlier research packet plus the current repo CI/build surfaces

## Scope
- Recommend one primary enforced analyzer and the intended execution points
- Add the smallest repo-owned command surface needed to run it
- Add minimal `pre-commit` framework wiring for the local hook path
- Update starter and project guidance to match

## Non-goals
- Multi-tool mandatory gate stack
- Hosted analysis platform integration
- Full enterprise security scanning rollout

## Requirements / constraints / assumptions to keep visible
- Keep CI YAML thin
- Reuse current CMake presets and compile databases
- Prefer a practical baseline that already passes on the current starter
- Keep the recommendation specific about what is deferred

## Public contract / compatibility impact
The documented static-analysis command in project guidance changes from `TODO` to a real command.

## SemVer / changelog expectation
Changelog update required under `Unreleased`.

## Key behavior rules / scenarios
- Editor guidance must distinguish host and target compile databases
- The `pre-commit` package hook and CI should use the same primary repo-owned analyzer command for this repo’s current size
- The analyzer script must be able to handle target-side Arm C++ includes

## Trade studies / decision points
- Primary enforced analyzer: choose `clang-tidy`
- Secondary analyzers: defer `cppcheck`, CodeQL, SonarQube, and PVS-Studio from mandatory integration for now

## Preferred test strategy
- Run the new static-analysis command locally
- Validate the `pre-commit` config and run the static-analysis hook through the framework
- Rerun `make ci-checks`
- Validate the work packet with `tools/cli.py check-work`
- Resync generated Claude instructions if the canonical project file changes

## Validation plan
- Confirm the starter README is sufficient to explain editor and gating usage
- Confirm the repo command succeeds on the current template without manual cleanup

## Walking skeleton
1. Record the repo-specific recommendation in a work packet
2. Add a starter `.clang-tidy` profile and repo-owned check script
3. Wire the script into `Makefile`, minimal `pre-commit` config, and CI entrypoints
4. Update docs and generated instruction surfaces
5. Run verification commands and capture the result

## Minimal configuration / iteration target
One new analyzer script, one new starter config file, lightweight doc updates, and one recommendation packet.

## Exit criteria / milestone criteria
- `make check-static-analysis` works locally
- `python3 -m pre_commit validate-config` passes
- `python3 -m pre_commit run --all-files static-analysis` passes
- `make ci-checks` still passes
- `tools/cli.py sync` has been run if canonical generated surfaces changed
- `tools/cli.py check-work cpp-static-analysis-stack` passes

## Plan steps
1. Define the repo-specific analyzer stack and record the recommendation.
2. Add a repo-owned `clang-tidy` command surface that covers both host and target starter translation units.
3. Wire the command into `Makefile`, minimal `pre-commit` integration, CI bootstrap, and the normal CI aggregate target.
4. Update starter docs and canonical project instructions.
5. Verify commands, sync generated files, and record evidence.

## Parallel lanes

For each active lane, capture:
- lane name
- owner
- write surface
- worktree / isolation plan
- merge point / integration checkpoint

No active parallel lanes.

## Ownership boundaries
- This slice chooses the baseline and wires the repo command
- Adding more analyzers or hosted platforms is intentionally deferred

## Blockers / dependencies
- `clang-tidy` must be available locally and in CI
- The target-side Arm include path issue must be handled in the repo script

## Verification gates
- `make check-static-analysis`
- `python3 -m pre_commit validate-config`
- `python3 -m pre_commit run --all-files static-analysis`
- `python3 tools/cli.py sync`
- `make ci-checks`
- `python3 tools/cli.py check-work cpp-static-analysis-stack`

## Risks / unknowns
- Target-side analysis may need environment-specific compiler include handling
- Overly broad check sets may create noisy failures and reduce adoption
- A second analyzer gate would add cost and complexity without clear signal yet

## Escalation triggers
- If `clang-tidy` cannot be made to analyze target-side files reliably with the current toolchain
- If the recommended baseline turns out to be too noisy to keep on by default
