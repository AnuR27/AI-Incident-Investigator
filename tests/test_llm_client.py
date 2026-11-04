from app.llm_client import generate_investigation

question = (
    "What could explain checkout timeouts, "
    "and what evidence is needed to investigate?"
)


context = """
[RUNBOOK-001]
Type: General guidance
Text: Database connection pool exhaustion can cause checkout
requests to time out. Check active connections, pool size,
and connection leaks.

[INCIDENT-EVIDENCE-001]
Type: Evidence availability
Text: No current incident logs or database metrics have been
provided to confirm that checkout requests timed out or that
connection pool exhaustion occurred.
"""


answer = generate_investigation(question, context)

print(answer)
