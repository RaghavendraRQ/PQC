
# Post-Quantum Cryptography (PQC)

This repository contains Python-based implementations of Post-Quantum Cryptographic algorithms: **ML-KEM (Kyber)** and **ML-DSA**, aligned with [NIST’s standardization efforts](https://csrc.nist.gov/projects/post-quantum-cryptography).

## 🔒 Overview

With the rise of quantum computing, traditional cryptographic schemes are at risk. This project demonstrates practical implementations of lattice-based cryptographic primitives that are believed to be quantum-resistant.

### Implemented Algorithms

- **ML-KEM (Kyber)**: A Key Encapsulation Mechanism (KEM).
- **ML-DSA**: A digital signature scheme.

## 📂 Structure

```bash
PQC/
├── core/          # Core logic for ML-KEM and ML-DSA
├── main.py        # Entry point and testing
└── .idea/         # IDE-specific settings
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- NumPy

### Installation

```bash
git clone https://github.com/RaghavendraRQ/PQC.git
cd PQC
pip install -r requirements.txt
python main.py
```

## 🧪 Features

- Key generation
- Encapsulation/decapsulation (ML-KEM)
- Signature generation and verification (ML-DSA)
- Basic testing hooks (via `main.py`)

## 📈 Roadmap

- [ ] Add performance benchmarks
- [ ] Expand tests using `pytest`
- [ ] Support for NTRU or Dilithium
- [ ] Integrate with OpenSSL for hybrid testing

## 📘 References

- [NIST PQC Project](https://csrc.nist.gov/Projects/post-quantum-cryptography)
- Kyber Specification: https://pq-crystals.org/kyber/
- ML-DSA Technical Docs (to be added)

## 📄 License

MIT License

---

Contributions and feedback are welcome. Feel free to open issues or PRs!
