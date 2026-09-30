# Publishing warning — review before making this course public

This course is legitimate professional education in AI/LLM/agent security, but its subject matter is
dual-use by nature. The material below is the honest list of what a reviewer should look at, so the
decision to publish is an informed one rather than a surprise. **Nothing in the course is a weapon
and nothing in it works against a real system**, but a reader could reasonably want to check that
before making it public.

## What the course is

A purple-team curriculum: attacks are built and measured, then defended, then attacked again, so
that a practitioner can both break and harden AI systems they are authorised to test. It is
positioned for defenders, security engineers and researchers.

## What a reviewer should confirm

1. **All offensive work is local and synthetic.** Every lab targets either an intentionally
   vulnerable app shipped in this repo or an in-process mock, on the learner's own machine. There
   are no real targets, no real credentials, no working malware, and no exfiltration endpoints
   beyond a local sink. Secrets in the labs are synthetic canaries of the form
   `LAB-CANARY-<something>`. Verify by reading `labs/module-*/` and `lab/README.md`.

2. **No network egress from labs.** The labs that use Docker bind services locally and do not route
   traffic off the host. Check any `docker-compose.yml` under `labs/module-*/` for published ports
   and confirm they are localhost-bound or unset.

3. **Payloads demonstrate mechanism, not effect.** Injection strings, jailbreak suffixes and
   poisoning examples end in an inert marker — a canary the learner's own sink records — rather than
   in a destructive or exfiltrating action. Spot-check a few attack scripts.

4. **Named real-world targets appear only as documented public incidents.** Lessons cite real
   products, CVEs and advisories (for example exposed model servers, MCP design issues, published
   vulnerabilities in orchestration platforms). These are references to publicly disclosed events
   and standards, described at the level needed to teach the defense. They are not step-by-step
   instructions against a named live system. Review
   `references/standards-map.md` and the "Real-world examples" sections.

5. **The reconnaissance module (27) is the one to read most carefully.** It teaches how to
   fingerprint AI services and enumerate model infrastructure. The content is standard material from
   any security literature and stays on detection-avoidance framing ("keep your probe rate below the
   defender's alerting threshold", "prefer passive OSINT"), but it is the section a reviewer is most
   likely to want to read personally. The lab is entirely in-process and binds no sockets.

6. **No credential, no malware, no targeting data.** The course does not ship leaked credentials,
   exploit code for an unpatched product, or lists of real targets.

## Not a concern

- The paper reading guides in `papers/` are study notes on published research.
- The standards crosswalks (OWASP, MITRE ATLAS, NIST) are public frameworks.
- The capstone (module 31) is a simulated environment shipped with the course.

## If you decide to restrict it

`curriculum/course-details.md` has the slug, repo and a suggested free/paid classification. The
Academy can restrict a course at import time; the repo itself may stay public as a docsify site, in
which case the same considerations apply to the Pages build, since it publishes the same markdown.
