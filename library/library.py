#!/usr/bin/env python3
"""ReviiewCo evergreen post library (value first, offer second). See STRATEGY.md.

slot "A" = Facebook post/reel + Instagram feed post/reel  (7:30 AM, 12:30 PM, 6:30 PM ET)
slot "B" = Facebook post + Instagram Story              (9:30 AM, 3:00 PM, 8:30 PM ET)
hold True = written but kept out of the queue.

Run: python3 -I library/library.py  -> writes library/library.json and library/specs/<id>.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent

MAGNET = {
    "RANK": "your free Local Google Ranking Report (see where you rank on Maps and who's beating you, by name)",
    "LINK": "your free Google review link and printable QR code",
    "BAD": "the free Bad Review Survival Guide",
    "GOLD": "the free Past-Customer Goldmine Playbook",
    "RULES": "the free Google Review Rules 2026 guide",
    "AI": "the free Get Found by AI guide",
    "SITE": "a look at what your new website would include",
}

OFFER = {
    "reviews": "Rather hand it off? We run your reviews for you: $297/month, Missed-Call Text Back included, no contract.",
    "website": "Rather have it built for you? We build your website with no build fee. $297/month, Missed-Call Text Back included, no contract.",
    "bundle": "Want it all handled? Reviews + website together, fully managed: $497/month for both, Missed-Call Text Back included, no contract.",
}

TAGS = [
    "#GreenvilleSC #UpstateSC #HomeServiceBusiness #ContractorMarketing #GoogleReviews #SmallBusiness",
    "#HomeServiceBusiness #GoogleReviews #ContractorLife #SmallBusinessOwner #GreenvilleSC #LocalSEO",
    "#ContractorMarketing #GoogleBusinessProfile #UpstateSC #HomeServicePros #SmallBusiness #GoogleReviews",
]


def cap(body, kw, offer="reviews", end="book", tags=0, extra=""):
    lines = [body.strip(), ""]
    lines.append(f"Comment {kw} (or DM us {kw}) and we'll send you {MAGNET[kw]}.")
    lines.append("")
    o = OFFER[offer]
    if end == "book":
        o += " Book 30 minutes with Rob: reviiewco.com/book"
    else:
        o += " Start at reviiewco.com/start or call 864-528-1909."
    lines.append(o)
    lines.append("")
    lines.append((TAGS[tags % 3] + (" " + extra if extra else "")).strip())
    return "\n".join(lines)


V = "videos/ReviiewCo_{}_VO.mp4"
items = []


def video(i, ad, topic, body, kw, **k):
    items.append(dict(id=i, slot="A", kind="video", topic=topic, media=V.format(ad), keyword=kw,
                      caption=cap(body, kw, **k)))


def image(i, slot, topic, spec, body, kw, hold=False, **k):
    spec = dict(spec)
    spec.setdefault("cta", f"Comment or DM “{kw}”")
    items.append(dict(id=i, slot=slot, kind="image", topic=topic, spec=spec, keyword=kw, hold=hold,
                      caption=cap(body, kw, **k)))


# ---------------- A: videos (Rob's ads) ----------------
video("A01", "Ad1_Original_30s", "Core hook", """
Two contractors. Same town. Guess who gets the call?

The guy across town isn't better than you. He just has more reviews. When a homeowner compares contractors, the one with more fresh 5-star reviews usually gets the call.

Want to know exactly who's beating you on Google Maps, and why?""", "RANK", tags=0)
video("A02", "Ad2_MoneyOnTheTable_20s", "Money on the table", """
Every job you finish is a review you never collected.

Hundreds of happy customers. Almost nothing on Google to show for it. Not because they didn't like the work, but because nobody asked.

Your old customer list is the fastest way to fix that. We wrote a step-by-step playbook for working it yourself, with a sample text you can copy.""", "GOLD", tags=1)
video("A03", "Ad3_WhatYourCustomerSees_25s", "What the customer sees", """
Here's what your customer actually sees (sample customer "Jessica"):

A thank-you text right after the job. One tap. About ten seconds. A friendly reminder only if she hasn't posted yet.

The secret is the link. If it opens your review box in one tap, people actually leave the review. Make yours free in about a minute, no signup.""", "LINK", tags=2)
video("A04", "Ad4_MissedCall_25s", "Missed-Call Text Back", """
You're up a ladder. The phone rings. Missed call. They call the next guy.

Missed-Call Text Back texts them first, automatically, so a call you can't pick up still gets a reply from your business.

It's included free with ReviiewCo. But first, see where you stand: who Google shows ahead of you, and what to fix to pass them.""", "RANK", end="start", tags=0)
video("A05", "Ad5_ThreeBids_18s", "Three bids", """
She got three bids. She didn't pick the cheapest. She picked the most trusted.

When a homeowner compares three contractors, the one with more fresh 5-star reviews usually gets the call. That's how you stop competing on price.

Step one is knowing where you stand against the other two bids in your town.""", "RANK", tags=1)
video("A06", "Ad6_YourSoftwareAlreadyAsks_24s", "Your software already asks", """
"My job software already asks for reviews." Great. Keep it.

But it only asks customers from here on. It doesn't go back to the hundreds you've already served. And it doesn't write and post a reply to every review.

Those past customers are your biggest untapped source of reviews. Here's how to reach them without it looking like spam.""", "GOLD", tags=2)
video("A07", "Ad7_TheAwkwardAsk_21s", "The awkward ask", """
"So, uh... would you maybe leave us a review?"

Asking at the door feels awkward, so it never happens. Fix it with a text right after the job and a link that opens your review box in one tap. Nobody on your crew has to say a word.

Make your link and a printable QR code for the truck, free.""", "LINK", tags=0)
video("A08", "Ad8_HowItWorks_22s", "How it works", """
Five minutes from you. Everything else from us.

Today: add us to your Google profile, send your list. This week: past customers start speaking up, a little at a time. Ongoing: every finished job gets a request, every review gets a reply.

Doing it yourself? Start with the list you already have. Our playbook shows you how, step by step.""", "GOLD", end="start", tags=1)
video("A09", "Ad9_FromTheFounder_23s", "Founder", """
"Our system gets you reviews. Reviews build trust. Trust drives calls. Calls build your business." — Rob Warfield, Founder, Greenville SC

Real customers, real work. We never write, buy or filter reviews, and you approve every message first.

Google changed its review rules in April 2026. Before you hire anyone, or run a review contest for your techs, know what's allowed.""", "RULES", tags=2)
video("A10", "Ad10_MapPack_21s", "Google Maps", """
Someone searches "contractor near me." Who shows up first?

Reviews are one of the signals Google uses to rank local businesses. Google's own help page says more reviews and positive ratings can help your local ranking.

Find out where you rank from 49 spots around your business, and who Google shows ahead of you.""", "RANK", tags=0)
video("A11", "Ad11_HalfwaySold_21s", "Halfway sold", """
Before you knock, she's already halfway sold.

Because dozens of her neighbors already vouched for you on Google. That's what reviews do. They do the selling before you show up.

Most of those neighbors are already in your customer list. Here's how to ask them, the right way.""", "GOLD", tags=1)
video("A12", "Ad12_AfraidOfABadReview_21s", "Afraid of a bad review", """
Worried that asking for reviews will get you a bad one?

Here's the math: with 10 reviews, one 1-star drops a 5.0 to 4.6. With 100 reviews, the same 1-star still shows 5.0. Your review count is your shock absorber.

Every customer gets the same invitation (that's Google's rule), and if someone's unhappy, you hear about it first so you can make it right.""", "BAD", tags=2)
video("A13", "Ad13_22Trades_25s", "22 trades", """
HVAC. Roofing. Landscaping. Garage doors. 22 home service trades and counting.

Different work, same problem: great jobs, and not enough reviews to show for it.

See how you stack up against the other contractors in your trade and your town.""", "RANK", tags=0, extra="#HVAC #Roofing #Landscaping")
video("A14", "Ad14_DidntHappen_19s", "If it's not on Google", """
Fixed the leak. Saved their weekend. "You're a lifesaver."

If it's not on Google, it didn't happen.

The easiest way to get that thank-you onto Google: text them a link that opens your review box in one tap, right after the job. Make yours free.""", "LINK", tags=1, extra="#Plumbing #Plumber")
video("A15", "Ad15_ThreePlaces_20s", "One review, three places", """
One happy customer. One review. Three places it works for you: your Google profile, your social media, and your website. Plus a reply posted in your name.

That only works if your website is doing its job: quote button on every page, tap-to-call, and a page for every service in every town you cover.

Want to see what a site built for calls looks like?""", "SITE", offer="website", tags=2)
video("A16", "Ad16_YouStayInControl_22s", "You stay in control", """
It's your business. You stay in control.

You keep ownership of your Google profile (we get manager access only). You approve every message. Texts go out during business hours. Two follow-ups max. No contract.

Before you hand your reviews to anyone, ask these 8 questions. Our free guide lists them, plus what Google and the FTC allow.""", "RULES", tags=0)
video("A17", "Ad17_StaleReviews_19s", "Stale reviews", """
Your last Google review: 8 months ago (illustration). The guy down the road: yesterday.

Homeowners notice. Fresh reviews say you're busy and you're good.

The fastest way to get fresh ones is the customers you've already served. Here's the step-by-step to ask them yourself.""", "GOLD", tags=1)
video("A18", "Ad18_YourListIsWorthMore_18s", "Your list is worth more", """
That list of past customers sitting in your software is worth more than you think.

Spreadsheet, CSV, phone contacts, it all works. Clean it, send in steady batches, follow up once or twice, then stop.

Our guarantee: send us 300+ past customers and get at least 10 new Google reviews in 30 days, or every dollar back.""", "GOLD", end="start", tags=2)
video("A19", "Ad19_AWeekInTheLife_21s", "A week in the life", """
A week in the life (sample):

Monday 2:00 PM, you finish the job. 2:05 PM, your customer gets a friendly text. Wednesday, no review yet, so one friendly reminder. Wednesday night, five stars, and a reply posted in your name.

And you? You just kept working. Curious where your Google profile stands right now?""", "RANK", end="start", tags=0)

# ---------------- A: feed images ----------------
image("A20", "A", "Core hook", dict(eyebrow="Free report", headline="He's not better than you. [[He just has more reviews.]]", body="See who Google shows ahead of you, by name, and what to fix to pass them.", photo="assets/home-service-crew-with-work-vans.jpg", layout="photo"), """
The guy across town isn't better than you. He just has more reviews.

Our free Local Google Ranking Report shows you:
• Your Google Maps rank from 49 spots around your business
• The competitors Google shows ahead of you, by name
• Your reviews, listings and profile, checked
• What to fix to pass them, in plain English

Takes about a minute. Yours to keep, no sales call needed.""", "RANK", tags=1)
image("A21", "A", "Missed-Call Text Back", dict(eyebrow="Can't pick up?", headline="On a ladder. Phone rings. [[They still hear from you.]]", body="Missed-Call Text Back texts the caller from your business, right away. Free with ReviiewCo.", photo="assets/trades/roofer.jpg", layout="photo", cta="reviiewco.com/start"), """
Every missed call is a homeowner deciding whether to call the next guy.

Missed-Call Text Back sends them a text from your business the moment you miss the call, so they hear from you first.

It's included free with our Review Management System and our websites.

Before you pick, see how you stack up on Google in your own backyard.""", "RANK", end="start", tags=2)
image("A22", "A", "DIY vs done-for-you", dict(eyebrow="What it really costs", headline="Do it yourself, or [[hand it off?]]", body="Job software add-on: $0–$99. Review app: $45–$125. Done for you: $297–$400. (Oct 2026)", layout="type"), """
There are five ways to handle reviews, and the real question isn't price. It's who does the work.

Job software features and review apps are cheap, but you're the one running them every week. Done-for-you services cost more, but nobody on your team has to touch it.

Two questions decide it: will anyone on your team run a tool every week? And will you sign a 12-month contract? If both answers are no, look at done-for-you.

Our free guide has the 8 questions to ask anyone before you sign.""", "RULES", tags=0)
image("A23", "A", "Founder", dict(eyebrow="Rob Warfield, Founder", headline="Reviews build trust. [[Trust drives calls.]]", body="Real reviews from real customers. You approve every message first.", photo="assets/rob-warfield-founder.jpg", layout="photo", cta="reviiewco.com/book"), """
I'm Rob, the founder of ReviiewCo, here in Greenville, SC.

I built this for owners who are great at their trade and have zero time to chase reviews. We never write, buy or filter reviews, and you approve every message first.

If you'd rather do it yourself, I'll give you the playbook for free. If you'd rather hand it off, let's talk.""", "GOLD", tags=1)
image("A24", "A", "Website", dict(eyebrow="Websites for the trades", headline="We build it. [[No build fee.]]", body="Custom design, live in about 10 business days. $297/month, no contract.", layout="type", cta="Comment or DM “SITE”"), """
Your website should bring in calls, not just sit there like a business card.

We build it for you, with no build fee:
• Custom design with your real photos
• Quote button and tap-to-call on every page
• A page for every service in every town you cover
• Sent to Google the day you launch
• Unlimited changes, live within two business days

Live in about 10 business days.""", "SITE", offer="website", tags=2)
image("A25", "A", "Website: service + town pages", dict(eyebrow="Get found in your towns", headline="Google can't send you work for [[pages that don't exist.]]", body="One page for each service in each town you cover. That's how you show up when they search.", photo="assets/hero-technician-review-notification.jpg", layout="photo", cta="Comment or DM “SITE”"), """
If you do water heater installs, drain cleaning and repiping across five towns, how many pages does your website have for that?

Search engines can't send you work for pages that don't exist. Experts in Whitespark's 2026 survey also ranked a page per service near the top for showing up in AI search.

DIY: write one page per service, per town: what you do, where, and what to expect.""", "SITE", offer="website", tags=0)
image("A26", "A", "Trade spotlight: HVAC", dict(eyebrow="HVAC owners", headline="When the AC dies in July, [[they call who they trust.]]", body="A homeowner with no AC isn't shopping long. Your reviews do the selling before you pick up.", photo="assets/trades/hvac-technician.jpg", layout="photo"), """
HVAC owners: when the AC quits in July, nobody reads ten websites. They look at Google Maps, see who has the most fresh 5-star reviews, and call.

So the question is: when someone in your town searches for AC repair, where do you show up?

Our free report checks your rank from 49 spots around your business and shows the competitors ahead of you.""", "RANK", tags=1, extra="#HVAC #HVACLife #ACRepair")
image("A27", "A", "Trade spotlight: roofing", dict(eyebrow="Roofing owners", headline="A new roof is a big check. [[Reviews make it easy to sign.]]", body="Big-ticket jobs get researched. Recent, real reviews are what they read.", photo="assets/trades/roofer.jpg", layout="photo"), """
Roofing is a big-ticket decision. Homeowners research it, compare bids, and read reviews before they let anyone on the roof.

Your past customers already trust you. Most of them were just never asked.

Our free playbook walks you through turning that old customer list into reviews: clean it, text in steady batches, follow up twice, then stop.""", "GOLD", tags=2, extra="#Roofing #Roofer #RoofingContractor")
image("A28", "A", "Trade spotlight: landscaping", dict(eyebrow="Landscaping owners", headline="You see the same yards every week. [[Ask them once.]]", body="Your regulars love your work. A one-tap review link turns that into proof.", photo="assets/trades/landscaper.jpg", layout="photo"), """
Landscaping owners: you've got regulars who've loved your work for years. How many of them have reviewed you on Google?

Text them a link that opens your review box in one tap. Print the QR code for your trailer and leave-behind cards.

Make your link free in about a minute. No signup, nothing stored.""", "LINK", tags=0, extra="#Landscaping #LawnCare #Landscaper")
image("A29", "A", "Trade spotlight: plumbing", dict(eyebrow="Plumbing owners", headline="One bad review hits harder [[when you only have ten.]]", body="10 reviews: one 1-star takes a 5.0 to 4.6. 100 reviews: it still shows 5.0.", photo="assets/trades/plumber.jpg", layout="photo"), """
Plumbers get the angry calls: the emergency at 2 AM, the bill nobody expected. Sooner or later, one turns into a 1-star review.

With 10 reviews, that one 1-star drops a 5.0 to 4.6. With 100 reviews, it barely moves you.

Our free guide shows the math, how many 5-stars it takes to recover, and exactly what to say back.""", "BAD", tags=1, extra="#Plumbing #Plumber #PlumbingBusiness")
image("A30", "A", "Guarantee", dict(eyebrow="Our guarantee", headline="10 new Google reviews in 30 days, [[or every dollar back.]]", body="When you send us a list of 300+ past customers. The 30 days start once we have your list and Google access.", layout="type", cta="reviiewco.com/start"), """
We put it in writing: at least 10 new Google reviews within 30 days when you send us a list of 300+ past customers, or a refund of everything you paid. The clock starts once we have your list and access to your Google profile.

$297/month, Missed-Call Text Back included, no contract, no setup fee.

Not ready? Start with the free playbook and work your list yourself.""", "GOLD", end="start", tags=2)

# ---------------- B: Facebook post + Instagram Story ----------------
image("B01", "B", "Bad review math", dict(eyebrow="The rating math", headline="10 reviews. One 1-star. [[5.0 becomes 4.6.]]", body="Your star rating is an average. Your review count is your shock absorber.", layout="type"), """
Your Google rating is basically total stars divided by number of reviews.

Ten perfect reviews, then one 1-star: 51 ÷ 11 = 4.6. A hundred perfect reviews, then one 1-star: 501 ÷ 101 = still shows 5.0.

Same customer, same complaint. Very different damage.""", "BAD", tags=0)
image("B02", "B", "Recovery formula", dict(eyebrow="Do the math on your phone", headline="19 five-stars to undo [[one bad day.]]", body="5-stars needed = (target × reviews − total stars) ÷ (5 − target). Round up.", layout="type"), """
Every "Google review calculator" online runs one formula:

New 5-stars needed ≥ (T × N − S) ÷ (5 − T)
T = rating you want, N = reviews you have, S = total stars. Round up.

Example: 49 stars across 11 reviews (showing 4.5). Getting back to 4.8 takes 19 five-star reviews.""", "BAD", tags=1)
image("B03", "B", "Replying to a bad review", dict(eyebrow="Copy this reply", headline="Got a 1-star? [[Reply once. Calmly.]]", body="Thank them. Own what's yours. Take it offline with a name and a number.", layout="type"), """
Example reply to a 1-star (sample):

"Mike, I'm sorry we ran late and didn't call ahead. That's on us. I'd like to make it right. Please call me directly at the shop. — Rob, owner"

What not to do: argue, call them a liar, or share their invoice. The next homeowner reads your reply and sides with them.""", "BAD", tags=2)
image("B04", "B", "4.5-star line", dict(eyebrow="Why tenths matter", headline="31% only call businesses [[rated 4.5 or higher.]]", body="BrightLocal, Local Consumer Review Survey 2026.", layout="type"), """
BrightLocal's 2026 survey: 31% of consumers will only use a business rated 4.5 stars or higher. 68% need 4 stars or more.

So a business sitting at 4.5 with only 11 reviews is one mediocre review away from dropping below the line almost a third of shoppers use.

The fix isn't avoiding bad reviews. It's building enough good ones that one bad day can't move you.""", "BAD", tags=0)
image("B05", "B", "Review link", dict(eyebrow="Free tool", headline="Stop saying “[[search for us]] on Google.”", body="Send a link that opens your review box in one tap. Free, no signup.", layout="type"), """
"Just search for us on Google and leave a review" loses most people before they find you.

A direct review link opens your review box in one tap. Text it after every job, add it to invoices and follow-up emails.

Make yours free, plus a QR code you can print. No signup, nothing stored.""", "LINK", tags=1)
image("B06", "B", "QR code on the truck", dict(eyebrow="5-minute fix", headline="Put your review QR code [[on the truck.]]", body="Truck, counter, invoices, leave-behind cards. Everywhere a happy customer looks.", photo="assets/home-service-crew-with-work-vans.jpg", layout="photo"), """
Your trucks drive past your best customers every day. Give them a way to say thanks.

Print your Google review QR code on the truck, the counter, your invoices and a leave-behind card. One scan opens your review box.

Free generator: no signup, nothing stored.""", "LINK", tags=2)
image("B07", "B", "Ask everyone", dict(eyebrow="Google's rules", headline="Only asking happy customers? [[That's against Google's rules.]]", body="It's called review gating. Ask every customer, the same way.", layout="type"), """
Sending happy customers to Google and unhappy ones to a private form has a name: review gating. Google's policy prohibits it. It's your profile at risk.

The safe way: ask every customer the same way, and give unhappy customers an easy way to reach you directly, too.

Our free 2026 rules guide lists what's allowed and what isn't.""", "RULES", tags=0)
image("B08", "B", "No incentives", dict(eyebrow="Google + FTC", headline="$10 off for a review? [[Don't.]]", body="No payment, discounts, gifts or free service in exchange for a review.", layout="type"), """
Google's policy says businesses must not offer incentives "such as payment, discounts, free goods and/or services" for a review. The FTC's rule also bars incentives tied to a positive or negative review.

Ask every customer, and give nothing in return for the review.

Get the full do's and don'ts, free.""", "RULES", tags=1)
image("B09", "B", "April 2026 rule change", dict(eyebrow="New in April 2026", headline="“Please mention Mike” [[is out.]]", body="Google now bans asking for reviews that name a staff member.", layout="type"), """
Google tightened its review rules in April 2026. Businesses must not ask staff to collect reviews that include specific content, including content that names a staff member.

So "please mention Mike in your review" and per-tech review contests are out. If a customer names your tech on their own, that's fine.

Get the full 2026 rules, free.""", "RULES", tags=2)
image("B10", "B", "No review quotas", dict(eyebrow="New in April 2026", headline="Review quotas for your techs? [[Banned.]]", body="Reward your crew for good work you measure yourself, not for reviews.", layout="type"), """
Since April 2026, Google's policy says businesses must not ask staff to bring in a certain number of reviews.

If you want to reward your techs, tie it to service quality you measure yourself, not to reviews. And send every customer the same neutral request.

Our free guide covers what changed and how to stay safe.""", "RULES", tags=0)
image("B11", "B", "8 questions", dict(eyebrow="Before you sign anything", headline="8 questions to ask [[any review company.]]", body="Contract? Who does the work? Do you ask everyone? What if it doesn't work?", layout="type"), """
Before you pay anyone to help with reviews, ask:

1. Is the price published, and what isn't included?
2. Is there a contract, and how do I leave?
3. Who actually does the work?
4. Do you ask every customer, or only the happy ones?
5. What about customers I've already served?
6. Who replies to reviews, and how fast?
7. What happens if it doesn't work?
8. What happens to my reviews if I leave?

Full answers in our free guide.""", "RULES", tags=1)
image("B12", "B", "Your reviews if you leave", dict(eyebrow="Know before you sign", headline="If you cancel, [[the reviews stay yours.]]", body="They live on your Google profile. Your profile belongs to your business.", layout="type"), """
Question to ask any review company: what happens to my reviews if I leave?

The right answer: they stay on your Google profile, because it belongs to your business. With us, you keep ownership of your profile (we get manager access only), and you keep every review.

Get the other 7 questions to ask, free.""", "RULES", tags=2)
image("B13", "B", "Past customers", dict(eyebrow="The untapped list", headline="Hundreds of happy customers. [[Nobody asked them.]]", body="Your old customer list is the biggest source of reviews you're not using.", layout="type"), """
Most contractors are sitting on years of happy customers who never left a review, just because nobody asked.

Job software review features only ask new customers. That old list is the gold mine.

Our free playbook shows you how to work it yourself, step by step.""", "GOLD", tags=0)
image("B14", "B", "Sample text", dict(eyebrow="Copy this text", headline="One sentence of thanks. [[One link.]]", body="“Hi [name], it's [you] at [business]. Would you share how it went on Google? [link]”", layout="type"), """
Sample text to a past customer (fill in the brackets):

"Hi [first name], it's [your name] at [your business]. We [the job we did] a while back, and I hope it's still holding up. If you have a minute, would you share how it went on Google? [link] It helps a small local business more than you'd think. Thanks either way."

No reward, no request for five stars, no guilt.""", "GOLD", tags=1)
image("B15", "B", "Steady batches", dict(eyebrow="Don't blast your list", headline="400 texts on a Saturday night? [[Don't.]]", body="A small number each day looks natural and keeps you inside text limits.", layout="type"), """
When you work your old customer list, pace it.

A small number each day looks natural, keeps you inside text-message limits, and gives you time to answer replies. Send during business hours. Honor every STOP right away.

Full step-by-step in our free playbook.""", "GOLD", tags=2)
image("B16", "B", "Follow-ups", dict(eyebrow="The follow-up rule", headline="Remind them twice. [[Then stop.]]", body="People forget, so one or two friendly reminders. Stop the moment they post.", layout="type"), """
Most people who don't leave a review just forgot.

One or two friendly reminders, a couple of days apart. Then stop. And stop the moment they've posted.

That's exactly how we run it for our customers: up to two follow-ups, business hours only, opt-outs honored on every text.""", "GOLD", tags=0)
image("B17", "B", "Replying to good reviews", dict(eyebrow="Reply to the good ones too", headline="“Thanks for your review!” [[says nothing.]]", body="Short, personal, in your own voice. Mention the job. Never copy-paste.", layout="type"), """
Example review (sample): "New water heater went in fast and the crew was great with our dog."

Weak reply: "Thank you for your review! We appreciate your business!"

Good reply: "Thanks, Linda. Glad the new water heater is keeping up with the whole family. Marcus said your dog supervised the entire install. Call us anytime."

Homeowners read the replies too. We write a reply to every review, in your voice.""", "GOLD", tags=1)
image("B18", "B", "AI search", dict(eyebrow="AI search", headline="45% now ask AI [[for local picks.]]", body="Up from 6% a year earlier. BrightLocal, 2026.", layout="type"), """
In BrightLocal's 2026 survey, the share of people using ChatGPT or other AI tools for local recommendations jumped from 6% to 45% in one year.

When someone asks AI for "the best roofer in Greenville," where does the answer come from? Google's AI tools lean on Google Maps data, including your reviews.

Our free guide shows what's known, what's a guess, and 5 things you can do this week.""", "AI", tags=2)
image("B19", "B", "Google AI reads reviews", dict(eyebrow="Google's AI", headline="Google's AI is [[reading your reviews.]]", body="“People talk most about” and “Tips from reviewers” are summaries of your Google reviews.", layout="type"), """
Tap a business in the Gemini app and you can see AI-written sections like "People talk most about" and "Tips from reviewers." Those are summaries of that business's Google reviews.

So a steady flow of real, recent reviews gives the AI fresh, accurate things to say about you.

Get the free Get Found by AI guide.""", "AI", tags=0)
image("B20", "B", "15-minute AI test", dict(eyebrow="Try this tonight", headline="Ask ChatGPT who to hire. [[Are you on the list?]]", body="Write down who comes up, and which sources it cites. That's where AI is looking.", layout="type"), """
15-minute test:
1. Open ChatGPT, the Gemini app and Google's AI Mode.
2. Ask: "Who's the best [your trade] in [your town]?"
3. Write down who comes up and what sources each tool cites.
4. Check if you're mentioned, and if your details are right.

If the same competitor keeps coming up, that tells you where AI is looking in your market.""", "AI", tags=1)
image("B21", "B", "Same info everywhere", dict(eyebrow="5-minute check", headline="Same name. Same address. [[Same phone. Everywhere.]]", body="Google, Facebook, Yelp, Bing. Mismatched info makes it harder to be sure who you are.", layout="type"), """
Pull up your Google profile, your Facebook page, Yelp and Bing side by side. Is the business name, address, phone and hours exactly the same?

Mismatched info makes it harder for Google, and for AI tools that read those sites, to be sure who you are.

More quick wins in our free Get Found by AI guide.""", "AI", tags=2)
image("B22", "B", "Ranking report", dict(eyebrow="Free report", headline="Where do you rank on Maps from [[49 spots around you?]]", body="We search your trade from 49 points and pin where you show up from each one.", layout="type"), """
Your Google Maps rank changes block by block. You might be #1 at your shop and invisible two miles away.

Our free Local Google Ranking Report searches your trade from 49 spots around your business and pins where you rank from each one, plus the first 10 businesses Google shows instead.

About a minute to request. Yours to keep.""", "RANK", tags=0)
image("B23", "B", "Who Google shows first", dict(eyebrow="Free report", headline="Who is Google showing [[instead of you?]]", body="The first 10 businesses at your address, with their ratings and review counts.", layout="type"), """
Want to know exactly who you're losing calls to?

Our free report lists the first 10 businesses Google shows at your address, with their ratings and review counts. Then it spells out what to fix to pass them, in plain English, with honest time estimates.

No sales call needed.""", "RANK", tags=1)
image("B24", "B", "Website: calls not clicks", dict(eyebrow="Your website's job", headline="Mid-problem, on a phone. [[Can they call you in one tap?]]", body="Quote button, tap-to-call and a short form, right up top on every page.", layout="type", cta="Comment or DM “SITE”"), """
Most homeowners land on your website from their phone, in the middle of a problem.

DIY check: open your site on your phone. Can you call in one tap without scrolling? Is there a quote button on every page? A short form before the fold?

If not, we'll build you one that does. No build fee.""", "SITE", offer="website", tags=2)
image("B25", "B", "Website: unlimited changes", dict(eyebrow="Websites", headline="New photo? New price? [[Live in two business days.]]", body="Unlimited changes, as often as you need. $297/month, no build fee.", layout="type", cta="Comment or DM “SITE”"), """
Most contractor websites are out of date the week they launch, because changing anything means calling the web guy.

Ours: send over a new photo, price or service and it's live within two business days, as often as you need. Plus a page for every service in every town, sent to Google on launch day.

We build it with no build fee.""", "SITE", offer="website", tags=0)
image("B26", "B", "Missed-Call Text Back", dict(eyebrow="Included free", headline="Miss the call. [[Not the job.]]", body="The caller gets a text from your business right away.", layout="type", cta="reviiewco.com/start"), """
You can't answer the phone with a torch in your hand. But that caller is about to dial the next contractor.

Missed-Call Text Back sends them a text from your business right away, so they hear from you first. It's included free with our reviews system and our websites.

Meanwhile, see who's showing up ahead of you on Google.""", "RANK", end="start", tags=1)
image("B27", "B", "Pricing", dict(eyebrow="One price", headline="$297/month. [[No contract. No setup fee.]]", body="Review requests, follow-ups, replies, Missed-Call Text Back. Unlimited users.", layout="type", cta="reviiewco.com/start"), """
Everything, done for you. One price.

• A text after every job, plus up to two reminders
• Your past-customer list worked for you
• A reply to every review, in your voice
• Missed-Call Text Back included
• Unlimited users, cancel anytime

Prefer yearly? $2,970, 12 months for the price of 10.""", "GOLD", end="start", tags=2)
image("B28", "B", "Five minutes", dict(eyebrow="Your entire job", headline="Five minutes from you. [[Everything else from us.]]", body="Add us to your Google profile. Send your list. Approve the texts.", layout="type", cta="reviiewco.com/start"), """
Here's your entire job:
1. Add us as a manager on your Google profile (about 5 minutes)
2. Send your customer list (about 2 minutes)
3. Approve the message templates (under a minute)

That's it. No app to learn. No dashboard to check. Works with Jobber, Housecall Pro, ServiceTitan, FieldEdge, or a simple list.""", "GOLD", end="start", tags=0)
image("B29", "B", "Ethics", dict(eyebrow="How we work", headline="We never write, buy [[or filter reviews.]]", body="Real reviews from real customers. Anyone who opted out is never contacted.", layout="type"), """
Fake reviews, bought reviews and filtering out unhappy customers can get your Google profile in real trouble.

We never write, buy or filter reviews. Every customer gets the same invitation. Anyone who opted out is never contacted. And you approve every message before it goes out.

Know exactly what's allowed in 2026. Free guide.""", "RULES", tags=1)
image("B30", "B", "First reviews", dict(eyebrow="How fast?", headline="The first ones usually [[land within days.]]", body="Your past customers already like you. They just needed a friendly text and a link.", layout="type", cta="reviiewco.com/start"), """
How fast do reviews start coming in? The first ones usually land within days. Your past customers already like your work; they just needed a friendly text and a one-tap link.

Our guarantee: at least 10 new Google reviews in 30 days when you send a list of 300+ past customers, or every dollar back.

Want to try it yourself first? Get the free playbook.""", "GOLD", end="start", tags=2)

# ---------------- Bundle: reviews + website at $497 (matches reviiewco.com/pricing) ----------------
image("H01", "A", "Bundle: reviews + website", dict(eyebrow="All of it, handled", headline="Reviews + website. [[Both for $497/month.]]", body="We build your site with no build fee, run your reviews, and Missed-Call Text Back is included.", layout="type", cta="reviiewco.com/book"), """
Your reviews and your website are the same fight from two directions: one gets them to trust you, the other gets them to call.

We'll handle both. We build your website with no build fee, run your review requests and replies, and Missed-Call Text Back comes free.

Not ready? See where you stand first.""", "RANK", offer="bundle", tags=0)
image("H02", "B", "Bundle: reviews + website", dict(eyebrow="Fully managed", headline="Your website and your reviews, [[one team.]]", body="Reviews + website bundle: $497/month. Missed-Call Text Back included.", layout="type", cta="reviiewco.com/book"), """
One team runs your website and your Google reviews, so they tell the same story.

• Website built for you, no build fee
• Review requests after every job, and a reply to every review
• Missed-Call Text Back, free

Curious what it would look like for your business?""", "SITE", offer="bundle", tags=1)

for it in items:
    it.setdefault("hold", False)

if __name__ == "__main__":
    specs = HERE / "specs"
    specs.mkdir(exist_ok=True)
    for it in items:
        if it["kind"] == "image":
            (specs / f"{it['id']}.json").write_text(json.dumps(it["spec"], ensure_ascii=False, indent=1))
    (HERE / "library.json").write_text(json.dumps(items, ensure_ascii=False, indent=1))
    heads = [it["spec"]["headline"] for it in items if it["kind"] == "image"]
    assert len(heads) == len(set(heads)), "duplicate headline"
    for it in items:
        w = len(it["caption"].split())
        bad = [x for x in ("blue-collar", "link in bio") if x in it["caption"].lower()]
        if bad or len(it["caption"]) > 2200:
            raise SystemExit(f"{it['id']}: {bad} len={len(it['caption'])}")
    print(len(items), "items;", sum(1 for i in items if i["slot"] == "A" and not i["hold"]), "A /",
          sum(1 for i in items if i["slot"] == "B" and not i["hold"]), "B live,", sum(i["hold"] for i in items), "held")
