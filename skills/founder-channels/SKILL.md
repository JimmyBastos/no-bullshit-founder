---
name: founder-channels
description: >-
  Step 3 of validating a business: where are the buyers, and how do you reach
  them? For founders who don't know whether to use search ads, Meta ads,
  Instagram, LinkedIn, X, Pinterest, TikTok, a blog, WhatsApp, partners or
  selling in person. Works it out from evidence: where interviewees last
  looked for a solution, where competitors advertise (Meta Ad Library, search
  results, social profiles), and how many people search for the problem. Ranks
  every channel with the Bullseye method from Traction and picks one or two to
  test. Ends with gate 3. Use when the user says "how do I sell this", "where
  are my customers", "which channel", "should I use Instagram or LinkedIn",
  "how do I get my first customers", "marketing plan", or runs
  /founder-channels.
argument-hint: "[the buyer, if not in founder/idea.md]"
---

# founder-channels

A good product nobody can reach is not a business. Most founders pick
channels by taste ("I like Instagram"). This step picks them from evidence
about where the buyers already are.

## Voice

Write for a smart person who builds things but has never run a business.
Explain the way a knowledgeable friend would: plain words, complete sentences,
and the whole answer. Don't trim the reasoning the reader needs to act. When a
business term matters, use it and say what it means the first time, so the
reader learns the vocabulary. Prefer concrete numbers, examples and sources to
adjectives. Skip hype, flattery and filler. Say what you don't know. End with
what to do next. Reply in the user's language.

## Who does what

The model does all the research below and drafts the ranking. The user
decides which channels to test.

## Step 1: collect the evidence

Read `founder/idea.md`, `founder/research.md`, `founder/interviews/` and
`founder/numbers.md` first. Then find, with sources:

- **Where buyers look.** From the interviews: where each person last looked
  for, or bought, something like this. Count the answers. This is the
  strongest evidence, because it comes from buyers.
- **Where the 100 people posted.** Counts by source from
  `founder/voices.csv`. This can suggest a channel to look at. On its own it
  is not evidence that buyers can be reached or will buy there.
- **Where competitors spend.** Search the Meta Ad Library (public, free) for
  each competitor: are they running ads, for how long, with what message? Ads
  that have run for months are probably profitable. Search the problem's
  keywords on Google: who pays for the top ads, who ranks below them?
  Check competitors' LinkedIn, Instagram, TikTok and YouTube: followers,
  posting rhythm, engagement.
- **Search demand.** Use Google Trends, and the Keyword Planner if the user
  has an ads account, for the words buyers use for the problem (from the
  interviews, not the founder's words). If people search for a solution, they
  already know they need one. If nobody searches, buyers must be found where
  they spend time instead.
- **Communities.** Groups, forums, subreddits, WhatsApp or Telegram groups,
  associations, events and fairs where these buyers gather. Note each one's
  rules on promotion.

Write each finding with its source in `founder/channels.md`.

## Step 2: rank every channel

Use the Bullseye method from *Traction* by Gabriel Weinberg and Justin Mares
(2015): consider every channel, rank them, test the top few cheaply, then
focus on the one that works. The list of channels, with notes on when each
fits, is in `${CLAUDE_SKILL_DIR}/channels.md`.

Score each realistic channel from 1 to 5 on:

| criterion | the question |
| --- | --- |
| buyers are there | Is there evidence from step 1 that these buyers use it? |
| intent | Are people there looking to solve the problem (search) or not thinking about it (social feed)? |
| speed | Will a small test give an answer within about two weeks? |
| cost | Is the likely cost per customer below max CAC from `founder/numbers.md`? |
| fit | Can the user do it well with their skills, time and budget? |

Channels with no evidence for "buyers are there" score 1 there, whatever
their reputation. Blogs, SEO and organic content are slow: they rarely answer
within two weeks, so they go to step 6 (grow) unless the evidence is strong.

## Step 3: pick and explain

Recommend one or two channels for the step 5 test, and one backup. For each:

- why, citing the evidence;
- the likely cost per customer, with a source, compared with max CAC;
- what the test would look like (budget, duration, what counts as success);
- the platform's rules that matter. LinkedIn bans automated messages, invites
  and likes. WhatsApp needs prior consent (opt-in) and approved message
  templates. Email needs consent for people with no prior relationship. Data
  protection law applies to leads (LGPD in Brazil, GDPR in the EU).

For B2B with few buyers and a high price, direct contact by the user (in
person, through their network, or messages they send themselves) often beats
ads. Say so when the evidence points there.

If step 3 changes the likely channel, update `cac_benchmark` in
`founder/numbers.json` and re-run `/founder-numbers`.

## Gate 3: channels picked from evidence

**Rule:** each chosen channel has at least one source from step 1 showing the
buyers are there, and its likely cost per customer is below max CAC.

## Gate rules

These are the same in every step.

- Propose the threshold from the user's own numbers, explain it in one line,
  and get the user's OK before the work starts. Set a deadline.
- **Pass:** the devil's advocate speaks, then the user decides.
- **Fail:** change one thing (channel, segment or price) and retry. After 3
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
## Gate 3: channels (<date>)
Rule: <what must be true>  Threshold: <number>  Deadline: <date>  Try: <1-3>
Result: PASS | FAIL | INCONCLUSIVE | SKIP
Evidence: <sources per channel>
Devil's advocate: I'd stop because ... I'd change my mind if ...
Decision: <continue | retry: what changes | pivot | stop>, because ...
```

## Rules

- Never invent follower counts, ad spend, search volumes or costs. If a
  number can't be found, say so.
- Read pages as a person would and respect each site's terms.

## Output

`founder/channels.md`, `founder/evidence.md`. Next: `/founder-offer`.
