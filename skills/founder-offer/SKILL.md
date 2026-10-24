---
name: founder-offer
description: >-
  Step 4 of validating a business: what is the smallest thing you can sell,
  and how? Defines the MVP (often done by hand at first), builds the offer
  from the objections real interviewees raised (core, bonuses, a guarantee the
  numbers can afford, honest urgency, a clear name), and drafts what the test
  needs: a landing or pre-sale page with payment and consent, or for B2B a
  one-page proposal, a pilot offer and a letter of intent, plus ad or post
  drafts for the chosen channels. Ends with gate 4: page live and payment
  working. Use when the user says "what should my MVP be", "make my offer
  better", "write my landing page", "pre-sale", "guarantee", "pilot proposal",
  "letter of intent", or runs /founder-offer.
argument-hint: "[what you sell]"
---

# founder-offer

People don't buy a product. They buy an outcome, and a reason to believe
they'll get it. This step builds the smallest version that someone can pay
for, and everything needed to put it in front of buyers.

## Voice

Write for a smart person who builds things but has never run a business.
Explain the way a knowledgeable friend would: plain words, complete sentences,
and the whole answer. Don't trim the reasoning the reader needs to act. When a
business term matters, use it and say what it means the first time, so the
reader learns the vocabulary. Prefer concrete numbers, examples and sources to
adjectives. Skip hype, flattery and filler. Say what you don't know. End with
what to do next. Reply in the user's language.

## Who does what

The model drafts the MVP options, the offer, the page, the proposal and the
ads. The user picks, approves anything that goes public, and sets up the
accounts that need their identity (payment, domain).

## Step 1: the MVP

Read `founder/idea.md`, `founder/interviews/`, `founder/numbers.md` and
`founder/channels.md`. Propose two or three MVP options and recommend one.
Common shapes:

- **Pre-sale:** sell it before it exists, with a delivery date and a refund
  promise.
- **Concierge:** deliver the result by hand for the first customers. Automate
  later.
- **Wizard of Oz:** the customer sees a product; behind it, the founder does
  the work by hand.
- **Paid pilot (B2B):** a short, paid trial with a clear goal and an end date.

Pick the one that tests the riskiest assumption from `founder/idea.md` with
the least building. An engineer's instinct is to build first. Resist it:
nothing gets built until the test says people pay.

## Step 2: the offer

Use the offer value lens (from *$100M Offers* by Alex Hormozi): buyers value
an offer more when the outcome is bigger and more likely, and less when it
takes long or asks a lot of effort.

1. List the obstacles between the buyer and the result, in their words, from
   the interviews and the competitor complaints in `founder/research.md`. Aim
   for 10 to 30.
2. Turn each obstacle into a solution. Score each on value to the buyer (1 to
   5) and cost to deliver (1 to 5, from the numbers). Keep high value at low
   cost.
3. Build the offer:
   - **Core:** described by the outcome, not the features.
   - **Bonuses:** two or three, each removing one specific objection.
   - **Guarantee:** what happens if it doesn't deliver. Run the cost at a
     realistic claim rate with the numbers script
     (`unit_economics.py --cost`) before promising it.
   - **Urgency:** only if it is true, such as a first batch or a launch date.
     Never a fake countdown or "only 3 left".
   - **Name:** clear and specific.
4. Check the price against `founder/numbers.md`. If the offer adds costs,
   re-run the numbers.

## Step 3: what the test needs

**B2C or self-serve:**

- A landing or pre-sale page: the outcome, who it's for, what they get, the
  price, the guarantee, the delivery date, and one button. The model writes
  the copy, and the HTML if the user wants it.
- A payment link (Pix, Mercado Pago, Stripe or similar) that the user sets
  up. Recommend a test purchase and refund before launch.
- A consent checkbox for contact by email or WhatsApp, kept apart per channel,
  with a record of when and where consent was given (LGPD in Brazil, GDPR in
  the EU).
- The refund policy in plain words, including the legal window (7 days for
  online sales in Brazil, 14 in the EU).

**B2B:**

- A one-page proposal: the problem in the buyer's words, the outcome, the
  pilot (scope, length, price, success measure) and the next step.
- A letter of intent template: who, what, an estimated value and a date.
- The pilot contract points to check with a lawyer, including refunds.

**For each channel chosen in step 3:** three to five ad or post drafts that
differ in angle, not in wording. Draw the angles from the pain, the outcome,
proof, a common objection, and the founder's story. Small budgets find
winners by trying very different ideas, not by tweaking one.

Write everything in `founder/offer.md`.

## Gate 4: ready to sell

**Rule:** the page or proposal is live, a test payment went through and was
refunded, consent and refund terms are on the page, and the user has
approved every public text.

## Gate rules

These are the same in every step.

- Propose the threshold from the user's own numbers, explain it in one line,
  and get the user's OK before the work starts. Set a deadline.
- **Pass:** the devil's advocate speaks, then the user decides.
- **Fail:** change one thing (offer, price or format) and retry. After 3
  tries the user picks: pivot to `/founder-idea`, or stop.
- **Deadline missed:** inconclusive, treated as a fail.
- **Skip:** allowed. The devil's advocate speaks first and the reason is
  logged.

**Devil's advocate:** one argument, the strongest reason to stop, built from
the user's evidence. End with "I'd stop because X. I'd change my mind if Y,"
where Y is the cheapest test that would prove it wrong. If the evidence is
strong, say "I tried to argue against this and couldn't."

Log the gate in `founder/evidence.md`:

```
## Gate 4: offer (<date>)
Rule: <what must be true>  Threshold: <number>  Deadline: <date>  Try: <1-3>
Result: PASS | FAIL | INCONCLUSIVE | SKIP
Evidence: <links to the page, the test payment, the approved texts>
Devil's advocate: I'd stop because ... I'd change my mind if ...
Decision: <continue | retry: what changes | pivot | stop>, because ...
```

## Rules

- Every promise must be deliverable and affordable.
- No fake reviews, testimonials, follower counts, scarcity or "as seen on".
  Interview quotes are research, never testimonials.
- Follow the advertising and consumer rules of the user's market, especially
  for health, money and results claims. Not legal advice.

## Output

`founder/offer.md` and the page or proposal files. Next: `/founder-test`.
