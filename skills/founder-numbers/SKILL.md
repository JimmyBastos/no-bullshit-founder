---
name: founder-numbers
description: >-
  Step 2 of validating a business: can the numbers work? Builds the unit
  economics before money is spent: profit per sale (contribution), break-even,
  the profit margin at the planned volume, year 1 month by month, the cash
  needed, payback, and the most you can pay to get one customer (max CAC).
  Compares max CAC with what customers really cost on the likely channel, from
  public benchmarks with sources. Runs a Van Westendorp price analysis only on
  answers from a real survey. Ends with gate 2. Use when the user says "do the
  numbers", "is this profitable", "what should I charge", "break-even", "unit
  economics", "how much can I spend on ads", "how much do I need to start", or
  runs /founder-numbers.
argument-hint: "[path to founder/numbers.json]"
---

# founder-numbers

A good idea is a business only if each sale leaves money after its costs, and
you can get customers for less than that. This step checks both with a
script, so every number traces to an input.

## Voice

Write for a smart person who builds things but has never run a business.
Explain the way a knowledgeable friend would: plain words, complete sentences,
and the whole answer. Don't trim the reasoning the reader needs to act. When a
business term matters, use it and say what it means the first time, so the
reader learns the vocabulary. Prefer concrete numbers, examples and sources to
adjectives. Skip hype, flattery and filler. Say what you don't know. End with
what to do next. Reply in the user's language.

## Who does what

The model finds the costs, prices and benchmarks, fills in the file, runs the
script and explains the result. The user confirms the numbers only they know
(rent quoted, wages, their own time) and decides the price.

## Step 1: fill in founder/numbers.json

The shape is in `${CLAUDE_SKILL_DIR}/example.json`.

| field | what goes in it |
| --- | --- |
| `business`, `unit`, `currency` | name, what one sale is (a cup, an order, a client-month), currency symbol |
| `price` | price per unit before tax |
| `variable` | the cost of one unit: materials, packaging, shipping, card or Pix fees, commissions |
| `fixed_monthly` | what you pay every month whatever you sell: rent, salaries, software |
| `startup` | one-off spend before the first sale |
| `ramp_per_day` | 12 numbers: realistic sales per day in each month of year 1. Required |
| `plan_per_day` | the volume once it runs (optional; default is the last ramp month) |
| `capacity_per_day` | the most you can deliver in a day, if there is a limit |
| `purchases_per_customer` | how many times one customer buys in year 1 (default 1) |
| `cac_benchmark` | `{"value": ..., "channel": ..., "source": ...}`: what one customer costs on the likely channel |

Where numbers come from, in this order:

1. The user's quotes, invoices and price lists.
2. Public prices the model can find and link: supplier lists, rents, payment
   fees, ad cost benchmarks. Write each source in `founder/numbers.md`.
3. An estimate, marked as an estimate, with the reasoning.

**Price:** start from the competitor price range in `founder/research.md` and
what interviewees already spend on workarounds. Never use a model's guess of
what buyers would pay.

**Ramp:** month 1 is almost never the full volume. Build the ramp from what
the user can really reach. Mark it as the assumption most likely to be wrong.

**CAC benchmark:** take the cost per lead or per sale for the likely channel
from a public source, and say how old it is and how it was measured. If step 3
has not picked a channel yet, use the channel the interviews point to, and
re-run after step 3.

## Step 2: run it

```bash
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" founder/numbers.json --out founder/numbers.md
```

The report shows contribution, break-even, the margin at plan, year 1 by
month, cash needed, payback, max CAC against the benchmark, a what-if table
(price -10%, volume -20%, unit costs +15%) and red flags. What-ifs without
editing the file:

```bash
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" founder/numbers.json --price 7.00
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" founder/numbers.json --volume 0.8
python3 "${CLAUDE_SKILL_DIR}/unit_economics.py" founder/numbers.json --cost 1.15
```

## Step 3: explain it

Add a short note at the top of `founder/numbers.md`:

- The contribution and what it means for this business.
- The line that moves the result most, with the what-if that shows it.
- The cash the user needs before it pays for itself.
- Max CAC against the benchmark, in plain words: "You can pay up to R$X to get
  a customer; on Meta, similar businesses pay about R$Y (source)."
- Two or three ways to improve the numbers. Run the what-if for each; don't
  guess.

## Price research with real people (optional)

If the user runs a price survey with real respondents, the Van Westendorp
script turns the four answers per person (too cheap, a bargain, getting
expensive, too expensive) into an acceptable price range:

```bash
python3 "${CLAUDE_SKILL_DIR}/van_westendorp.py" survey.csv --price 6.50 --out founder/price-range.md
```

It needs real answers, at least 30 to draw the curve. Practitioners suggest
200 or more for a reliable range. Never feed it model answers. With few
respondents, the result only tells you which prices to test in step 5.

## Gate 2: can the numbers work?

The script prints the gate result. **Rule:** contribution is above zero, and
max CAC is at least the CAC benchmark for the channel. Also flag, and discuss
with the user, a break-even above capacity, a plan above capacity, or a
payback beyond 12 months.

## Gate rules

These are the same in every step.

- Propose the threshold from the user's own numbers, explain it in one line,
  and get the user's OK before the work starts. Set a deadline.
- **Pass:** the devil's advocate speaks, then the user decides.
- **Fail:** change one thing (price, costs, offer or segment) and retry. After
  3 tries the user picks: pivot to `/founder-idea`, or stop.
- **Deadline missed:** inconclusive, treated as a fail.
- **Skip:** allowed. The devil's advocate speaks first and the reason is
  logged.

**Devil's advocate:** one argument, the strongest reason to stop, built from
the user's evidence. End with "I'd stop because X. I'd change my mind if Y,"
where Y is the cheapest test that would prove it wrong. If the evidence is
strong, say "I tried to argue against this and couldn't."

Log the gate in `founder/evidence.md`:

```
## Gate 2: numbers (<date>)
Rule: <what must be true>  Threshold: <number>  Deadline: <date>  Try: <1-3>
Result: PASS | FAIL | INCONCLUSIVE | SKIP
Evidence: <the numbers, with links to files>
Devil's advocate: I'd stop because ... I'd change my mind if ...
Decision: <continue | retry: what changes | pivot | stop>, because ...
```

## Rules

- Every number in the note comes from the script's output or an input with a
  source.
- Revenue is before tax. Say if the market adds sales tax on top.
- Not financial, tax or legal advice. Say once that an accountant should check
  the structure, payroll and tax before money moves.

## Output

`founder/numbers.json`, `founder/numbers.md`, `founder/evidence.md`. Next:
`/founder-channels`.
