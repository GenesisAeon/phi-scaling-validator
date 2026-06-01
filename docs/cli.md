# CLI Reference

## `phi-validate` — Package 38

### `phi-validate run`

Run all Phi^(1/3) validation analyses across CREP Spectrum, beta-clusters, Q4, EML, and v_RIG.

```bash
phi-validate run
phi-validate run --json          # machine-readable output
phi-validate run --packages 17-37
```

Output:
```
Phi^(1/3) Universal Scaling Validator -- P38
Phi^(1/3) = 1.17398500   v_RIG = 1352.06 km/s

Domain          Mean ratio   p-value   Confirmed
CREP Spectrum   1.36895      0.1444       x
beta-Clusters   1.83000      0.0231       v
Universality score: 50% of tested domains
```

### `phi-validate report`

Print detailed per-domain report with notes and confidence intervals.

```bash
phi-validate report
```

### `phi-validate zenodo`

Print Zenodo-compatible metadata record (JSON).

```bash
phi-validate zenodo
phi-validate zenodo > zenodo_record.json
```

---

## `diamond` — Scaffolder

### `diamond scaffold`

Create a new Python project from a template.

```
Usage: diamond scaffold [OPTIONS] PROJECT_NAME

Options:
  -t, --template TEXT    Template: minimal | genesis  [default: minimal]
  --author TEXT          Author name
  --description TEXT     Short description
  --dry-run              Preview without writing files
```

```bash
diamond scaffold my-physics-tool --template genesis --author "Johann Römer"
```

### `diamond list-templates`

```bash
diamond list-templates
```

| Template | Description |
|----------|-------------|
| `minimal` | Clean Python package |
| `genesis` | Adds `domains.yaml` + entropy-table bridge (GenesisAeon preset) |

### `diamond validate`

Validate a project directory against diamond-setup conventions.

```bash
diamond validate path/to/my-project
diamond validate          # current directory
```
