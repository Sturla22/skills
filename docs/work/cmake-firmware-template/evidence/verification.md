# Verification

## Claim verified

The repo now includes a reusable embedded CMake starter with checked-in host and Arm cross-build presets, configure-time architecture enforcement, and a minimal nRF52840 hello-world firmware target.

## Behavior scenarios checked

- Given a host developer, the host preset configures, builds, and runs tests without hardware.
- Given an invalid `domain -> platform` dependency edge, configure fails and the negative test passes by expecting that failure.
- Given a local `gcc-arm-none-eabi` toolchain, the target preset configures and builds an nRF52840 firmware ELF plus post-build artifacts.
- Given the repo's Pitchfork rules and work-packet rules, the added files still pass the existing repo checks.

## Requirement / stakeholder-need coverage

- Concrete starter for adopters: covered by the new `extras/cmake-nrf52840-template/` project and README.
- Mechanical architecture enforcement: covered by the negative configure test.
- Toolchain-file example for `gcc-arm-none-eabi`: covered by target configure/build.
- Runnable target example for nRF52840: covered by successful cross-build; not flashed on hardware.

## Checks run

1. `python3 tools/cli.py check-work cmake-firmware-template`
   Result: pass
2. `python3 tools/cli.py check-layout`
   Result: pass
3. `cmake --preset host-debug`
   Working directory: `extras/cmake-nrf52840-template/`
   Result: pass
4. `cmake --build --preset build-host-debug`
   Working directory: `extras/cmake-nrf52840-template/`
   Result: pass
5. `ctest --preset test-host-debug`
   Working directory: `extras/cmake-nrf52840-template/`
   Result: pass (`hello_service_test`, `architecture_violation_rejected`)
6. `cmake --preset nrf52840-debug --fresh`
   Working directory: `extras/cmake-nrf52840-template/`
   Result: pass
7. `cmake --build --preset build-nrf52840-debug`
   Working directory: `extras/cmake-nrf52840-template/`
   Result: pass; produced `hello_nrf52840` and post-build binary/hex artifacts

## Results

- Host-side verification path works as documented.
- Architecture enforcement is not just documented; it is exercised by a negative test.
- Cross-build path works locally with the installed GNU Arm Embedded toolchain.
- Build artifacts are ignored via `.gitignore`, so checked-in presets do not pollute the repo diff.

## Compatibility / release-impact check

- Contract impact: additive
- SemVer expectation: `MINOR`
- `CHANGELOG.md`: updated under `Unreleased`

## Validation gap note

This verification demonstrates technical viability, not broad adopter fit. No separate validation study or downstream adopter trial was run in this slice.

## Residual risk

- The starter assumes the request meant `nRF52840`, not another Nordic part.
- The linker script assumes bare-metal flash and RAM with no bootloader or SoftDevice reservation.
- Semihosting output depends on a debug environment that supports newlib `rdimon`.

## Not verified

- Physical flashing, boot, and semihosted output on real nRF52840 hardware
- Any Nordic SDK, Zephyr, or board-support integration beyond the self-contained starter

## Verdict

Verified for the planned scope.
