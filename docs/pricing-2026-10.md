# Astrovarium price: the check before the Money block

Astrovarium session, 29 Oct 2026, run at Dafa's request through `/be-ambitious`. Decided by Dafa
the same day: **$29.99 once**, **$19.99 for the first month after launch**, founding testers get
Astrovarium 1 free for good. This file is what that decision was checked against, and what is still
unchecked.

## 1. What the competitors charge, by country (App Store, read 29 Oct 2026)

| app | US | UK | Germany | Israel | Brazil | India | Georgia | ratings, US / others |
|---|---|---|---|---|---|---|---|---|
| iPhemeris (paid upfront) | $29.99 | £29.99 | €34.99 | ₪99.90 | R$199.90 | ₹2,999 | $34.99 | 1,118 / 72 DE, 103 GB |
| Time Nomad | $8.99 | £8.99 | €9.99 | ₪29.90 | free | free | free | 2,745 / 136 DE, 241 GB |
| Astro Gold | free + "Gold Monthly" $7.99, a $0 "Gold Level Free Trial", reports $2.99-3.99, Astrolocality Maps $24.99 | | | | | | | 234 |
| TimePassages | free + charts $0.99 each, Pro $7.99 a month or $59.99 a year | | | | | | | 44,121 |

- **The paying market is the US first, then the UK and Germany**: iPhemeris has 1,118 US ratings
  against 13 in India and 1 in Georgia.
- **Apple's default price equalisation makes the same app dearer in poorer countries**: iPhemeris
  is about $36 in Brazil and $34 in India. A manual lower price for those storefronts is possible
  later; with this little volume there it is not worth doing before launch.
- **Astro Gold's lifetime price** ($69.99 on iOS, from a third-party listing of August 2026) is not
  confirmed: the App Store page lists only its ten top in-app purchases, and lifetime is not among
  them. Its "Gold Level Free Trial" at $0.00 is the same mechanism we plan (a $0 one-time item
  named as a trial, guideline 3.1.1).

## 2. What buyers say about price, in their own words

From the 500 most recent US reviews of each (1,373 read, 249 mention money):

- **Professionals do not call $29.99 expensive.** "I've been a teacher of astrology for nearly 15
  years. This is an inexpensive app that really delivers" (iPhemeris, $29.99). "I have other, more
  expensive astrology apps... this is my Go To" (an astrologer of 40 years). One dissent: "is that
  worth $18?" about a feature add-on.
- **The anger is about three other things, never the headline price:**
  1. **costs found after paying:** "You pay $8.99 to download the app only to find out you will
     need to pay $50 for a bundle to have access to basic features" (Time Nomad, 1 star);
  2. **a one-time payment turned into a subscription:** "I paid for a pro membership in Sept 2024,
     it was a one time fee... Now all of a sudden it says I am a 'free' user" (TimePassages,
     1 star); "the additional options are subscription based instead of purchase based" (iPhemeris);
  3. **paying again or losing data:** "every time I try to transfer my account onto a new device,
     suddenly it wants me to pay for the charts all over again" (TimePassages); "I've lost 300~
     charts again because this app has lost its iCloud function" (Astro Gold).
- **What is praised:** "one time payments for add ons, not subscription based" (Time Nomad, 5
  stars).

**What follows:** at $29.99 the price itself is not where we lose people. We lose them if the
payment does not cover everything, if "once" ever changes, or if charts are lost. So the unlock is
one item that opens every paid feature, the licence rule is written on the purchase screen (CLAUDE.md,
Money), and the iCloud and Google Drive sync on the roadmap matters for sales, not only comfort.

## 3. How to show $19.99 honestly

- **There is no introductory price for a one-time purchase in the App Store**: introductory offers
  exist only for auto-renewable subscriptions. What exists is a **scheduled price change**: $19.99
  from launch, $29.99 from a set date, configured in App Store Connect in advance. The store shows
  only the price of the day; it never draws a crossed-out one.
- **In the EU a price reduction must name as its "before" price the lowest price of the previous 30
  days** (the Omnibus Directive). We will never have charged $29.99 before launch, so "$29.99,
  now $19.99" would break it. What is allowed and true: **"Launch price $19.99 until [date]; from
  [date] it is $29.99."** That is an announced future price, not an invented past one. (A reading of
  the rule, not legal advice.)
- **For founding testers:** "Astrovarium 1, $29.99 from [date] - yours free". True from the day the
  price is set.

## 4. The money per tier

Apple keeps 15% under the Small Business Program. Per 100 people who start the 7-day trial, with c
the share who buy:

| price | net per sale | net per 100 trials |
|---|---|---|
| $19.99 | $16.99 | 16.99 × c |
| $29.99 | $25.49 | 25.49 × c |

**$29.99 earns more as long as the share buying at $29.99 is at least two thirds of the share buying
at $19.99.** If the launch month converts 6% and the month after at least 4%, the higher price wins.

## 5. What the testers are asked instead of "yes / no"

The single question "would you pay $9.99?" was replaced on 29 Oct (it asked about the wrong price
and invites a polite yes). The testers get the four Van Westendorp questions and one ladder, at the
end of their week:

1. At what price would Astrovarium seem so cheap that you would doubt its quality?
2. At what price would it be a bargain, a great buy?
3. At what price would it start to feel expensive, though you might still buy it?
4. At what price would it be too expensive to consider?
5. Would you buy it once at $14.99 / $19.99 / $29.99 / $39.99? (yes or no at each)

With 10-20 answers the curves are rough, so the reading is the range, not a point.

## 6. The checks that decide it, outside Dafa and this session

- **Testers' range** (15 Nov 2026): **pass** if $29.99 sits below the median "too expensive" and
  above the median "too cheap". **Fail** if the median "expensive" is below $29.99: then the price
  is $19.99 and the launch discount goes.
- **Real purchases** (the first month at $19.99 against the month after at $29.99): **pass** if the
  net per trial at $29.99 is not lower than at $19.99, which is a buy rate at least two thirds of
  the launch month's. **Fail**: return to $19.99 and write down both rates.
- **Refunds** (App Store Connect reports): a rise after the change to $29.99 says the price
  surprised people, whatever the conversion.

## 7. Not checked

- Astro Gold's lifetime price on the store itself.
- Prices of ZET Geo and the desktop programs today (MARKET.md, 25 Sep: ZET Geo 4,000 ₽).
- Whether offer codes for a one-time purchase work in the sandbox (reported failing for some
  developers; _HQ, 29 Oct).
- Apple's own page on scheduled price changes and the EU text, read in full.
