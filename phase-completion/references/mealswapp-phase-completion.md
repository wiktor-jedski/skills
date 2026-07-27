# Mealswapp Phase Completion Reference

## Inputs

- `docs/implementation/01_PLAN.md`: phase scope, exit criteria, and test plan.
- `docs/implementation/02_TASK_LIST.md`: authoritative task statuses and verification criteria.
- `docs/implementation/04_OPEN.md`: assumptions, clarifications, actions, and accepted deviations.
- `docs/implementation/implemented/{phase:02d}_PHASE_UAT.md`: generated project-owner acceptance document.
- `tools.md`: source description for Phase Completion skill responsibilities.

## Validation Commands

Prefer the aggregate command first:

```sh
python3 scripts/check.py
```

Use targeted commands when relevant to the phase or when the aggregate script delegates imperfectly:

```sh
cd backend && GOCACHE=$PWD/.go-cache GOMODCACHE=$PWD/.go-mod-cache go test ./...
cd backend && GOCACHE=$PWD/.go-cache GOMODCACHE=$PWD/.go-mod-cache go test ./internal/... -coverprofile=coverage.out
cd frontend && BUN_TMPDIR=$PWD/.bun-tmp BUN_INSTALL=$PWD/.bun-install bun run build
cd frontend && BUN_TMPDIR=$PWD/.bun-tmp BUN_INSTALL=$PWD/.bun-install bun test --coverage
bash scripts/start-services.sh
```

If present, also use the tooling scripts described in `tools.md`:

```sh
python3 scripts/validate-traceability.py
python3 scripts/verify-local-stack.py
python3 scripts/verify-frontend.py
```

## Traceability Checks

Verify:

- implemented source has concise `Implements DESIGN-*` comments near the relevant module, component, function, type, or generated block;
- referenced design files exist;
- comments identify a static design aspect, not just a file number;
- JSON files do not contain comments;
- JSON files that need traceability use sidecar `{filename}-trace.md` documents.

## UAT Document Shape

Use this structure unless the repository already has a newer phase UAT style:

```md
# Phase NN UAT - Title

## Scope

## Automated Verification

## Project Owner Acceptance Tests

### 1. Test Name

Steps:

Accept when:

## Phase NN Acceptance Decision
```

Add a short `Known note` or `Known notes` section when coverage exceptions, deferred generation, local-service requirements, or manual project-owner actions matter.

## Completion Checklist

Before marking the phase complete:

1. Every target phase task is `PASSED` or explicitly left lower with a reason.
2. Dependencies for `PASSED` tasks are also satisfied.
3. Aggregate and targeted verification commands have run or are listed as not run with reasons.
4. Coverage deviations are recorded in `04_OPEN.md`.
5. Traceability comments and JSON sidecars are present.
6. Phase UAT document exists and contains actionable acceptance tests.
7. Final response separates completed validation from project-owner acceptance still to be performed.
