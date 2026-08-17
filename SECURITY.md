# Security Policy

Thank you for helping keep cocktail-recipe-finder secure. This document explains how to report a vulnerability, what to expect after you report one, and how we handle disclosure.

## Supported Versions

We will indicate which versions are actively supported for security fixes. Replace the table below with the actual supported versions for this project.

| Version | Supported |
| ------- | --------- |
| main (latest) | :white_check_mark: |
| 0.1.x | :white_check_mark: |
| < 0.1 | :x: |

## Reporting a vulnerability (preferred)
1. Preferred: Open a private report using GitHub Security Advisories for this repository. Go to the repository's "Security" → "Advisories" and click "Report a vulnerability".
2. Alternative: If you cannot use GitHub Security Advisories, send an email to: SECURITY@example.com (replace with a real address for this project).

If you prefer encrypted email, please encrypt with our PGP key (replace the placeholder with a real key if you publish one):

-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: PGP

<PGP PUBLIC KEY OR FINGERPRINT HERE>

-----END PGP PUBLIC KEY BLOCK-----

Please do NOT open a public issue or discuss the vulnerability in public — this helps prevent accidental disclosure and protects users.

## What to include in your report
Please include as much of the following as you can:
- A short summary of the vulnerability and its impact.
- Affected versions / commits (tag/branch/commit SHA).
- Steps to reproduce or a proof-of-concept (PoC). Minimal PoCs are acceptable.
- Any logs, screenshots, or network traces that help reproduce the issue.
- Whether you are aware of active exploitation.
- Your contact details and whether you want to be credited.

We will treat sensitive attachments (PoC code, dumps) privately.

## Response timeline and updates
We aim to be responsive and transparent. Typical timeline:
- Acknowledgement: within 48 hours of receiving your report.
- Initial triage: within 5 business days.
- Status updates: at least once every 7 calendar days while we are actively working on a fix, or sooner for critical issues.
- Patch timeline: varies by severity. We will provide an estimated ETA during triage.

Severity and typical targets (estimates):
- Critical (remote code execution, data exfiltration of production user data): initial mitigation/temporary workaround within 7 days; fix and release as soon as possible, aim within 30 days.
- High (privilege escalation, serious data exposure): aim to fix within 30 days.
- Medium (limited information disclosure or scoped auth bypass): aim to fix within 90 days or in the next release cycle.
- Low (minor issues, suggestions, or non-exploitable bugs): fixed in a future release when convenient.

These are guidelines; actual timelines depend on complexity, resources, and user risk. If the issue is actively exploited in the wild, we will accelerate timelines and coordinate an expedited disclosure.

## What happens if the vulnerability is accepted
- We will work with you privately to reproduce and confirm the issue.
- We will develop and test a fix, and release it to users (patch/release/PR). We will coordinate the disclosure timeline with you.
- When appropriate, we will request or assign a CVE.
- With your consent we will credit you in the release notes or an ACKs file. If you prefer anonymity, tell us in your initial report.

## What happens if the vulnerability is declined
- If we determine the report is not a vulnerability (out-of-scope, not applicable, or misconfiguration), we will explain why and provide mitigation recommendations where appropriate.
- If you disagree with our assessment, you may request further review and we will re-triage with additional context.

## Scope
In scope:
- Code and configuration in this repository and files managed directly by the project.
- GitHub Actions workflows and CI configurations stored in this repo (as they appear here).

Out of scope:
- Third-party services, external dependencies, or other projects not maintained in this repository (report to the vendor or upstream project).
- Physical attacks, social engineering, or attacks against other users.

If you're unsure whether something is in scope, please report it privately and we will clarify.

## Coordinated disclosure and public advisories
We follow a coordinated disclosure process. We will work with you to agree a disclosure date once a fix is available and users have had a reasonable window to update. If you prefer immediate public disclosure, tell us and we will discuss the potential impacts.

If you want a public advisory (e.g., a GitHub Security Advisory or a CVE), we will coordinate publishing it once the fix is ready and we've agreed on a disclosure timeline.

## Safe harbor
We welcome good-faith security research. We will not pursue legal action against researchers acting in good faith and following this policy. Please avoid privacy violations, exfiltrating production user data beyond what is necessary to demonstrate an issue, and denial-of-service testing that might harm users or infrastructure.

## Acknowledgments
We appreciate security researchers who help improve this project. With your permission we will credit you in an ACKs file or release notes.

## Contact / Maintainer
- Repository: https://github.com/xiaoWings/cocktail-recipe-finder
- Preferred reporting: GitHub Security Advisories for this repo
- Alternative contact: SECURITY@example.com (replace with a working project email or remove if you prefer only GitHub advisories)

---

Please replace placeholders (email/PGP) with real contact information if you want this policy to be actionable.
