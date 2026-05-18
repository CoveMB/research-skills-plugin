# Retrieval/Synthesis Control Fixtures

This directory contains two synthetic controlled fixtures that exercise optional retrieval and synthesis expectation fields.

- `retrieval-reject-decoy-sources` checks retrieval recall and precision separately from synthesis. It expects central synthetic source identifiers and rejects decoy or forbidden source selection.
- `synthesis-preserve-disagreement-uncertainty` checks synthesis faithfulness separately from retrieval. It requires claim boundaries, disagreement handling, and uncertainty preservation.

These fixtures do not assert real-source truth, real citations, field consensus, or publication readiness. They are small harness controls for the retrieval/synthesis distinction only.
