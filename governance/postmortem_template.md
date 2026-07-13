# Postmortem Template

When Entity experiences a SEV-0/1/2 incident, a postmortem is published
within 72 hours. This template structures the writeup.

## Incident Summary

- **Incident ID:** ENTITY-YYYY-MM-DD-NN
- **Severity:** SEV-0 (Prime Directive violation) | SEV-1 (significant defect) | SEV-2 (minor defect)
- **Detection time:** ISO timestamp
- **Resolution time:** ISO timestamp
- **Duration:** N hours/minutes

## What Happened

Brief factual description. No blame, no speculation.

## Impact

- Users affected: N | none
- Funds at risk: $N | none
- False alerts published: N | none
- Posts retracted: N | none
- Trust damage: assessment

## Timeline

- HH:MM - first signal
- HH:MM - detection
- HH:MM - escalation to founder review
- HH:MM - mitigation deployed
- HH:MM - resolution confirmed

## Root Cause

Direct technical root cause. May include:
- LLM hallucination
- Source data error
- Dedup miss
- Rate limit miscalibration
- Voice transform failure
- Spending guard miscalibration
- Drift detector false negative
- External API failure not handled
- Operator error

## Contributing Factors

Background conditions that made the incident possible.

## What Worked

What defenses prevented this from being worse.

## What Did Not Work

Where Entity's defensive layers failed.

## Action Items

- [ ] Code change: short description (assignee, deadline)
- [ ] Process change: ...
- [ ] Documentation update: ...
- [ ] Test coverage: ...

## Public Apology (if applicable)

If Entity caused harm or published incorrect alerts, explicit
acknowledgment + correction. Posted to X + Telegram + feed.

## Lessons Learned

Observations for the broader defensive AI community. This postmortem
becomes a public artifact in Entity's transparency record.

---

## Severity Definitions

**SEV-0** - Prime Directive violation:
- Entity attacked something
- Entity assisted in offensive action
- Entity refused legitimate defensive guidance
- Entity violated spending limits

**SEV-1** - Significant defect:
- False CRITICAL alert published
- Outage > 1 hour
- Data exposure (private info leaked)
- Multiple incorrect alerts in single cycle

**SEV-2** - Minor defect:
- Single incorrect alert
- Voice transform failure
- Dedup miss < 5 instances
- Brief outage < 15 minutes

---

*Postmortems are not punishment. They are improvement.*
*Entity is not infallible. Entity is honest about being fallible.*
