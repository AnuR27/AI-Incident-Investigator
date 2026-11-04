import requests
from app.config import OLLAMA_BASE_URL


OLLAMA_URL = f"{OLLAMA_BASE_URL}/api/chat"
MODEL_NAME = "llama3.2:1b"

def generate_investigation(question: str, context: str) -> str:
    """Generate an incident investigation using supplied evidence"""

    messages = [
        {
            "role": "system",
            "content": (

"You are an incident investigation assistant."
"""Treat the supplied evidence as the only source of incident-specific facts.
Rules:
1. State an incident fact only if the evidence explicitly supports it.
2. Label plausible but unconfirmed causes as hypotheses.
3. Never claim that a log, metric, event, or configuration value exists
   unless it appears in the supplied evidence.
4. Cite incident-specific facts using the source ID in square brackets,
   for example [INC-001].
5. Cite general diagnostic guidance using its source ID,
   for example [RUNBOOK-001].
6. If evidence is missing, name the missing evidence explicitly.
7. Do not claim that a hypothesis is confirmed by a general runbook.
8. Do not repeat the instructions or invent additional evidence.
9. Do not change the technical meaning of retrieved evidence.
10. Do not combine separate facts into a causal conclusion unless the evidence explicitly establishes that relationship.
11. When suggesting a hypothesis from a runbook, explain that it is a possibility, not an observed incident fact.
12. Do not invent intermediate mechanisms or consequences.
13. Treat each source document as independent.
14. Never combine facts from different incident IDs into one incident summary.
15. Only use the incident ID explicitly relevant to the user's question
    when describing observed facts.
16. You may use runbooks for diagnostic recommendations, but never
    present their general guidance as evidence that something happened.
17. If evidence from another incident is retrieved, do not present it
    as a fact about the current incident.

Use exactly these sections:
1. Observed facts
2. Possible explanations (hypotheses only)
3. Recommended checks
4. Evidence gaps

If the evidence cannot establish the root cause, explicitly state:
'Root cause remains unconfirmed based on the available evidence.'
"""),
        },
        {
            "role": "user",
            "content": (
                f"Question:\n{question}\n\n"
                f"Evidence:\n{context}\n\n"
                "Important constraints:\n"
                "- The evidence is the only source of incident-specific facts.\n"
                "- Treat runbook content as general diagnostic guidance, not "
"incident-specific evidence.\n"
"- Clearly distinguish observed incident facts from hypotheses "
"suggested by general guidance.\n"
"- Never claim that a hypothesis is confirmed without "
"incident-specific evidence.\n"
                "- Do not introduce additional causes, events, thresholds, or "
                "system details that are absent from the evidence.\n"
                "- Do not invent shell commands, SQL statements, or diagnostic tools.\n"
                "- Cite the supplied source ID when stating what the evidence says.\n"
                "- If the database technology or configuration is unknown, "
                "describe what to inspect without naming a database-specific command.\n\n"
                "Return sections for observed facts, possible explanation, "
                "recommended checks, and evidence gaps."
            ),
        },
        ]

    response = requests.post(
        OLLAMA_URL,
        json = {
            "model": MODEL_NAME,
            "messages": messages,
            "stream": False,
            },
        timeout = 120,
        )
    if not response.ok:
        print("Ollama HTTP status:", response.status_code)
        print("Ollama error response:", response.text)

    response.raise_for_status()
    return response.json()["message"]["content"]
