# Helios Atlas Schema Blueprint

Helios Atlas modela el repositorio como un grafo dirigido etiquetado. El objetivo es ofrecer consultas de contexto jerárquico para agentes con ventanas de tokens limitadas y detectar impactos cruzados entre átomos.

## Entidades Principales

### Node Types

| Tipo | Descripción | Atributos Clave |
|------|-------------|-----------------|
| `module` | Paquete lógico o carpeta raíz de dominio. | `id`, `name`, `domain`, `owner`, `risk_score` |
| `atom` | Unidad mínima de implementación con su manifiesto. | `id`, `intent_id`, `language`, `size_metrics`, `hash`, `invariants` |
| `composition` | Flow declarativo que une átomos. | `id`, `inputs`, `outputs`, `graph_signature`, `constraints` |
| `test` | Caso de prueba, suite o propiedad. | `id`, `type`, `coverage_scope`, `criticality` |
| `contract` | Esquema/invariante formal compartido. | `id`, `spec_ref`, `level` (API, dominio, sistema) |
| `prompt` | Intención original de humano/IA. | `id`, `source`, `normalized_text`, `tags` |
| `artifact` | Documentos, migraciones, assets. | `id`, `artifact_type`, `checksum` |

### Edge Types

| Tipo | Origen → Destino | Semántica |
|------|------------------|-----------|
| `declares` | `atom → contract` | El átomo implementa o depende del contrato. |
| `validates` | `test → atom/composition` | La prueba cubre ese nodo con nivel de criticidad. |
| `composes` | `composition → atom` | La composición referencia al átomo. |
| `depends_on` | `atom/composition → atom/composition` | Dependencia semántica o técnica. |
| `emits` | `prompt → intent` | Un prompt origina una intención específica. |
| `documents` | `artifact → node` | Un artefacto describe o impacta al nodo. |
| `touches` | `capsule → node` | Historial de cápsulas que modifican nodos. |

## Jerarquía de Resúmenes

Cada nodo mantiene versiones de resumen:

```yaml
summary:
  macro:
    tokens: 2048
    embedding: vector<1536>
    outline: "Panorama del dominio y objetivos"
  meso:
    tokens: 512
    key_points:
      - "Uso principal"
      - "Dependencias críticas"
  micro:
    tokens: 128
    fields:
      signature: "validate_email(email) -> {valid, error}"
      constraints:
        - deterministic
        - null_safety
```

Los resúmenes se reconstruyen cuando cambia `hash` o `intent_revision`.

## Context Packs

Se generan bajo demanda combinando nodos y deltas:

```yaml
context_pack:
  request:
    target_tokens: 2800
    focus_nodes:
      - atom:email-format-validator
      - contract:authentication_inputs
    capsule_id: omega-481
  contents:
    macro_outline: |
      ...
    meso_details:
      - node: atom:email-format-validator
        summary_ref: v2025.03.12-1
        change_delta:
          since_capsule: omega-430
          highlights:
            - "Añadido soporte IDN"
            - "Pruebas fuzz unicode"
    micro_snippets:
      - file: src/auth/email_validator.py
        excerpt_hash: sha256:9a8b...
        start_line: 4
        end_line: 22
    related_tests:
      - test: property/email_unicode_fuzz
        command: `pytest tests/property/test_email_unicode_fuzz.py -k atom_743a2`
    invariants:
      - deterministic
      - null_safety
```

## Drift Watchdog

- Recalcula embeddings para nodos afectados por cápsulas aprobadas.
- Compara `macro.embedding` con el histórico; si el coseno < 0.92, marca potencial deriva.
- Lanza tareas de revisión para regenerar resúmenes y validar contratos.

## API de Consulta

- `GET /atlas/nodes/{id}` → retorna nodo + resúmenes + conexiones directas.
- `POST /atlas/context-pack` → genera pack con restricciones de tokens.
- `POST /atlas/impact-diff` → lista nodos afectados por cápsula propuesta.
- `POST /atlas/search` → búsqueda semántica / estructural con filtros (`type=atom`, `invariant=deterministic`).

## Estrategia de Persistencia

- Grafo almacenado en base orientada a grafos o triplestore (ej. Neo4j, Neptune, Dgraph); embeddings en almacén vectorial.
- Actualizaciones transaccionales post-`Trust Gate`; las cápsulas no aprobadas no alteran Helios.

## Métricas Clave

- `context_pack_latency_ms`
- `impact_radius_mean`
- `summary_drift_rate`
- `capsule_conflict_density`

Este blueprint es el punto de partida para implementar Helios Atlas y sus servicios asociados.
