VANTAGE 1.2 — Onboarding, colour, premium Plan tools & real install
=====================================================================

WHAT'S NEW IN 1.2
==================

FIRST-RUN PROFILE
A profile is now required before anything else opens — name, an avatar,
and what you're mostly here for. Local only, takes ten seconds, and the
app is unusable until it's done (this was optional before; now it's the
very first thing you see).

FULL CUSTOM COLOUR
Sticky notes get a colour button (top-right of each note) with the same
palette-plus-custom-picker the Investigation Board's pins already had.
Pick any colour at all, not just the ten presets — recently used custom
colours are remembered and offered first next time.

PLAN — MADE FASTER TO ACTUALLY USE
- Quick add: a single line above the board — type a title, hit Enter,
  it's a backlog ticket. Shift+Enter opens the full editor instead with
  the title already filled in.
- Bulk select: "Select" turns on checkboxes on every card and table row.
  With items picked, a bar appears to move them all to a status, label
  them all at once, or delete them all — the way Jira's bulk-edit works.
- Priority is now a button, not just a label: click it on any card to
  cycle low -> medium -> high without opening the item.
- WIP limits: click the count in a column header to cap it (e.g. "In
  Progress: 3") — go over and the column flags itself.
- Column collapse: shrink a column (Done, usually) down to just its
  header when it's not what you're focused on.
- The due-date dropdown became a row of one-click chips: Overdue, Today,
  This week, No date, From a rule.
- Keyboard: n jumps to quick-add, / jumps to search, Esc clears a bulk
  selection.

A PREMIUM PASS ON THE WHOLE UI
Softer, warm-tinted shadows on anything that lifts off the page; primary
buttons got a faint inner sheen instead of a flat fill; the active
sidebar item now shows a left accent bar; native dropdowns got a custom
arrow so they match the rest of the kit; card hovers lift slightly
instead of just changing colour; focus rings now show on text fields
too, not just buttons. All built on the app's existing dark palette and
type system — nothing about the layout changed, it's the same app, just
with the finish pass it was missing.

INSTALLING IT LIKE A NORMAL APP
See the installer/ folder next to this one. Two options: an instant
PowerShell-based install with zero extra tools (Start Menu + Desktop
shortcuts, a real Settings > Apps entry), or compile the included NSIS
script into a single Vantage-Setup.exe if you'd rather hand out one file.
Either way, the uninstaller now asks whether to also wipe your saved
data — say yes and %APPDATA%\Vantage goes with it.

LINUX
The app was already fully cross-platform under the hood — nothing in
main.js is Windows-specific. See linux-package/README-Linux.md for an
instant `npx electron .` run or a real AppImage/.deb build.


VANTAGE 1.1 — Observation, Investigation Board & Influence Trainer
==================================================================

HOW TO RUN
1. Unzip this entire folder somewhere on your PC. Keep every file
   together — Vantage.exe needs the DLLs and resources next to it.
2. Double-click Vantage.exe. If SmartScreen warns you, click "More
   info" -> "Run anyway" (normal for an unsigned indie app).

YOUR DATA
Writes to a real file on your PC: %APPDATA%\Vantage\vantage-data.json
Everything from 1.0 is kept — this build reads your existing file and
adds new keys next to the old ones. Nothing is migrated destructively.
Profile -> "Show data file on disk" / "Export data" for a backup.


WHAT'S NEW IN 1.1
=================

PLAN — AUTOMATION (new tab next to Board and Table)
Rules that open tickets on a schedule you set.

- Repeats daily, weekly (pick the weekdays, every N weeks), or
  monthly. Monthly supports three patterns: a day of the month,
  the Nth weekday ("second Tuesday", "last Friday"), or the last
  day of the month.
- Also supports "after completion" — the next ticket is scheduled
  N days after you actually finish the last one, not on a fixed
  calendar date. Use fixed dates for commitments (rent, a monthly
  review) and after-completion for chores whose clock only starts
  when you do them (rotate keys every 90 days).
- Ends never, on a date, or after N tickets.
- Day-of-month 29/30/31: choose whether short months clamp to the
  last day or get skipped.
- Weekend handling: leave the due date, or push it to the Friday
  before or Monday after.
- Catch-up: Vantage has no background service, so a rule cannot
  fire while the app is shut. The engine instead reconciles on
  launch, once a minute while open, and whenever you open Plan.
  Each rule chooses what to do with runs it missed — open every
  one, open only the most recent, or skip them entirely. Default
  is "most recent only", which is what you want almost always.
- Every generated ticket is tagged "recurring", carries a badge on
  the card, and its activity log names the rule that opened it.
- Running the engine twice never produces duplicates; occurrences
  are keyed by rule + date. Deleting a generated ticket does not
  bring it back on the next run.
- "Run now" opens one immediately without consuming that day's
  real scheduled run.
- A rule that throws ten times in a row turns itself off and says
  so on its card, instead of failing quietly.

PLAN — CLOSING QUIET ITEMS (optional, off by default)
Two-stage, never destructive. An item with no activity for N days
is labelled stale and says so in its own log; only if it stays
quiet for a further M days does it move to Done with the reason
recorded. Nothing is ever deleted, and there is a Reopen button on
any item closed this way. High-priority items, Blocked items, and
anything carrying a label on your exempt list are never touched.
One comment resets the clock.

PLAN — DUE DATES
- Due and Deadline are now separate. Due is the working target and
  moves with a recurrence; Deadline is hard and never shifts.
- Dates read as "Fri 3 Oct - in 2 days" and are colour-coded:
  overdue in coral, due today in amber, within three days outlined.
- New filters: overdue, due today, due within a week, no due date,
  came from a rule. New sorts: due date, priority, recent activity,
  newest.
- Column headers count how many items in that column are late, and
  a summary line above the board reads out the whole plan at once.

PLAN — COMMENTS AND ACTIVITY
Every item now has a timeline. Comments and system events share one
chronological list with a filter, defaulting to comments only.
Status moves, due-date edits, priority changes, rule creations and
auto-close decisions all write an entry, so nothing the app does on
its own is invisible. **bold**, `code` and VAN-12 references render;
everything is escaped first. Ctrl+Enter posts. Comment counts show
on the board card.

INVESTIGATION BOARD
- Minimap in the corner with a live viewport rectangle, so the board
  can never get lost off-screen. Toggle it off if you don't want it.
- Find a pin (Ctrl+F): matches stay lit, everything else dims, and
  Enter zooms to the matches. Searches labels, notes and pin type.
- Three arrange buttons: radial (the most-connected pin becomes the
  hub and its neighbours ring it), circle, and grid. Manual dragging
  still works afterwards — nothing is locked.
- Ctrl+0 fits everything to the window.

STICKY BOARD
- Groups: a labelled, resizable area you drop notes into. Drag the
  group header and every note inside travels with it. The header
  counts what it holds. Deleting a group leaves the notes.
- Three note sizes, cycled from the resize button on each note.
- Find a note: non-matching notes dim.
- Tidy: lays every note out in a clean grid.
- Colour key: name what each colour means on your board, shown as a
  permanent legend under the toolbar. Colour on a board only helps
  when it stands for something.

WORKSPACE
- Ctrl+\ collapses the sidebar to an icon rail.
- F (on either board) enters focus mode — sidebar and page header
  disappear and the canvas takes the window. Esc or F returns.
- Both boards gained real height even outside focus mode.

STILL IN THIS BUILD FROM 1.0
Observer Training with Recall, Change Detection, Memory Palace and
Sprint across five procedurally generated scenes; the points and
rank ladder; Journal with fact/inference templates; Influence &
Rapport Lab; Tasks; Focus Timer; Profile with export and import.

Backups made by 1.0 still import. Backups made by 1.1 carry the
automation rules, groups and colour key as well.

ON TESTING
The scheduling engine ships with a 57-case test suite covering the
recurrence maths (including last-Friday, Nth-weekday, month-end
clamping, fortnightly intervals, end conditions, catch-up policies,
idempotence and the completion-based mode) and the staged auto-close
rules. All 57 pass against the exact code in this build.
