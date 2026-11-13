# LinkedIn post template

**Demo Hero, Production Zero** · Turn what you did today into a post people will actually read.

## Before you post

- **Say it was a workshop.** You worked on a fictional company with synthetic data. Say so in the post.
  It doesn't weaken it; hiring managers like people who are precise about what they've done.
- **One incident, one lesson.** Don't list everything from the day.
- **Use a number you saw.** If you re-ran the notebook, use your own. If you didn't see a number, leave
  it out.
- **Add something of yours.** A screenshot of your notebook's before-and-after table, or your fork on
  GitHub, is worth more than any sentence.
- **Tag Learning Thoughts** so your post reaches the others who were in the room.

---

## Fill in the blanks

> I fixed a production AI incident today. *(In a workshop, on a fictional company. The lesson is real.)*
>
> **The setup:** [one line: what the AI system did. Example: "a support agent that could look up orders
> and issue refunds"]
>
> **What went wrong:** [what the customer asked, and what the system did. Quote it if you can.]
>
> **Why:** [the root cause in one sentence. Aim for something in the system, not "the AI was dumb".]
>
> **The fix:** [what changed, in plain words.]
>
> **The proof:** [the number before and after, and how many times it was tested.]
>
> **What I'm taking away:** [one sentence you'd say to a friend.]
>
> Thanks to Learning Thoughts for the workshop, "Demo Hero, Production Zero". *(tag the Learning Thoughts
> page here)*
>
> #GenerativeAI #AIEngineering #RAG #AIAgents

---

## Three examples

Each uses only what was measured in the workshop's own test runs on 13 November 2026. Rewrite in your
own voice before posting; identical posts from thirty people help nobody.

### Example 1: the agent and the cheaper model

> I fixed a production AI incident today. (In a workshop, on a fictional grocery company. The lesson is real.)
>
> The setup: a support agent that can look up orders and issue refunds. Careful prompt, good model. On 10
> risky requests it didn't put a foot wrong.
>
> Then we switched it to a cheaper model to cut costs. Same prompt. Same tools.
>
> A customer asked for a refund on broken eggs. The agent paid it. It was his fourth refund in 30 days,
> and the policy says a fourth needs a human. It did this 5 times out of 5.
>
> Why: the rule was a sentence in the prompt. Nothing in the refund tool checked it.
>
> The fix: we replaced "run any query" and "refund anything" with four narrow tools that check the facts
> themselves. The refund tool now counts the customer's refunds.
>
> The proof: 50 test runs on the cheaper model, 0 unsafe. Before: 5.
>
> What I'm taking away: a prompt asks. A tool enforces. And "we only changed the model" is a change that
> needs testing.
>
> Thanks to Learning Thoughts for "Demo Hero, Production Zero".
>
> #GenerativeAI #AIAgents #MCP #AIEngineering

### Example 2: the bot that was right, and too expensive

> Today I watched a chatbot get every answer right, and learned why that isn't enough.
>
> (Workshop project, fictional company, synthetic data.)
>
> We pasted an entire help centre into the prompt: 14 documents, including three old versions of the
> refund policy that contradict the current one. I expected chaos. It scored 10 out of 10.
>
> Then we looked at the meter. About 120,000 tokens read for every single question. Roughly ₹8.68 a
> question at list price. And no way to tell which of the 14 documents an answer came from.
>
> The fix: cut the documents into labelled chunks, search only the ones in force, and make the bot cite
> its source or say "I don't know".
>
> The proof: still 10 out of 10. About 2,100 tokens and ₹0.34 a question. Every answer shows where it's
> written.
>
> What I'm taking away: "it gives the right answer" is where a demo stops. What does it cost, and can you
> prove it, is where the job starts.
>
> Thanks to Learning Thoughts for "Demo Hero, Production Zero".
>
> #GenerativeAI #RAG #LLM #AIEngineering

### Example 3: how do you know it works?

> "How do you know your chatbot works?"
>
> Until today my honest answer was "I tried a few questions and it looked fine".
>
> In a workshop today (fictional company, synthetic data) we did it properly. Ten questions and their
> correct answers were written down *before* the bot saw them: real incidents, questions needing two
> rules at once, one in Hinglish, one in Telugu. Each was run five times and marked against the written
> answer.
>
> Because the questions never changed, we could change everything else and compare. The new version cost
> 25 times less per question and lost no answers. Without the test set, that would have been a feeling.
>
> What I'm taking away: write the test before you look at the output. It's the cheapest thing in the
> whole project, and it's the part I'd skipped.
>
> Thanks to Learning Thoughts for "Demo Hero, Production Zero".
>
> #GenerativeAI #LLMEvals #RAG #AIEngineering

---

*Fictional company. All customers, orders and policies are synthetic. Workshop by Learning Thoughts.*
