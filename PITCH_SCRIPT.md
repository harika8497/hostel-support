# quietline — 15-minute technical storytelling script

The rule for this format: every tech detail earns its place only if it serves the story. If a judge could nod along without knowing what MySQL is, you're doing it right.

---

## 1. The hook (1.5 min) — start with a person, not a problem statement

Don't open with "our project is an anonymous reporting system." Open with a scene:

> "It's 11 PM. A first-year student in your hostel has been mocked, mimicked, and pushed around by seniors every day since orientation. There's a complaint form at the warden's office. She's looked at it three times this week. She's never picked up the pen — because the moment she writes her name, room number, and branch on that form, everyone in her block will know who complained by breakfast. So she says nothing. And nothing changes."

Pause. Then: "That's not a hypothetical. That's the actual reason ragging and bullying complaint numbers are so much lower than the actual rate of it happening. The problem was never that students don't want help. It's that the *first step* to asking for it costs too much."

## 2. The reframe (1.5 min)

State the real problem in one sentence: **"Existing complaint systems ask for identity before they offer safety. We flipped that order."**

This is the line that should stick. Everything else in the talk supports it.

## 3. Walk through the product as a story, not a feature list (5 min)

Narrate it as "watch what happens when she uses this instead":

- She opens quietline. No sign-up screen. Two choices: *just venting* or *I want this resolved.* Say clearly: this isn't a gimmick, it's the actual design answer to "how do you help someone anonymously" — she decides how much of herself to give, not a form.
- She writes what happened. Submits. Gets a passcode — like a locker key, not a login.
- Somewhere else, a warden opens a dashboard and sees her message. If it sounded urgent, it's already flagged near the top — not because a machine "understood" her pain, be explicit about this, but because certain phrases are a signal worth a human looking sooner rather than later.
- The warden replies. She comes back later, types her passcode, and there's a message waiting. A real back-and-forth, still with nothing tying it to her name — unless she's the one who decided to share it.

Show the actual screens live here (or a short recording) — this is where the demo carries the story, keep narration light while it's on screen.

## 4. The honest part — this is your differentiator (2.5 min)

Every team building "anonymous reporting" claims perfect anonymity and perfect detection. Say plainly that you're not claiming either:

> "We are not saying this is untraceable magic. We're not saying our system detects a crisis reliably. What we're saying is: this is a lower-pressure on-ramp into help that already exists — counselors, the anti-ragging committee — not a replacement for them. If something is serious, it still goes to a real person on a real committee. We built the on-ramp. We didn't reinvent the destination."

This is the tradeoff moment: full anonymity vs. real intervention. Name it out loud — "the more anonymous we make it, the less a warden can actually act on it, and we chose to let the *student* decide where on that line they sit, conversation by conversation." Judges remember teams that name the hard tradeoff over teams that pretend there isn't one.

## 5. What's actually built vs. what's vision (1.5 min)

Be upfront and confident, not apologetic:

> "For this competition, we built the working core: the report form, the passcode system, and a staff dashboard with flagging. That's the engine. The vision — SMS-based check-ins, integration with the actual anti-ragging committee's workflow, multi-language support — that's the roadmap, and we know exactly what it takes to get there because the core is already working."

## 6. Close — return to the person from the opening (1 min)

> "Go back to that student at 11 PM. The form on the warden's desk didn't change. But now there's a second option that doesn't cost her name to use. That's the whole idea. We're not trying to fix bullying with software. We're trying to remove the one barrier that keeps people from asking for help in the first place — the fear of being known."

Leave the room with the sentence, not a summary slide.

---

## Delivery notes

- **Don't say "MySQL," "Flask," or "backend" more than once each, if at all.** If asked in Q&A, answer plainly then: "we store it in a standard database, nothing exotic" is enough unless a judge specifically wants architecture depth.
- **Say numbers, not just feelings, if you have any** — e.g., cite that ragging/bullying underreporting is a known, cited problem in student welfare literature, if you can source a real stat before the talk. A story lands harder with one real number in it.
- **Practice the pause after the opening scene.** Silence after "and nothing changes" is doing more work than any slide.
- **Have the live demo ready to fail gracefully** — a 20-second screen recording as backup if the server hiccups mid-talk.
