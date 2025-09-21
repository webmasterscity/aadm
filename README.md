# 🧬 AADM 2.0 – IA-Native Architecture Fabric

> *El futuro del desarrollo no es escribir código, sino preservar intención y validar consecuencias.*

## 🌌 Visión

AADM nació para atomizar el software y hacerlo autocontenible. La versión 2.0 va más allá: convierte el repositorio en un tejido vivo donde múltiples IAs con ventanas de contexto limitadas pueden evolucionar sistemas masivos sin perder intención, sin romper contratos existentes y con validación automática al 100%.

La arquitectura se diseña desde las restricciones de los modelos: contexto finito, propensión a la deriva semántica, necesidad de feedback inmediato y verificación externa. Cada capa optimiza la experiencia de la IA y reduce las decisiones manuales del humano a simples prompts de alto nivel.

## ⚖️ Principios IA-Nativos

- **Todo es intención versionada.** El código es sólo una realización; la intención (prompts, contratos, decisiones) vive en artefactos formales auditables.
- **Contexto empaquetado jerárquicamente.** Ningún agente necesita más tokens que los del objetivo que ejecuta; la arquitectura entrega resúmenes Macro → Meso → Micro bajo demanda.
- **Ejecución en cápsulas verificables.** Cada modificación se limita a una cápsula con planes, diffs, pruebas mínimas y estrategia de rollback.
- **Verificación previa a integración.** Ningún cambio se acepta sin pasar por estática, pruebas diferenciales y simulación de impacto en contratos vecinos.
- **Autonomía medible.** Telemetría y trazabilidad son parámetros de la arquitectura, no complementos.

## 🧠 Arquitectura de Capas

### 1. Plano de Conocimiento: Helios Atlas

| Componente | Propósito |
|------------|-----------|
| **Helios Atlas** | Grafo semántico del repositorio. Indexa archivos, átomos, contratos, tests, dependencias y relaciones de dominio. Mantiene resúmenes jerárquicos (Macro, Meso, Micro) y embeddings contextualizados. |
| **Context Packs** | Paquetes de contexto generados on-demand: resumen textual, firmas de invariantes, consultas frecuentes, enlaces a pruebas críticas. Ajusta tamaño al límite de tokens solicitado por el agente. |
| **Drift Watchdog** | Detecta divergencias entre resúmenes y código de origen; dispara regeneración de embeddings y alerta a gobernanza. |

**Patrones clave:**
- Indexación incremental tras cada cápsula para mantener el grafo sincronizado.
- Firmas sintácticas y semánticas que permiten detectar colisiones cuando varios agentes editan áreas adyacentes.

### 2. Plano de Intención: Spec Vault & Orbit Ledger

| Componente | Propósito |
|------------|-----------|
| **Spec Vault** | Almacén inmutable de `intent-spec` para cada función, contrato, flujo y requisito. Incluye: prompt original, contexto usado, restricciones, métricas objetivo. |
| **Orbit Ledger** | Bitácora temporal de decisiones: plan → cambio → validación → despliegue. Permite reproducir cualquier ciclo y rastrear por qué se tomó cada decisión. |
| **Prompt Lint** | Linter de instrucciones humanas. Normaliza formato, detecta ambigüedades y verifica que las peticiones apunten a elementos registrados en Helios Atlas. |

**Beneficio:** cada IA puede reconstruir intención original incluso si el código cambió múltiples veces, evitando drift semántico.

### 3. Plano de Ejecución: Ω-Capsules

| Componente | Propósito |
|------------|-----------|
| **Ω-Capsule Builder** | Ensambla la cápsula de trabajo con el objetivo, contexto relevante, rutas de impacto, contratos afectados, tests obligatorios, scripts de validación y plan de rollback. |
| **Scope Weaver** | Determina con precisión el alcance: identifica átomos vecinos, dependencias semánticas y políticas a respetar antes de permitir cambios. |
| **Delta Crafter** | Agente especializado en generación de código que opera dentro de la cápsula y sólo modifica los elementos autorizados. |

**Garantías:**
- Las cápsulas son reproducibles, exportables y auditables.
- Al finalizar, se adjunta diff, justificativos y evidencias de verificación para aprobación automática.

### 4. Plano de Seguridad y Verificación: Guardian Shield & Proof Forge

| Componente | Propósito |
|------------|-----------|
| **Guardian Shield** | Orquesta análisis estático, linters, validaciones de seguridad y verificación simbólica donde aplique. |
| **Proof Forge** | Ejecuta `test suites` asociadas, pruebas diferenciales, fuzz y ataques específicos definidos en manifiestos. Implementa el "semáforo cuántico": verde sólo si todas las validaciones pasan. |
| **Impact Sentinel** | Simula escenarios críticos con contratos vecinos y confirma que las invariantes registrados en Spec Vault continúan vigentes. |

**Resultado:** cero integración sin evidencia; los fallos se devuelven a Delta Crafter con el plan de remediación propuesto.

### 5. Plano de Gobernanza y Autonomía

| Componente | Propósito |
|------------|-----------|
| **Telemetry Spine** | Registra métricas de cada cápsula: cobertura efectiva, mutación, latencia de validación, tasa de reversión, consumo de tokens. |
| **Trust Gate** | Sistema de autorizaciones y políticas. Valida que la cápsula cumpla objetivos, límites de seguridad y reglas de despliegue antes de merge virtual. |
| **Autonomy Loop** | Observa patrones de fallas, propone mejoras de tooling, reentrena prompts o ajusta heurísticas de Scope Weaver para maximizar efectividad. |

## 🧾 Manifiestos Enriquecidos (`intent-spec`)

Cada átomo ahora cuenta con dos artefactos complementarios:

```yaml
# email-format-validator.intent.yaml
identity:
  id: atom-743a2
  name: email-format-validator
  version: 2.1.0
  hash: sha256:...

intent:
  prompt_signature: "validate emails against RFC 5322 with i18n"
  requirements:
    - "Failed emails must return error.reason"
    - "Support IDN via punycode"
  invariants:
    - label: deterministic
      description: "Same input → same output"
    - label: null_safety
      description: "Never return null fields"

contracts:
  input_schema: ...
  output_schema: ...
  side_effects: []

risk_profile:
  criticality: medium
  blast_radius: "authentication"
  dependencies:
    semantic:
      - regex-library
      - unicode-normalizer

validation:
  required_tests:
    - unit/email_validator_spec
    - property/email_validator_properties
    - fuzz/email_unicode_fuzz
  rollback_strategy: revert_to: 2.0.5
```

Los manifest tradicionales (`*.manifest.yaml`) siguen describiendo detalles técnicos, pero ahora se sincronizan con `intent-spec` para garantizar que cualquier cambio preserve intención y contratos.

## 🔄 Flujo Operativo de un Agente

1. **Recepción de Prompt** → `Prompt Lint` valida y enruta.
2. **Planificación** → `Planner` consulta Helios Atlas y elige subtareas; cada subtarea genera una Ω-Capsule con Scope Weaver.
3. **Generación** → `Delta Crafter` modifica artefactos dentro de la cápsula basándose en context packs micro.
4. **Verificación** → `Guardian Shield` + `Proof Forge` ejecutan el semáforo cuántico.
5. **Revisión** → `Sage Reviewer` produce explicación estructurada, riesgos residuales y recomendaciones.
6. **Integración** → `Trust Gate` valida políticas; al aprobar, Helios Atlas y Spec Vault se actualizan; Orbit Ledger registra el ciclo.

## 🧰 Convivencia Multi-Agente

- **Shards de Dominio:** cada subdominio (ej. `payments://`, `ml-pipeline://`) mantiene pipelines independientes y cachés de contexto, pero sincroniza resúmenes Macro en Helios Atlas global.
- **Locks Semánticos:** Scope Weaver aplica bloqueos finos usando firmas semánticas para permitir trabajo paralelo sin colisiones.
- **Context Fabric:** si varios agentes tocan el mismo dominio, se construye un "context delta" común que comparte invariantes y cambios pendientes.


## 💻 Ejemplos Multilenguaje

Estos ejemplos viven en `examples/` y muestran cómo un mismo contrato se expresa en distintos runtimes.

### Python – Atom funcional
```python
# examples/python/email_validator.atom.py
import re

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_email(email: str) -> dict:
    valid = bool(EMAIL_PATTERN.match(email))
    return {"valid": valid, "error": None if valid else "Invalid format"}
```

```yaml
# examples/python/email_validator.intent.yaml
identity:
  id: atom-email-validator-py
  name: email-format-validator
  version: 2.1.0
  hash: sha256:<pending>
intent:
  prompt_signature: "python email validator rfc5322"
  requirements:
    - "Return structure {valid, error}"
contracts:
  input_schema: {type: object, properties: {email: {type: string}}}
  output_schema: {type: object, properties: {valid: {type: boolean}, error: {type: string}}}
validation:
  required_tests:
    - {id: unit/test_email_validator.py, type: unit, command: "pytest -k email_validator"}
  rollback_strategy: {type: revert, target_version: 2.0.5}
```

### Flutter (Dart) – Servicio UI-friendly
```dart
// examples/flutter/lib/atoms/email_validator_atom.dart
const String emailPattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$';

typedef EmailValidationResult = Map<String, Object?>;

EmailValidationResult validateEmailAtom(String email) {
  final regex = RegExp(emailPattern);
  final isValid = regex.hasMatch(email);
  return {
    'valid': isValid,
    'error': isValid ? null : 'Invalid format',
  };
}
```

### PHP – Átomo interoperable
```php
<?php // examples/php/email_validator_atom.php
function validate_email_atom(string $email): array {
    $valid = filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    return [
        'valid' => $valid,
        'error' => $valid ? null : 'Invalid format',
    ];
}
```

Cada variante comparte intención a través de `intent-spec` equivalente, permitiendo que Helios Atlas y Spec Vault sincronicen invariantes independientemente del lenguaje.

## 🧪 Estrategia de Testing Total

- **Mandatory Suites:** cada cápsula declara suites mínimas; Trust Gate falla si alguna falta.
- **Regression Mesh:** Proof Forge selecciona pruebas de regresión basadas en impacto semántico, no sólo en dependencias directas.
- **Mutation & Property as First-Class:** se exige `mutation_kill_rate` objetivo por dominio y propiedades formales con auto-verificación.
- **Telemetry Feedback:** métricas alimentan Autonomy Loop para sugerir nuevas pruebas donde haya huecos.

## 🛠 Ruta de Implementación Sugerida

1. **Fase Atlas**
   - Modelar esquema de Helios Atlas (nodos, relaciones, resúmenes).
   - Prototipar generación de Context Packs y Drift Watchdog.

2. **Fase Intención**
   - Definir formato `intent-spec` y poblar Spec Vault desde componentes piloto.
   - Integrar Prompt Lint con la interfaz de humanos/IA para validar instrucciones.

3. **Fase Cápsulas**
   - Implementar Ω-Capsule Builder con plantillas y pipelines de validación.
   - Orquestar agentes especializados (Scope Weaver, Delta Crafter, Sage Reviewer).

4. **Fase Verificación**
   - Automatizar Guardian Shield + Proof Forge en CI/CD.
   - Definir reglas del Trust Gate y política de rollback.

5. **Fase Gobernanza**
   - Desplegar Telemetry Spine y tableros de autonomía.
   - Activar Autonomy Loop para retroalimentar mejoras de tooling.

## 📚 Glosario Rápido

- **Helios Atlas:** grafo semántico de conocimiento.
- **Context Pack:** paquete de resumen escalado por tokens.
- **Spec Vault:** repositorio de intenciones y contratos formales.
- **Orbit Ledger:** bitácora de decisiones y ejecuciones.
- **Ω-Capsule:** contenedor reproducible para modificaciones con verificación completa.
- **Guardian Shield / Proof Forge:** sistema dual de validación (estática + dinámica).
- **Trust Gate:** puerta de gobernanza previa a integración.

---

AADM 2.0 transforma la arquitectura en una experiencia diseñada para agentes: la IA recibe exactamente el contexto que necesita, ejecuta cambios en cápsulas controladas y entrega evidencia verificable antes de integrar. Los humanos sólo definen la intención de alto nivel; el tejido hace el resto.
