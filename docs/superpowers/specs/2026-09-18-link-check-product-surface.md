# Spec: link-check-product-surface (P5)

## Problem
Lychee scanned README.md only with fail:false on PR.

## Requirements
1. Include docs/index.html in lychee args with README.md.
2. On pull_request, non-zero lychee exit fails the job (blocks merge).
3. Schedule/workflow_dispatch keep issue create/update behavior.
4. Action SHAs stay pinned.

## Research
research: skipped (local CI workflow only)
