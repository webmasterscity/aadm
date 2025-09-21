# Spec Vault & Orbit Ledger

Spec Vault almacena `intent-spec` mientras Orbit Ledger documenta la evolución temporal.

## Estructura de Carpetas (Referencia)

```
spec-vault/
  atoms/
    atom-743a2/
      2025-03-12T09-33-00Z.intent.yaml
      metadata.json
  compositions/
    auth-flow/
      2025-03-11T15-05-12Z.intent.yaml
  contracts/
    authentication_inputs/
      2025-03-10.intent.yaml
```

- Los archivos `intent.yaml` siguen `intent_spec.schema.json`.
- `metadata.json` agrega índices invertidos: etiquetas, dominio, criticidad, enlaces a cápsulas.

## Orbit Ledger

Ledger append-only que captura cada iteración de cápsulas:

```json
{
  "capsule_id": "omega-481",
  "timestamp": "2025-03-12T09:42:11Z",
  "initiator": "ai-agent://planner-7",
  "request_prompt_ref": "prompt://auth/extend-idn",
  "scope": {
    "nodes": ["atom-743a2", "test:property/email_unicode_fuzz"],
    "contracts": ["contract://authentication_inputs"]
  },
  "diff_ref": "git://aadm/commit/ab1234",
  "verifications": {
    "guardian_shield": "pass",
    "proof_forge": "pass",
    "impact_sentinel": "pass"
  },
  "telemetry": {
    "coverage_delta": 0.03,
    "mutation_kill_rate": 0.97,
    "latency_ms": 18350
  },
  "notes": "Añadido soporte IDN y se ajustaron pruebas fuzz"
}
```

Orbit Ledger debe exponer API de consulta para reconstruir narrativa:

- `GET /ledger/capsules/{id}`
- `GET /ledger/nodes/{node_id}`
- `GET /ledger/prompts/{prompt_ref}`

## Integridad y Seguridad

- Versionado WORM (Write Once, Read Many) para evitar alteraciones posteriores.
- Firmas digitales por `Trust Gate` para cada asiento del ledger.
- Replicación en almacenamiento frío para auditorías externas.

## Índices Sugeridos

- `by_node_id`: lista cápsulas que tocaron un nodo.
- `by_prompt_ref`: seguimiento de cumplimiento de cada intención.
- `by_agent`: rendimiento por agente IA.
- `by_invariant`: detectar intenciones que modifican invariantes críticos.

## Ciclo de Vida

1. `Ω-Capsule Builder` registra borrador de intención.
2. Tras validación completa, `Trust Gate` sella la cápsula y empuja el intent final a Spec Vault.
3. Orbit Ledger agrega asiento con diffs, verificaciones y telemetría.
4. `Helios Atlas` consume evento para actualizar grafos y resúmenes.

Esta especificación guía la implementación inicial de almacenamiento de intención y auditoría temporal.
