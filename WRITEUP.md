Week 2 Write-Up: Password Strength Checker & Network Port Scanning

Program: Vortex Tech Cyber Security Internship — Week 2 (Beginner-Intermediate) Author: Hadi Faheem

1. Objective

This task covered two exercises: building a password strength evaluator in Python, and performing legal, authorized port scans to identify open ports and the services behind them. The goal is to connect two everyday weaknesses — weak passwords and unnecessarily exposed services — to real-world attack surface.

2. Password Strength Checker
2.1 Design

passwordchecker.py evaluates a password against five checks: minimum length of 8 characters, an uppercase letter, a lowercase letter, a digit, and a special character. It also checks the password against a blacklist of commonly breached/used passwords (e.g. 123456, password, qwerty). A blacklist match is automatically rated Very Weak, regardless of composition, since these are the first passwords attackers try in credential-stuffing attacks.

Based on how many of the five composition checks pass, the tool assigns Weak, Medium, or Strong, with specific feedback (e.g. "Add at least one special character"). It supports three run modes:

python passwordchecker.py --demo
python passwordchecker.py -p "SomePassword"
python passwordchecker.py
2.2 Automated Tests

test_password_checker.py runs 9 fixed cases covering all four rating tiers and asserts the returned rating matches expectations:

[PASS] '123456': got 'Very Weak', expected 'Very Weak'
[PASS] 'password': got 'Very Weak', expected 'Very Weak'
[PASS] 'hello': got 'Weak', expected 'Weak'
[PASS] 'aaaaaaaa': got 'Weak', expected 'Weak'
[PASS] 'Summer2026': got 'Medium', expected 'Medium'
[PASS] 'ADMIN123!': got 'Medium', expected 'Medium'
[PASS] 'Password1!': got 'Strong', expected 'Strong'
[PASS] 'Qwerty123!': got 'Strong', expected 'Strong'
[PASS] 'Tr0ub4dor&3!!': got 'Strong', expected 'Strong'

All tests passed.

All 9/9 cases pass, giving repeatable proof the rating logic behaves correctly across common-password, weak, medium, and strong inputs.

3. Port Scanning

All scans were run against localhost, my own home network (192.168.18.0/24), and scanme.nmap.org — a host the Nmap project maintains specifically for the community to practice scanning against, with scanning explicitly permitted by its operator. No unauthorized third-party network was scanned.

3.1 Localhost (Own Machine)
PORT      STATE SERVICE
135/tcp   open  msrpc
445/tcp   open  microsoft-ds
902/tcp   open  iss-realsecure
912/tcp   open  apex-mesh
2008/tcp  open  conf
16992/tcp open  amt-soap-http
135 (msrpc) — Windows RPC, internal service communication; historically targeted by worms (e.g. Blaster).
445 (microsoft-ds) — SMB file/printer sharing; one of the most exploited Windows ports (e.g. EternalBlue/WannaCry).
902 / 912 — Associated with the VMware Authentication Daemon (VMware is installed on this machine).
2008 (conf) — Generic label; would need -sV to positively identify.
16992 (amt-soap-http) — Intel AMT remote management interface.
3.2 Home Network (192.168.18.0/24)

256 addresses scanned, 11 hosts up, completed in ~610 seconds.

Host	Likely Device	Open Ports	Note
192.168.18.1	Router (Huawei)	22, 23 (telnet), 53, 80	Telnet is unencrypted and should be disabled
192.168.18.13	IoT (Amazon)	5555, 8009	Cast/media-control style ports
192.168.18.86	This machine	Same as localhost scan	Now visible from the network
.14, .22, .65, .121	Phones/other	None	Properly locked down
192.168.18.77	TP-Link	Filtered	Firewall silently drops probes — good posture
3.3 scanme.nmap.org (Authorized Public Test Host)
PORT      STATE    SERVICE
22/tcp    open     ssh
25/tcp    filtered smtp
80/tcp    open     http
9929/tcp  open     nping-echo
31337/tcp open     Elite
22 (ssh) — encrypted remote access, open by design for demonstrations.
25 (smtp, filtered) — no response from the firewall; more secure than an active "reset".
80 (http) — the host's public web page.
9929 (nping-echo) — Nping's packet-echo test service.
31337 (Elite) — a nod to "eleet" hacker slang; historically linked to backdoor trojans like Back Orifice, but intentionally opened here by the Nmap team, not a compromise.

Full breakdown: see scan_results/scan_results.md.

4. Reflection: Why This Matters

Weak passwords and open ports are the same problem from two angles: unnecessary attack surface. A weak or blacklisted password removes the effort an attacker needs to spend — automated tools guess it in seconds, no exploit required. An unnecessary open port does the same for a network — Wi-Fi strength doesn't matter if the router is quietly running Telnet.

The most notable finding here was Telnet (port 23) open on the home router. Telnet sends everything, including credentials, in plaintext. If an attacker reaches the local network, or the router is ever misconfigured to face the internet, credentials can be captured just by observing traffic. This mirrors a weak password exactly: both eliminate effort an attacker would otherwise need, and both are fixed with basic hygiene — disabling unused services, preferring SSH over Telnet, and using a strong, unique router admin password.

The scanme.nmap.org comparison reinforces the point from the other direction: every port open there is deliberate, and non-essential mail relay is filtered rather than left wide open. That is the difference between a hardened host and a typical unmanaged one — not the absence of open ports, but the absence of unintentional ones.

The broader lesson: security is rarely broken by a single sophisticated exploit. It's far more often broken by defaults nobody turned off and passwords nobody changed.