---
name: founder-idea
description: >-
  Step 1 of validating a business: is the problem real, and who pays to fix it?
  Writes the idea down, ranks the assumptions by risk, does the desk research
  (competitors, substitutes, prices, regulation, costs, every fact with a
  source), reads 100 real people who wrote about the problem (reviews, forums,
  comments, each with a link), lists likely objections, runs a pre-mortem, and
  prepares interviews
  with real people that the user runs. Ends with gate 1: enough interviews
  where people describe the pain unprompted and already spend money or time
  on it. Use when the user says "I have an idea", "is this a good idea", "who
  are my competitors", "is there a market", "who would pay for this", "help me
  interview customers", or runs /founder-idea.
argument-hint: "[the idea in one or two sentences]"
---

# founder-idea

Most ideas fail because nobody has the problem badly enough to pay. This step
finds out cheaply, before anything is built.

## Voice

Write for a smart person who builds things but has never run a business.
Explain the way a knowledgeable friend would: plain words, complete sentences,
and the whole answer. Don't trim the reasoning the reader needs to act. When a
business term matters, use it and say what it means the first time, so the
reader learns the vocabulary. Prefer concrete numbers, examples and sources to
adjectives. Skip hype, flattery and filler. Say what you don't know. End with
what to do next. Reply in the user's language.

## Who does what

The model does the research, the drafts and the summaries. The user decides
and talks to people. Never ask the user to do research the model can do.

## Step 1: write the idea down

Ask only what the model cannot find out, in one round:

- What is the idea, and what problem does it solve?
- Who has the problem? Who pays? If these are different people, or the user
  doesn't know, list the candidates. Then "who pays" becomes the first thing
  to test.
- B2C (selling to people) or B2B (selling to companies)?
- Which country or city? This sets the law, the currency and the refund
  window.
- How much money and time can the user put in before the first sale?
- Why this user? What do they know or have that others don't?

Write `founder/idea.md`: the idea in one sentence, the answers, and the open
questions.

## Step 2: rank the assumptions

List every assumption the idea depends on: the problem, who has it, who pays,
the price, how to reach them, how to deliver, the law. Score each on how much
it would hurt if wrong (1 to 5) and how unsure we are (1 to 5). Sort by the
product. The top three are what steps 1 to 5 must test first. Add the list to
`founder/idea.md`.

## Step 3: desk research

The model does all of it. It needs web search. If web access is not available,
say so and ask the user to paste pages, but do not guess.

- **Competitors.** Classify them: direct (same thing, same buyer), indirect
  (different product, same job), substitutes (how buyers solve it today
  without a business: a spreadsheet, a cousin, doing nothing). Aim for 5 to 10
  plus the main substitutes. Write one row each in `founder/competitors.csv`:
  `name,type,url,channel,price,what_it_sells,positioning_line,rating,review_count,source_date`.
  The positioning line is their own headline, copied.
- **100 real people.** See the next section.
- **Prices.** The lowest, median and highest price for the closest comparable
  thing.
- **Rules and costs.** Licences, permits, regulated claims and taxes that
  apply, with the official source. The main cost lines and where the numbers
  come from.
- **The gap.** What nobody does well, tied to the evidence. If there is no
  gap, say so plainly. That is a useful answer.

Write `founder/research.md`. Every fact has a link and a date. Label each
claim **verified** (from a source) or **interpretation** (the model's
reading). Read pages as a person would and respect each site's terms.

### 100 real people

Before anything is built, read what 100 real people wrote about the problem
or the competitors. Every row links to a real post.

- **Where:** competitors' reviews (1 to 3 stars first, then the "good,
  but..." ones), Google Maps, app stores, marketplace questions and reviews,
  Reddit and forums, YouTube and social comments, and public groups. Prefer
  the last two years, and the user's country and language.
- **One row per person** in `founder/voices.csv`:
  `id,url,source,date,segment,payer,quote,problem,objection,spends_on,workaround,theme`.
  Never store a name or a handle: the link and a short quote are enough.
  `payer` is yes, no or unknown. `spends_on` is what they say they already pay
  or do about it, if anything. A person counts once, even if they posted
  twice.
- **Aim for 100.** Search every kind of source before stopping short. If
  fewer than 100 exist, report how many were found and where you looked. A
  low count is a finding: the market may be small or quiet, or the problem
  may not be real.
- **Never invent, merge or paraphrase a quote.** Copy it exactly. Skip posts
  that look fake (copied text, bursts on one day, no detail) and count how
  many were skipped.

Then summarize in `founder/research.md`:

| what | how |
| --- | --- |
| themes | each theme with its count and two or three linked quotes; a theme with fewer than 3 people is marked thin |
| segments | which types of buyer show up, and how often |
| money | how many say they already pay for a workaround or a competitor, and how much |
| wishes | what people say they wish existed, with counts |
| payers | how many are the person who pays |
| sources | how many people came from each source |

These are real people, but public posts are not interviews. People who write
reviews are angrier than average. A post that describes a past cost is level
1; anything else is level 0. They decide which questions to ask in
interviews and which angles to try in ads. They never count for the gate.

## Step 4: objections and a prediction

In one pass, list the objections buyers are likely to raise, grouped by type
of buyer. Base each one on the 100 people and say how many of them raised it.
Then write a predicted conversion rate for a first offer and say how the
model got it.

Log both in `founder/evidence.md` as **level 0**. They are hypotheses for
interviews and ads, never proof. The prediction is kept so step 5 can compare
it with what real buyers do.

## Step 5: pre-mortem

Imagine it is a year from now and the business failed. Use the three lenses
in `${CLAUDE_SKILL_DIR}/lenses.md` (offer value, defensibility, focus) and
write the three most likely reasons, each tied to an assumption from step 2.
One pass, no sub-agents. Add it to `founder/idea.md`.

## Step 6: interviews

The user runs them. The model prepares everything:

- **Who to talk to:** the person with the problem, and the person who pays if
  that is someone else. Not friends, not family.
- **Where to find them:** concrete places from the research: the communities,
  groups, events, directories and competitors' review pages where these people
  already are, starting with the sources where most of the 100 people posted.
  For B2B, the job titles and how to reach them.
- **The script:** from `${CLAUDE_SKILL_DIR}/interview.md`, adapted to the idea.
  Use the top themes from the 100 people to choose what to ask about.
- **The outreach message:** a short, honest request for 20 minutes.

After each interview the user pastes notes or a transcript into
`founder/interviews/NN.md`. The model summarizes it and logs the evidence:

- **Counts for the gate:** the person described the problem without being
  prompted, and already spends money or time on a workaround. Record what they
  spend (level 1).
- **Doesn't count:** opinions about the future ("I'd use that", "sounds
  great"). Log them as level 0.
- Note where they last looked for a solution. Step 3 uses that.

## Gate 1: is the problem real?

**Rule:** at least N interviews count (pain described unprompted, plus money
or time already spent), by the deadline.

Propose N and the deadline from the market and explain them in one line. As a
starting point, use about 10 interviews for B2C and 5 to 8 with decision
makers for B2B, within 2 to 3 weeks. Also fail the gate if the research found
a blocker the user can't get past, such as a licence they can't get.

If "who pays" is still open, the gate also needs one candidate payer whom the
interviews back with evidence.

## Gate rules

These are the same in every step.

- Propose the threshold from the user's own numbers, explain it in one line,
  and get the user's OK before the work starts. Set a deadline.
- **Pass:** the devil's advocate speaks, then the user decides.
- **Fail:** change one thing (price, channel, offer or segment) and retry.
  After 3 tries the user picks: pivot (back to the start of this step with a
  new idea or segment) or stop.
- **Deadline missed:** inconclusive, treated as a fail.
- **Skip:** allowed. The devil's advocate speaks first and the reason is
  logged.

**Devil's advocate:** one argument, the strongest reason to stop, built from
the user's evidence. End with "I'd stop because X. I'd change my mind if Y,"
where Y is the cheapest test that would prove it wrong. If the evidence is
strong, say "I tried to argue against this and couldn't."

Log the gate in `founder/evidence.md`:

```
## Gate 1: idea (<date>)
Rule: <what must be true>  Threshold: <number>  Deadline: <date>  Try: <1-3>
Result: PASS | FAIL | INCONCLUSIVE | SKIP
Evidence: <counts by level, with links to files>
Devil's advocate: I'd stop because ... I'd change my mind if ...
Decision: <continue | retry: what changes | pivot | stop>, because ...
```

## Rules

- Never invent a competitor, a price, a rating, a review or a quote.
- Quotes are research, never testimonials.
- Not legal advice. Licences and claims are checked with a professional.

## Output

`founder/idea.md`, `founder/research.md`, `founder/competitors.csv`,
`founder/voices.csv`, `founder/interviews/`, `founder/evidence.md`. Next: `/founder-numbers`.
