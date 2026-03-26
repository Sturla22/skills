---
name: security-threat-modeling
description: Identify security threats, attack surfaces, and trust boundaries for firmware and connected-device changes. Use when adding connectivity, authentication, storage of secrets, OTA update paths, or external interfaces. Complements safety-risk-scan which covers reliability failure modes.
allowed-tools: Read, Grep, Glob, Bash
---

# Security Threat Modeling

Identify intentional-adversary risks early for embedded firmware and connected devices.

## Process

1. **Identify trust boundaries and data flows** — list what crosses a trust boundary and where control changes hands: BLE, UART, USB, flash storage, debug ports, bootloader, OTA channel, cloud/API, sensor inputs.
2. **Enumerate assets** — keys, credentials, firmware images, user data, calibration, configuration, device identity, debug unlock state.
3. **Apply STRIDE per element** — for each asset, interface, and boundary, ask:
   - **S**poofing: can an attacker impersonate a device/user/service?
   - **T**ampering: can data, code, or state be modified?
   - **R**epudiation: can actions be denied or unaudited?
   - **I**nformation Disclosure: can secrets or sensitive data leak?
   - **D**enial of Service: can the system be made unavailable?
   - **E**levation of Privilege: can an attacker gain more authority?
   Mark any category **not applicable** with a short reason.
4. **Rate each threat** — use Likelihood × Impact, or High/Medium/Low if that is sufficient for the context.
5. **Map mitigations** — for each threat, name the concrete countermeasure; if none exists, mark it as a gap.

## Common firmware attack surfaces

- [ ] Debug/JTAG/SWD ports left enabled in production
- [ ] Unencrypted or unsigned OTA updates
- [ ] Plaintext secrets in flash or source
- [ ] Unauthenticated external interfaces (BLE, UART, USB)
- [ ] Bootloader without signature verification
- [ ] No anti-rollback protection
- [ ] Side-channel leakage (timing, power)
- [ ] Unprotected flash readout (no RDP/APPROTECT)

## Standard mitigations reference

| Surface | Standard mitigation |
|---|---|
| Debug port | Disable or lock in production; use fuse-based protection |
| OTA | Signed images, anti-rollback counter, A/B bank with fallback |
| Secrets | Hardware key storage (secure element, TrustZone); never plaintext in flash |
| External interfaces | Authentication, input validation, rate limiting |
| Bootloader | Chain of trust; signature verification before jump |
| Flash readout | Enable RDP/APPROTECT at manufacturing |

## Threat findings template

For each item, capture:
- element / boundary
- STRIDE category
- attack scenario
- likelihood / impact
- concrete mitigation or gap
- residual risk

## Guardrails

- Do not mark a threat as mitigated without naming the concrete countermeasure.
- Do not skip STRIDE categories; mark **not applicable** with reason.
- Threats rated **High** that lack mitigations block shipping.
- If threat modeling reveals missing architectural support (for example, no secure element or no secure boot), escalate to `firmware-architect`.

## Relation to safety-risk-scan

This skill covers security: intentional adversaries, abuse, and compromise paths. `safety-risk-scan` covers reliability: unintentional failure modes. Both may apply to the same change. When they overlap, cross-reference the shared finding (for example, a corrupt OTA image can be both a security and safety concern).

## Done-when

- trust boundaries, assets, and data flows are listed
- STRIDE has been applied to each relevant element, with not-applicable reasons where needed
- threats are rated and mapped to concrete mitigations or explicit gaps
- High-rated unmitigated threats are marked as blockers
- overlap with safety-risk-scan is noted where relevant

## Output

- trust boundaries and assets
- STRIDE findings
- threat ratings
- mitigations / gaps
- blockers
- cross-references to safety-risk-scan, if any
