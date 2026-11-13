# Production Readiness Scorecard

**Demo Hero, Production Zero** · Score yourself twice: at the start, and again at the end.

For each line, write **0**, **1** or **2**:

- **0** · I haven't done this
- **1** · I've seen it or tried it once
- **2** · I could do it at work, or explain it in an interview

Be honest. Nobody sees this but you.

| # | I can... | Start | End | Program part that teaches it |
|---|---|---|---|---|
| 1 | Explain why a prompt that gives right answers still isn't production-ready (cost, sources, change) | | | RAG |
| 2 | Build retrieval that handles tables and long documents, not just paragraphs | | | RAG |
| 3 | Make an AI cite its source, or say "I don't know" when it has none | | | RAG |
| 4 | Measure answer quality with an eval set instead of "it looks right" | | | RAG · Prove it |
| 5 | Design narrow tools so an agent can't act on the wrong data | | | MCP |
| 6 | Add a human-approval step for risky agent actions | | | Agents |
| 7 | Defend an agent against prompt injection | | | Agents · Protect it |
| 8 | Read a trace and find the exact step where an agent went wrong | | | Observability (LangSmith, Langfuse) |
| 9 | Work out what one AI conversation costs, and cut it | | | Cost and latency engineering |
| 10 | Use a coding agent (Claude Code or Codex) to build and fix faster | | | AI-assisted development |
| 11 | Deploy an AI system on a cloud platform (AWS, Azure or GCP) | | | Ship it, in every part |
| 12 | Run an open model locally for private data | | | Fine-Tuning & Local Models |

**Start total:** ____ / 24  **End total:** ____ / 24

---

### Reading your score

- Lines that moved up today: you've seen them work. The program makes them a 2.
- Lines that didn't move (9 to 12): today only previewed them. Each is a full module in the program.
- Every line on this card is taught in the Generative AI Developer Program, with a capstone that uses it.
