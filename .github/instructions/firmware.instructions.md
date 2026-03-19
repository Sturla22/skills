---
applyTo: "**/*.c,**/*.cc,**/*.cpp,**/*.cxx,**/*.h,**/*.hh,**/*.hpp,**/*.hxx,**/*.inc,**/*.ld,**/*.lds,**/*.s,**/*.S,**/*.overlay,**/*.dts,**/*.dtsi,**/Kconfig,**/Kconfig.*,**/prj.conf"
---
# Firmware-specific instructions

- Keep direct hardware access narrow and intentional.
- Make execution context explicit when relevant: ISR, task/thread, callback, startup, shutdown.
- Avoid hidden global state and hidden ownership transfer.
- Prefer explicit units in names, comments, or types.
- Do not add speculative abstraction unless the near-term caller pressure is real.
- For stateful logic, name valid states and transition triggers.
- For retries, timeouts, queues, buffers, and watchdog interactions, make the failure behavior explicit.
- For platform changes, preserve the existing contract unless the change explicitly updates the contract and tests.
- Add or update host-side seams when they materially improve verification.
