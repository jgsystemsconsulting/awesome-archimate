# Spec: pin-validate-setup-python (P6)

## Problem
validate.yml uses mutable actions/setup-python@v5 while sibling workflows pin full SHAs.

## Requirement
Pin setup-python to the full commit SHA that tag v5 currently resolves to, with `# v5` comment, matching sibling style. validate.yml still runs check_release.py. No other workflow changes.

## Research
research: skipped (local workflow pin only; SHA resolved from GitHub API tag v5 -> a26af69be951a213d495a4c3e4e4022e16d87065)
