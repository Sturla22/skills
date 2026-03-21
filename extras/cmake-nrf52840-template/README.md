# CMake nRF52840 Starter

This starter shows one concrete way to pair the repo's embedded workflow guidance with a small CMake firmware project for **Nordic nRF52840**.

## What this starter includes

- Pitchfork-style layout inside the starter
- checked-in CMake presets for host verification and Arm cross-builds
- a `gcc-arm-none-eabi` toolchain-file example
- configure-time architecture enforcement for a small layer stack
- a minimal semihosted hello-world firmware target
- host-side tests, including a negative test that proves an invalid dependency edge is rejected

## Layering model

- `starter_contracts`: shared capability interfaces
- `starter_domain`: pure-ish application logic; may depend only on `starter_contracts`
- `starter_platform`: target-facing implementation details; may depend only on `starter_contracts`
- `hello_nrf52840`: composition root; may depend on domain, platform, and contracts

Edit [`cmake/architecture.cmake`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template/cmake/architecture.cmake) to extend the allowed layer matrix.

## Host verification

```bash
cmake --preset host-debug
cmake --build --preset build-host-debug
ctest --preset test-host-debug
```

This builds the domain test and runs a negative configure test that is expected to fail when `domain` links directly to `platform`.

## Cross-build for nRF52840

```bash
cmake --preset nrf52840-debug
cmake --build --preset build-nrf52840-debug
```

The toolchain preset expects these binaries on `PATH`:

- `arm-none-eabi-gcc`
- `arm-none-eabi-g++`
- `arm-none-eabi-objcopy`
- `arm-none-eabi-size`

Build outputs land under `build/nrf52840-debug/`:

- `hello_nrf52840.elf`
- `hello_nrf52840.bin`
- `hello_nrf52840.hex`
- `hello_nrf52840.map`

## Target assumptions

- Bare-metal Cortex-M4F target
- flash origin `0x00000000`, size `1024K`
- RAM origin `0x20000000`, size `256K`
- no SoftDevice, no MBR offset, no bootloader reservation
- semihosting enabled through newlib `rdimon`

If your board uses a bootloader or reserved flash/RAM regions, update [`ld/nrf52840.ld`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template/ld/nrf52840.ld) before flashing.

## Files to copy first

- [`CMakeLists.txt`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template/CMakeLists.txt)
- [`CMakePresets.json`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template/CMakePresets.json)
- [`cmake/toolchains/gcc-arm-none-eabi.cmake`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template/cmake/toolchains/gcc-arm-none-eabi.cmake)
- [`cmake/architecture.cmake`](/home/sturlalange/Dev/my-claude-skills/extras/cmake-nrf52840-template/cmake/architecture.cmake)

Then adapt the layer names, linker script, and platform implementation to your board support package.
