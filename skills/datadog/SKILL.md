---
name: datadog
description: "Find and install the Datadog Labs skill needed for Agent setup, APM, Single Step Instrumentation, or another Datadog task. Use instead of installing the whole catalog."
---

# Datadog skill index

Use the [Datadog Labs skill catalog](https://github.com/datadog-labs/agent-skills)
as the source. This skill routes requests; it does not deploy the Agent,
change observability settings, or authorize access to a Datadog account.

1. Identify the job and platform. For Agent installation, look for the
   platform-specific `dd-agent-install-*` skill. For APM and Single Step
   Instrumentation, start with `dd-apm` and choose its platform-specific
   guidance. For other requests, inspect the catalog instead of guessing names.
2. Check the target harness for the selected skill. If it is already installed,
   use the installed copy and respect local modifications; do not update it
   just to answer a question.
3. If absent and installation is authorized, inspect the upstream skill at a
   specific revision. Install only its directory through the configured skill
   manager at that reviewed revision. If the manager cannot select it safely,
   link to the specific skill instead. Verify the installed source and revision.
4. Follow the selected skill within the original task's permissions. Treat any
   Agent deployment, credential prompt, or external data transfer as a separate
   action, not a side effect of installing a guide.
