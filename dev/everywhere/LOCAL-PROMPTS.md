# Prompts for a local session on the owner's computer

Short, self-contained prompts for the few things the cloud sessions can't do. Paste one into Claude Code (Sonnet is
fine) on your own computer, in any folder. Each one says what to do, what not to do, and what to report back.

**When:** the cloud session hands over A and B together when it reaches stage 5 (the browser extension), and the
local session takes over for that stretch. A includes the old wip branch deletion and the Lens 0.4.1/0.4.2 note.
C and D come at stage 8, once everything is released.

---

## Prompt A: GitHub chores (with Prompt B, at stage 5)

```text
You are helping with the Arcade apps (GitHub owner: qa-p1). Use the gh CLI (run `gh auth status` first; if it isn't
logged in, stop and tell me to run `gh auth login`). Do exactly these steps, show me each command before running
anything that deletes or creates, and stop if a step fails.

1. Delete these 12 remote branches. Every name starts with `claude/sharp-cori-29w5eg-`. For each, first confirm the
   branch exists and has no commits that are missing from that repo's main (`gh api repos/qa-p1/<repo>/compare/main...<branch>`
   must show "ahead_by": 0, or its commits must already be in main by content). If one isn't merged, skip it and tell
   me. Then delete it with `gh api -X DELETE repos/qa-p1/<repo>/git/refs/heads/<branch>`.
   - Arcade-Link: wip-link-unpacked
   - Arcade-clipboard: wip-gates, wip-step5-security
   - Arcade-Find: wip-security
   - Arcade-lens: wip-security
   - Arcade-look: wip-restart, wip-security, wip-security-2
   - Arcade-Shelf: wip-step5, wip-tier2
   - Arcade-wheel: wip-step5, wip-tier2
   Do NOT delete any other branch, especially not anything in Arcade-box and not `claude/sharp-cori-29w5eg` itself.

2. In qa-p1/Arcade-lens, add this paragraph at the very top of the release notes of releases v0.4.1 and v0.4.2
   (keep the existing notes below it; use `gh release view` then `gh release edit --notes-file`):

   > **Update to [Arcade Lens 1.0.0](https://github.com/qa-p1/Arcade-lens/releases/tag/v1.0.0) or later.** On Linux this release can crash on start with a font error (found on 2026-11-21); 1.0.0 fixes it. Arcade Tools offers the update.

3. Create an empty repository qa-p1/Arcade-browser with the same visibility as qa-p1/Arcade-Link, description
   "Arcade for the browser: every Arcade app's abilities in Chrome, Edge, Brave, Firefox and Zen.", no template, no
   files. Enable Dependabot alerts like the other Arcade repos.

4. Mozilla signing key (for the Firefox/Zen extension). I will do the website part myself:
   - Tell me to open https://addons.mozilla.org/developers/addon/api/key/ , log in or create the free account,
     and generate credentials.
   - Then run `gh secret set AMO_JWT_ISSUER --repo qa-p1/Arcade-browser` and
     `gh secret set AMO_JWT_SECRET --repo qa-p1/Arcade-browser` so I paste the values into the terminal prompt.
     Never ask me to paste the values into this chat, and never print them.

At the end, report: which branches were deleted or skipped (and why), the two release URLs you edited, the new repo's
URL, and whether both secrets are set (`gh secret list --repo qa-p1/Arcade-browser`, names only).
```

---

## Prompt B: where Zen looks for the native messaging file (with Prompt A, at stage 5)

```text
I use the Zen browser (Firefox-based). I need to know exactly which folder (or registry key on Windows) Zen reads
native messaging host manifests from, because a helper program must register there. Find it by testing, not by
guessing. Work in a new temporary folder and clean up everything you create at the end.

1. Tell me my OS, how Zen is installed (tarball, AppImage, Flatpak, Snap, .deb/.rpm, Homebrew, installer) and its
   version (from about:support or its application.ini). If it's Flatpak or Snap, say so clearly: sandboxed browsers
   handle native messaging differently, and that matters.
2. Write a tiny native messaging host: a script that, when started, appends one line with the absolute path of the
   manifest it was registered through (pass it as an argument in each manifest) to a log file, then answers
   {"ok":true} using the native messaging framing (4-byte length + JSON) and exits.
3. Write host manifests named `arcade_probe` (type "stdio", allowed_extensions ["probe@arcade.dev"]), one per candidate
   location, each pointing to the script with a different argument:
   - Linux: ~/.mozilla/native-messaging-hosts/, ~/.zen/native-messaging-hosts/, ~/.config/zen/native-messaging-hosts/,
     /usr/lib/mozilla/native-messaging-hosts/ (only if I agree to use sudo), and any folder you find by searching
     Zen's install for the text "native-messaging-hosts" (e.g. inside omni.ja or libxul).
   - macOS: ~/Library/Application Support/Mozilla/NativeMessagingHosts/, ~/Library/Application Support/Zen/NativeMessagingHosts/,
     ~/Library/Application Support/zen/NativeMessagingHosts/.
   - Windows: registry keys HKCU\Software\Mozilla\NativeMessagingHosts\arcade_probe and
     HKCU\Software\Zen\NativeMessagingHosts\arcade_probe (default value = manifest path), plus any vendor name you
     find in Zen's application.ini.
4. Write a minimal temporary WebExtension (manifest_version 2 is fine for this test, id "probe@arcade.dev",
   permission "nativeMessaging") whose background script calls browser.runtime.sendNativeMessage("arcade_probe", {})
   once and logs the result. Tell me to load it in Zen via about:debugging → This Zen/Firefox → Load Temporary
   Add-on, and to open the extension's Inspect console.
5. Read the log file: which manifest path(s) did Zen use? If none worked, show me the console error.
6. Remove everything you created (manifests, registry keys, script, log, extension folder).

Report: OS, Zen version and install type, the exact working location(s), and anything surprising. Keep it short.
```

---

## Prompt C: Windows real-user check (stage 8, when the cloud session says the releases are ready)

```text
On this Windows PC, check the released Arcade apps the way a normal user would, and write down everything that is
wrong or confusing. Do not change any code. Work only in your own test folder and the normal user locations the apps
use. Ask me before anything needs admin rights.

1. Download the latest Arcade Tools setup.exe from https://github.com/qa-p1/Arcade-tools/releases/latest , check
   its SHA-256 against the release's SHA256SUMS, install it. Through Tools, install every Arcade app.
2. In Tools' "Everywhere" page, follow the browser steps for Chrome (unpacked zip from
   https://github.com/qa-p1/Arcade-browser/releases/latest ) and confirm it says Connected.
3. In File Explorer, right-click (and "Show more options") on: a PNG, a JPG, a PDF, an MP4, an MP3, a DOCX, a CSV, a
   folder, and 3 images selected together. For each, try the "Arcade" menu, "Send to → Arcade", and two pinned
   actions. Check the output files appear where Tools' settings say, and the small progress window behaves
   (minimize, finish notification, Open, Show in folder).
4. Press Space on a file in Explorer (Look's Explorer integration) and Ctrl+Alt+Shift+Space.
5. In Chrome: right-click an image, a link, selected text (also "12 USD" and "5 miles"), and a page; use the image
   hover button; on a YouTube video use the Download button for an MP4 at 720p and for MP3 audio only; use the
   toolbar popup to run 3 tools with no input; send a link to a phone if one is paired in Arcade Clipboard.
6. Uninstall everything from Tools ("Uninstall everything") and check no Arcade entries remain in Explorer's menus,
   Send to, the registry (HKCU\Software\Classes\SystemFileAssociations\*\shell\Arcade*) or Chrome's
   NativeMessagingHosts key.

Write the results to a file `REAL-USER-WINDOWS.md` (what worked, what broke with exact steps and screenshots paths,
what was confusing), then commit it on a new branch `local/real-user-windows` in a clone of qa-p1/Arcade-catalog under
dev/everywhere/ and open a pull request to main titled "Windows real-user check". No extra footers in the commit or PR.
```

---

## Prompt D: macOS real-user check (stage 8)

```text
Same as the Windows check, on this Mac:
1. Install Arcade Tools from the latest .dmg at https://github.com/qa-p1/Arcade-tools/releases/latest (check its
   SHA-256 against SHA256SUMS; it is not notarized yet, so tell me how to allow it in System Settings → Privacy &
   Security), then every Arcade app through Tools.
2. Set up the browser extension in Chrome (unpacked) and in Zen or Firefox (the signed .xpi) from
   https://github.com/qa-p1/Arcade-browser/releases/latest ; confirm Tools' "Everywhere" page says Connected for both.
3. In Finder, right-click → Quick Actions / Services on a PNG, a PDF, an MP4, an MP3, a folder and 3 images; run the
   Arcade entries and check outputs and the progress window. Try Look's Finder shortcut (Control+Option+Shift+Space).
4. In both browsers: right-click an image, a link, selected text ("12 USD", "5 miles"), a page; the image hover
   button; YouTube Download (720p MP4 and MP3); the toolbar popup with 3 no-input tools.
5. "Uninstall everything" in Tools; check nothing Arcade is left in Services, ~/Library/Services, ~/Library/Application
   Support/*/NativeMessagingHosts or login items.

Write `REAL-USER-MACOS.md` the same way, commit it on branch `local/real-user-macos` in a clone of
qa-p1/Arcade-catalog under dev/everywhere/, open a PR to main titled "macOS real-user check". No extra footers.
```
