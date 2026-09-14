# 🔐 Vortex Tech Cyber Security Internship — Week 2

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Nmap](https://img.shields.io/badge/Nmap-7.98-green?logo=nmap&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

Hands-on with basic security tools: a Python password strength checker (with
automated tests) and Nmap port scans of my own machine, my home network, and
Nmap's official public test target.

---

## 📁 Repository Structure

```
VortexTech_Internship_Week2/
├── README.md
├── WRITEUP.md
├── password_checker/
│   ├── passwordchecker.py
│   └── test_password_checker.py
└── scan_results/
    └── scan_results.md
```

---

## 🔑 Password Checker

`passwordchecker.py` rates a password as **Very Weak**, **Weak**, **Medium**,
or **Strong** based on:

- Length (8+ characters)
- Character variety — uppercase, lowercase, digit, special character
- A common/breached-password blacklist check

**Run it:**
```bash
python passwordchecker.py --demo              # built-in demo cases
python passwordchecker.py -p "YourPassword"   # check a single password
python passwordchecker.py                     # interactive mode
```

**Run the automated tests:**
```bash
python test_password_checker.py
```
✅ 9/9 test cases pass, covering all four rating tiers.

---

## 🌐 Port Scanning

Performed with [Nmap](https://nmap.org/) against:

| Target | Scope |
|---|---|
| `localhost` | Own machine |
| `192.168.18.0/24` | Own home network |
| `scanme.nmap.org` | Nmap's official public test host — scanning explicitly permitted by the operator |

Full results and per-port service explanations: [`scan_results/scan_results.md`](./scan_results/scan_results.md)
Security analysis and reflection: [`WRITEUP.md`](./WRITEUP.md)

> ⚠️ **Ethics note:** Only localhost, my own home network, and the explicitly
> authorized scanme.nmap.org test host were scanned. No unauthorized
> third-party network was accessed.

---

## 👤 Author

**Hadi Faheem**
