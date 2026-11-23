# 05 · UML modelisation

Paper exercise first, then implementation (slide 68 and the course's UML practice page).

| Folder | System | Diagrams | Code |
|---|---|---|---|
| [`hospital/`](hospital/) | Hospital Management System | class diagram, 4 sequence diagrams, state diagram | `hospital.py` + tests |
| [`abcd_records/`](abcd_records/) | ABCD Records (mail-order CDs & tapes) | use case diagram, class diagram, 4 sequence diagrams | `abcd_records.py` + tests |

The diagrams are written in [Mermaid](https://mermaid.js.org/), which GitHub renders directly in Markdown. Mermaid has no native use case diagram, so the use case diagram is drawn as a flowchart: actors are stick figures in rounded boxes and use cases are stadium shapes.

Run: `pytest 05_uml_modelisation`
