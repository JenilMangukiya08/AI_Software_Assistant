from llm.llm import llm

from graph.prompts import SECURITY_PROMPT

from tools.security_scanner import security_scan


def security_agent(repository, question):

    findings = security_scan(repository)

    if not findings:

        return "No obvious security issues were found."

    text = ""

    for f in findings:

        text += f"""

Issue:
{f['issue']}

File:
{f['file']}

Line:
{f['line']}

Code:
{f['code']}

-------------------------

"""

    prompt = SECURITY_PROMPT.format(

        findings=text,

        question=question

    )

    response = llm.invoke(prompt)

    return response.content