Vortex Tech Cyber Security Internship — Week 2

Hands-on with basic security tools: a Python password strength checker (with automated tests) and Nmap port scans of my own machine, my home network, and Nmap's official public test target.

Repository Structure
VortexTech_Internship_Week2/
├── README.md
├── WRITEUP.md
├── password_checker/
│   ├── passwordchecker.py
│   └── test_password_checker.py
└── scan_results/
    └── port_scan_results.md
Password Checker

passwordchecker.py rates a password as Very Weak, Weak, Medium, or Strong based on length (8+ chars), character variety (uppercase, lowercase, digit, special character), and a common/breached-password blacklist check.

Run it:

bash
python passwordchecker.py --demo              # built-in demo cases
python passwordchecker.py -p "YourPassword"   # check a single password
python passwordchecker.py                     # interactive mode

Run the automated tests:

bash
python test_password_checker.py

9/9 test cases pass, covering Very Weak, Weak, Medium, and Strong ratings.

Port Scanning

Performed with Nmap against:

localhost (own machine)
My home network range 192.168.18.0/24
scanme.nmap.org — Nmap's official public test host, which the Nmap project explicitly permits the community to scan

Full results and per-port service explanations are in scan_results/scan_results.md. The security analysis and reflection are in WRITEUP.md.

Ethics note: Only localhost, my own home network, and the explicitly authorized scanme.nmap.org test host were scanned. No unauthorized third-party network was accessed.

Author

Hadi Faheem 