# Work anchor: proof before use

- base: main after rights-lineage merge `106d3b01cfc9065b7429d8771686dd6b282eaedd`
- branch: `feature/prove-right-before-use`
- owner: nsolland
- invariant: before a rights-sensitive use, the proposed user must prove a valid right for the exact use
- fail-closed: missing/unresolved proof -> `DENY_OR_DEFER`; rejected proof -> `DENY`
- legal boundary: contract admission is not a court judgment and does not create statutory rights
