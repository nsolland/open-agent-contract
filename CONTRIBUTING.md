# Contributing

Contributions are welcome through focused pull requests.

## Before opening a PR

- keep the contract vendor-neutral and independently usable;
- preserve the invariant `conformance != execution authorization`;
- do not make identity, transport, protocol membership, or agent capability imply authority;
- add or update tests for behavioral changes;
- update documentation and changelog for externally visible changes;
- do not commit credentials, customer data, private collaboration material, or unpublished third-party content.

## Validation

Run:

```bash
python -m pip install -e '.[test]'
pytest --tb=short
```

CI must be green before merge.

## Compatibility

Breaking contract or API changes require an explicit version change and migration note. Optional adapters must not become mandatory dependencies of the portable contract.
