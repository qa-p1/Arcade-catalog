# Arcade 1.0.0: steps for the owner's PC

The cloud session does everything it can: code, tests, CI, rc releases, and every exit gate against the published rc
files. The steps below need something the cloud session doesn't have: your logged-in `gh`, permission to create
repositories, or your real desktop. Each item says what it unblocks. Do them in order. Item 1 matters most.

## 1. Create the update-signing key (unblocks every stable release)

Why: `promote.yml` (rc → stable) and `nightly.yml` sign `manifest.json` with the `ARCADE_UPDATE_SIGNING_KEY` Actions
secret and refuse to publish without it. The cloud session can't set Actions secrets (blocker B1), so no app can be
promoted to stable until this is done. Everything up to a verified rc continues meanwhile.

On a machine where `gh auth status` shows you logged in as an owner of the `qa-p1` repos:

```bash
git clone https://github.com/qa-p1/Arcade-Link && cd Arcade-Link
```

```bash
cargo run -q -p arcade-link-cli --features release -- keygen --secret-to-gh qa-p1/Arcade-tools --secret-to-gh qa-p1/Arcade-box --secret-to-gh qa-p1/Arcade-clipboard --secret-to-gh qa-p1/Arcade-look --secret-to-gh qa-p1/Arcade-Find --secret-to-gh qa-p1/Arcade-lens --secret-to-gh qa-p1/Arcade-Shelf --secret-to-gh qa-p1/Arcade-wheel
```

It prints the public key first (an `untrusted comment:` line and an `RW…` line), then pipes the private key straight
into `gh secret set` for each repo. The private key is never written to disk. Then either:
- paste the printed public key into a comment on the open Tools PR (or into `PUBLIC_KEY.txt` in this folder), and
  the session commits it into Tools as the current key; or
- commit it yourself to `qa-p1/Arcade-tools` as described in Link `docs/SIGNING.md`.

Check: `gh secret list -R qa-p1/Arcade-tools` lists `ARCADE_UPDATE_SIGNING_KEY`.

## 2. Create the `Arcade-template` repository (blocker B2)

Why: the cloud session may not create repositories. The template lives and is tested in Link `template/` (CI job
"Template app"), so nothing is blocked. This step only makes it a one-click GitHub template.

```bash
gh repo create qa-p1/Arcade-template --public --description "Start a new Arcade app"
```

```bash
git clone https://github.com/qa-p1/Arcade-Link /tmp/arcade-link && cd /tmp/arcade-link/template && git init -b main && git add -A && git commit -m "Arcade app template (from Arcade-Link v1.0.0)" && git remote add origin https://github.com/qa-p1/Arcade-template && git push -u origin main
```

```bash
gh repo edit qa-p1/Arcade-template --template
```

## 3. Checks that need your real desktop

None yet. Anything the CI harness (headless Hyprland plus sway, KWin, Mutter and X11) can't reproduce is listed here
with the exact steps, the expected result and where to record it.

## 4. Your call: trade a little UX for memory with a WebKit window open (optional)

Nothing is blocked on this. With its window open, Tools measures about 261–334 MB PSS on CI's virtual display, against
the 225 the audit estimated (Tools `docs/v1/DECISIONS.md` D10 has the numbers). Every change that costs no UX is
already in. The rest is WebKit drawing the page. Two switches would cut it, and both change how the app feels, so
the agent won't turn them on by itself:

- **Compositing off** (`WEBKIT_DISABLE_COMPOSITING_MODE=1`): about −50 MB. The audit measured slower frames in Box's
  island on your GPU (p95 15–17 → 19–22 ms). Tools has little motion.
- **Paging out the open window:** about −80 MB, but a click can stall while memory comes back from swap.

If you want either for Tools, say so in the catalog README's owner decisions and it will be applied and measured.
Otherwise the window-open cap stays at what CI measures and only goes down.
