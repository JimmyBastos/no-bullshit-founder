---
name: founder-grow
description: >-
  Step 6 of validating a business: do customers come back, and does it make
  money? Starts once strangers have paid. Records a baseline (the number the
  user already tracks and how they measure it), re-runs the numbers with real
  costs and sales, maps the real flow from order to delivery including the
  time work sits waiting, and improves one thing at a time with a rule written
  before each change. Adds operations only when they are needed: suppliers,
  permits, routines, risks. Ends with gate 6: repeat purchase at the agreed
  rate and one month in profit on real numbers. Use when the user says "I have
  customers, now what", "how do I grow", "people aren't coming back",
  "where is the bottleneck", "are we profitable", or runs /founder-grow.
argument-hint: "[the number to improve]"
---

# founder-grow

The test showed strangers will pay. Now the question is whether they pay
again and whether the business makes money on real numbers, not plans.

## Voice

Write for a smart person who builds things but has never run a business.
Explain the way a knowledgeable friend would: plain words, complete sentences,
and the whole answer. Don't trim the reasoning the reader needs to act. When a
business term matters, use it and say what it means the first time, so the
reader learns the vocabulary. Prefer concrete numbers, examples and sources to
adjectives. Skip hype, flattery and filler. Say what you don't know. End with
what to do next. Reply in the user's language.

## Who does what

The model gathers the numbers, maps the flow, finds where things wait, and
proposes changes. The user decides what to change and runs the business.

## Step 1: baseline

Before any change, write down how things are today in `founder/grow.md`:

- the numbers the user already tracks (sales a week, repeat rate, cost per
  customer, monthly profit), and how each is measured: where it comes from,
  how often, who counts it;
- what is not tracked yet but should be, starting with repeat purchase: the
  share of customers who buy again within a set period.

If a number is not measured, measuring it is the first change.

## Step 2: real numbers

Replace the estimates in `founder/numbers.json` with real costs, real prices,
real sales a day and real purchases per customer, and re-run the numbers
script from `/founder-numbers`. Compare plan with reality line by line and say
which assumption was furthest off.

## Step 3: map the flow

Walk through what happens from the moment a customer orders to the moment
they have what they paid for. For each step, note who does it, how long the
work takes, and how long the order waits before the work starts. Ask the user
for real examples, ideally the last 5 to 10 orders.

Most delay is waiting, not working. The step with the longest wait is usually
the bottleneck, and fixing anything else first changes little. Write the map
and the bottleneck in `founder/grow.md`.

## Step 4: one change at a time

Pick the change most likely to move the weakest number: repeat rate, cost per
customer, margin or the bottleneck. For each change:

- the hypothesis: what changes, and which number it should move;
- the rule: the number it should reach, by when, and the result that would
  show the change didn't work;
- run it like a test. Use `/founder-test` when it involves buyers or spending.

Change one thing at a time, so the result can be traced to the change.

Slow channels belong here: SEO, a blog, organic social, referrals,
partnerships. They compound over months once the business works.

## Step 5: operations, when needed

Add only what the current volume needs:

- suppliers, with real quotes, lead times and minimum orders;
- permits and registrations, with the official source;
- day-to-day routines written as short checklists, so someone else can do
  them;
- a short risk list: what could stop sales or delivery, and the plan for
  each.

Feed every real cost back into `founder/numbers.json`.

## Gate 6: a business, not a test

**Rule:** repeat purchase at or above the rate agreed with the user, within
the agreed period, and one full month in profit on real numbers, by the
deadline. Propose the repeat rate from the type of business and explain it.
A product bought weekly and a product bought once a year need very different
rates.

After this gate the user is running a business. Keep using step 4 for each
improvement.

## Gate rules

These are the same in every step.

- Propose the threshold from the user's own numbers, explain it in one line,
  and get the user's OK before the work starts. Set a deadline.
- **Pass:** the devil's advocate speaks, then the user decides.
- **Fail:** change one thing and retry. After 3 tries the user picks: pivot to
  `/founder-idea`, or stop.
- **Deadline missed:** inconclusive, treated as a fail.
- **Skip:** allowed. The devil's advocate speaks first and the reason is
  logged.

**Devil's advocate:** one argument, the strongest reason to stop, built from
the user's evidence. End with "I'd stop because X. I'd change my mind if Y,"
where Y is the cheapest test that would prove it wrong. If the evidence is
strong, say "I tried to argue against this and couldn't."

Log the gate in `founder/evidence.md`:

```
## Gate 6: grow (<date>)
Rule: <what must be true>  Threshold: <number>  Deadline: <date>  Try: <1-3>
Result: PASS | FAIL | INCONCLUSIVE | SKIP
Evidence: <repeat rate, monthly profit, how each was measured>
Devil's advocate: I'd stop because ... I'd change my mind if ...
Decision: <continue | retry: what changes | pivot | stop>, because ...
```

## Rules

- Every number says where it came from and how it was measured.
- Not financial, tax or legal advice. An accountant checks the books.

## Output

`founder/grow.md`, an updated `founder/numbers.json`, `founder/evidence.md`.
