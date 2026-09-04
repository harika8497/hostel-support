# quietline — anonymous hostel support, working prototype

## 1. What's in this folder

```
hostel-support/
├── app.py              ← the whole backend (Flask). All logic lives here.
├── schema.sql           ← run this once to create your MySQL tables
├── requirements.txt      ← Python packages to install
├── templates/            ← the actual pages (HTML)
└── static/style.css      ← the dark theme
```

## 2. VS Code extensions you need

You said you already have the MySQL extension — good. Also install:
- **Python** (Microsoft) — gives you run/debug support for `app.py`
- **Pylance** — comes bundled with the Python extension, just autocomplete/type-checking, no setup needed

That's it. No Java, no Android, no Firebase extensions needed for this one.

## 3. One-time setup

Open a terminal in VS Code (`` Ctrl+` ``) and run:

```bash
# 1. create a virtual environment (keeps this project's packages separate from the rest of your machine)
python -m venv venv

# 2. activate it
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. install the packages
pip install -r requirements.txt
```

Then create the database. Using the MySQL extension in VS Code (or MySQL Workbench, or terminal):

```bash
mysql -u root -p < schema.sql
```

Open `app.py` and edit the `DB_CONFIG` block near the top — put in your actual MySQL password.

## 4. Running it

```bash
python app.py
```

Open **http://127.0.0.1:5000** in your browser. That's the student-facing form.

Staff side: **http://127.0.0.1:5000/staff/login** — demo password is `warden123`.

## 5. What each technology is actually doing (so you can explain it to your team without jargon)

**Flask (Python)** — this is the "waiter" of the app. When someone clicks submit, Flask takes that request, decides what to do with it (save it, generate a passcode, check a password), and hands back the right page. Nothing fancier than that — it's just the traffic controller between the browser and the database.

**MySQL** — this is the filing cabinet. Every report and every reply gets stored as a row in a table. We only have two tables: `reports` (the original messages) and `replies` (the back-and-forth conversation), linked by an ID number. When you explain this to non-tech judges, just say: "we keep a locked filing cabinet of conversations, and the only key is the passcode."

**Passcode system** — instead of a username/password, we hand the student a random 8-character code (like `A1B2C3D4`) at the moment they submit. No account, no email, nothing that identifies them. They just need to remember that code to come back and check for a reply.

**Keyword flagging** — a very simple check: does the message contain certain distress-related phrases? If yes, it gets marked with a red dot on the staff dashboard so it's seen sooner. Say this clearly in your pitch: *it's a triage signal, not a diagnosis.* We are not claiming the system understands emotional state — we're saying it helps a human get to the right message faster.

**Two-tier mode (vent vs. resolve)** — this is the actual design decision that answers "how does the warden know who it is if it's anonymous." Short version: *it doesn't, unless the student chooses to let it.* "Just venting" stays fully anonymous forever. "I want this resolved" asks for branch/year/hostel block (not necessarily a name) so a human can actually act. This is the tradeoff every anonymous system has to make, and naming it out loud in your talk is what makes the pitch feel honest instead of oversold.

## 6. Known limitations to say out loud in Q&A (this makes you look stronger, not weaker)

- The passcode system means if a student loses their code, there is no recovery — that's the tradeoff for not storing identity.
- Keyword flagging will miss things phrased differently and will sometimes false-flag — it's a first filter, not a judgment.
- This prototype does not encrypt data at rest in MySQL — for a real deployment you'd add encryption and a proper login system for staff (not a hardcoded password).
- IP addresses aren't logged in this app code, but the network/server layer could still technically see them — so "fully untraceable" is not a claim we make.
