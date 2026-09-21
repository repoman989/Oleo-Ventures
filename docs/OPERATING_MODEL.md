# Operating Model

## Terminology
| System concept | Oleo Ventures term |
| --- | --- |
| User | Founder / CEO |
| Primary assistant / orchestrator | Dex — Chief of Staff |
| Agent | Employee |
| Lightweight agent | Intern |
| General knowledge worker | Analyst / Engineer |
| High-capability worker | Senior |
| Temporary worker | Contractor |
| External/API model | Consultant |
| Capability grouping | Department |
| Task | Assignment |
| Large task | Initiative |
| Ongoing portfolio company | Venture |
| Tools and APIs | Company Resources |
| Persistent knowledge | Institutional Knowledge |
| Verification | Internal Audit |
| Human-required decision | Executive Approval |
| Final result | Deliverable |

## Executive workflow
1. Objective — Founder gives Dex a desired outcome.
2. Scope — deliverable, constraints, risk, information needs.
3. Staffing — smallest appropriate team from Departments.
4. Delegation — Initiative decomposed into Assignments.
5. Execution — approved local models, tools, data.
6. Review — Internal Audit checks claims, code, contradictions.
7. Revision — another pass, more expertise, or escalate.
8. Delivery — Dex synthesizes the Deliverable.

## V0 constraint on execution
Per V0_READINESS.md: LLM generation calls, model load/swap, and state writes are sequential. Non-LLM I/O, parsing, and git work can run in parallel (4-6 workers).
