# Ω-Capsule Operational Pipeline

Este documento detalla el lifecycle de una cápsula desde el prompt inicial hasta la integración mediante Trust Gate.

## Estados de la Cápsula

1. `draft` – generado por Ω-Capsule Builder con información inicial.
2. `scoped` – Scope Weaver resolvió nodos, dependencias y políticas.
3. `in_progress` – Delta Crafter ejecuta modificaciones dentro del sandbox.
4. `verification` – Guardian Shield, Proof Forge e Impact Sentinel evaluando evidencias.
5. `review` – Sage Reviewer produce narrativa, riesgos residuales y sugerencias.
6. `approved` – Trust Gate valida requisitos; cápsula lista para merge virtual.
7. `sealed` – Registro final en Orbit Ledger y actualización en Helios Atlas / Spec Vault.

## Artefactos de la Cápsula

```
omega-capsules/
  omega-481/
    capsule.yaml
    plan.md
    context_pack.meso.yaml
    diffs/
      repo.patch
    validations/
      guardian_shield.json
      proof_forge.json
      impact_sentinel.json
    telemetry.json
```

### `capsule.yaml`

```yaml
capsule_id: omega-481
prompt_ref: prompt://auth/extend-idn
objective: "Añadir soporte IDN a email-format-validator"
status: verification
scope:
  nodes:
    - atom-743a2
    - test:property/email_unicode_fuzz
  contracts:
    - contract://authentication_inputs
context:
  packs:
    - ref: atlas://context-packs/cp-2025-03-12-09-31
      granularity: meso
  invariants:
    - deterministic
    - null_safety
validation_plan:
  required:
    - guardian_shield
    - proof_forge
    - impact_sentinel
rollback_strategy:
  type: revert
  target_version: 2.0.5
  automated: true
```

## Guardian Shield

- Ejecuta linters específicos por lenguaje.
- Corre análisis estático (ej. `mypy`, `eslint`, `bandit`).
- Verifica invariantes declarados (`deterministic`, `null_safety`) mediante reglas formales.
- Salida estándar:

```json
{
  "capsule_id": "omega-481",
  "status": "pass",
  "checks": [
    {"name": "eslint", "status": "pass", "duration_ms": 3820},
    {"name": "bandit", "status": "pass", "duration_ms": 1475},
    {"name": "invariant:null_safety", "status": "pass"}
  ]
}
```

## Proof Forge

- Determina suites mínimas desde `intent-spec`.
- Ejecuta pruebas diferenciales contra versión base.
- Calcula métricas: cobertura efectiva, `mutation_kill_rate`, latencia.
- Salida ejemplo:

```json
{
  "capsule_id": "omega-481",
  "status": "pass",
  "tests": [
    {"id": "unit/email_validator_spec", "result": "pass", "duration_ms": 930},
    {"id": "property/email_unicode_fuzz", "result": "pass", "duration_ms": 14300},
    {"id": "regression_mesh", "result": "pass", "duration_ms": 6400}
  ],
  "metrics": {
    "coverage_delta": 0.03,
    "mutation_kill_rate": 0.97
  }
}
```

## Impact Sentinel

- Extrae contratos vecinos desde Helios Atlas.
- Ejecuta simulaciones con datos de escenarios críticos.
- Evalúa que invariantes externos continúen vigentes.
- Respuesta típica:

```json
{
  "capsule_id": "omega-481",
  "status": "pass",
  "simulations": [
    {
      "contract": "contract://authentication_inputs",
      "scenario": "unicode-login",
      "result": "pass",
      "notes": "Tokens generados correctamente"
    }
  ]
}
```

## Integración con Trust Gate

Trust Gate evalúa:

- Estado `pass` de las tres verificaciones.
- Cumplimiento de políticas (`criticality`, `blast_radius`, aprobaciones humanas si aplica).
- Presencia de plan de rollback automatizable.
- Actualización de telemetría: latencia total, gasto de tokens, consumo energético estimado.

### Resultado de Trust Gate

```json
{
  "capsule_id": "omega-481",
  "decision": "approve",
  "policy_checks": [
    {"policy": "coverage >= baseline", "status": "pass"},
    {"policy": "mutation_kill_rate >= 0.9", "status": "pass"}
  ],
  "approved_by": "agent://trust-gate-1",
  "timestamp": "2025-03-12T09:43:51Z"
}
```

Tras aprobación:

1. Se sella la cápsula (`sealed`).
2. Spec Vault recibe la nueva versión del `intent-spec`.
3. Orbit Ledger agrega asiento y firma digital.
4. Helios Atlas recalcula resúmenes y embeddings relevantes.
5. Telemetry Spine ingiere métricas para el Autonomy Loop.

## Automatización de Regresiones

Proof Forge mantiene una matriz `regression_mesh` alimentada por Impact Sentinel:

- Selecciona pruebas basadas en similitud semántica (`cosine > 0.85`) con el nodo editado.
- Prioriza suites históricamente propensas a fallar cuando se toca el mismo contrato.

## Gestión de Fallos

- Si cualquier verificación falla, Trust Gate bloquea la cápsula y crea tareas de remediación.
- Orbit Ledger registra el fallo con estado `rejected` y métricas para análisis posterior.
- Autonomy Loop aprende del fallo y puede ajustar heurísticas de Scope Weaver o sugerir nuevas pruebas.

Este pipeline estandariza el trabajo multi-IA garantizando trazabilidad, verificaciones obligatorias y control automático de regresiones.
