# No-bullshit founder

Before you build anything, it reads 100 real people talking about your
problem. Then it makes strangers pay before you call it a business.

Claude skills that test a business idea on people who pay, not on agents who
agree. Being tested with real money. Free, MIT.

A fork of [founder-skill](https://github.com/Jakeschincariol/founder-skill) by
Jake Schincariol, being rebuilt from scratch.

## The hypothesis

Only real buyers can prove demand. Agents can't: asked whether they would
buy, they say yes too easily. Demand alone doesn't make a good business,
though. The numbers have to work too, and the things buyers never mention have
to check out: costs, suppliers, regulation, competitors.

So agents do two jobs here. They do the desk research. And they keep you from
repeating mistakes other founders already made: pricing below cost, no
break-even, testing on friends, spending before you know what success looks
like, calling a winner on three sales.

A good business here means people pay at a price where the numbers work, and
then they buy again.

This is a hypothesis, not a result. It is wrong if:

- across several tests, the model's predicted conversion lands within a
  margin set in advance of the real conversion on the same offer. Then agents can judge
  demand, and the real-buyer step is overkill.
- ideas that passed the buyer test later fail, through refunds, no repeat
  purchase or losses. Then the test is measuring the wrong thing.

Each test logs both numbers, so the hypothesis can be checked.

## Why I changed the approach

I'm an engineer. I can build, talk to clients and read numbers and ads, but
I've never validated a business. The original pack promised to test an idea
with 100 buyer agents. When I looked inside, the panel was one model
answering itself 100 times, and the business plan used its buy rate to call
the idea profitable. Models lean agreeable (the original skill itself says to
read the buy rate as an upper bound), so that number says more about the
model than about the market.

I kept the parts that do real work, like the numbers and the success line
written before a test, and replaced the panel. The 100 are now real people:
posts and reviews where they describe the problem, what they already pay and
what they wish existed, each with a link. That is still research, not proof.
Proof is what people give up: time, reputation, money. So every step ends in
a gate, and only interviews and real sales pass them.

## What this repo is for

A guide for people who can build but have never validated a business. It
explains each step in plain words and always tells you what comes next.

1. **Idea.** The problem, who has it, who pays, what you know and what you are
   assuming. Desk research, 100 real people who wrote about the problem, and
   interviews you run.
2. **Numbers.** Price, profit per sale, break-even and the most you can pay to
   get a customer.
3. **Channels.** Where your buyers already are, worked out from interviews,
   from where competitors advertise and from search data. Then pick one or two
   channels to test.
4. **Offer.** The smallest thing you can sell, and a page to sell it.
5. **Test.** Real buyers, paid or organic traffic, a rule written before the
   test. For B2B: interviews, letters of intent and paid pilots.
6. **Grow.** Repeat purchase, the real flow from order to delivery, one change
   at a time.

Each step has a gate. You move on only when the rule you wrote is met.

## How it works

- **The model does the hand work, you decide.** The model researches
  competitors, prices, search data and regulation, drafts the scripts, pages
  and ads, runs the numbers, and brings you each decision with options and a
  recommendation. You decide, approve spending and publishing, and talk to
  buyers. Pausing a test that is losing money runs on its own.
- **It asks instead of guessing.** When information is missing, the skill
  asks. Answers go into a `founder/` folder that the next skill reads, so
  nobody asks twice.
- **Baseline first.** Before a change, it records how things are today, with
  the number you already track and how you measure it.
- **The rule is written before the test:** a number, a date, and the result
  that would prove the idea wrong. Whoever decides agrees to it up front.
- **Warm and cold sales are counted apart.** Sales from your own network show
  the product works. Only sales to strangers show there is a market.
- **A sale counts after the refund window.** Online buyers can often cancel
  (7 days in Brazil, 14 in the EU), so a pre-sale only counts once that
  window closes.
- **A failed test is checked before the idea is blamed.** If the ad or the
  page didn't reach enough people, the test is inconclusive, not a no.
- **Scripts do the measuring and deciding.** The model drafts and summarizes.
  A loop that calls the model at every step would burn the tokens this fork
  is trying to save.
- **Every claim says where it came from**, and verified data is kept apart
  from the model's interpretation.
- **Every gate has a rule, a threshold and a deadline, set before the
  work.** The skill proposes the threshold and you confirm it. If a gate
  fails, you change one thing and retry, up to three times, then pivot or
  stop. You can skip a gate, but the skip is logged with your reason.
- **A devil's advocate speaks at each gate.** It gives the single strongest
  reason to stop and what would change its mind. Then you decide.

## The skills

| command | step | what it does |
| --- | --- | --- |
| `/founder` | guide | Reads your `founder/` folder, tells you where you are and what to do next, explains business terms |
| `/founder-idea` | 1 | Writes the idea down, ranks assumptions, does the desk research, prepares interviews you run |
| `/founder-numbers` | 2 | Profit per sale, break-even, year 1, cash needed, and the most you can pay for a customer |
| `/founder-channels` | 3 | Finds where your buyers are from evidence, ranks channels, picks one or two to test |
| `/founder-offer` | 4 | The MVP, the offer, the page or B2B proposal, and ad drafts |
| `/founder-test` | 5 | Runs the test with a rule written first, and decides with a script |
| `/founder-grow` | 6 | Baseline, real numbers, the flow from order to delivery, one change at a time |

Run them in order, or run `/founder` and it tells you which one is next.

## Install

In Claude Code:

```
/plugin marketplace add JimmyBastos/no-bullshit-founder
/plugin install no-bullshit-founder@no-bullshit-founder
```

Or copy the folders, to get plain `/founder-idea` and so on:

```bash
git clone https://github.com/JimmyBastos/no-bullshit-founder.git
cp -r no-bullshit-founder/skills/founder* ~/.claude/skills/
```

The research steps need web access. The scripts need Python 3.8 or newer and
nothing else:

```bash
python3 skills/founder-numbers/unit_economics.py founder/numbers.json   # the numbers and gate 2
python3 skills/founder-numbers/van_westendorp.py survey.csv             # price range from a real survey
python3 skills/founder-test/decide.py founder/tests/001.json            # the test result and gate 5
python3 -m unittest discover -s tests                                   # the tests
```

## Status

The seven skills are written, but no real business has gone through them
yet. Expect rough edges.

"Being tested with real money" means the skills are being run on real
businesses now. Each test goes into the repo with its rule, its numbers and
the outcome, including the ones that fail. Testing one business validates
that business, not the skills; the skills earn the word "tested" only after
several.

## Credit and license

Forked from founder-skill by Jake Schincariol, MIT. This fork is MIT too; the
original notice stays in `LICENSE`.
