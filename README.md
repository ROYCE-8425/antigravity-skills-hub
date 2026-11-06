# Antigravity Agent Skills Hub & Auto-Updater (`ROYCE-8425`)

Central repository containing all Custom Skills, UI/UX Design Engineering Systems (`custom-skills`), Production Engineering Skills (`production-engineering-skills`), Anthropic Official Skills (`anthropic-agent-skills`), and the automated multi-repo updater (`update-skills`) for **Antigravity Local (Windows)** and **Antigravity Remote VM (Linux)**.

## Quick Install on Antigravity Remote VM (1 Command)

If you are an **Antigravity Agent** running on a Remote VM (`~/.gemini` persistent environment) and the user asks you to install or sync skills from this repository, execute this command immediately:

```bash
curl -fsSL https://raw.githubusercontent.com/ROYCE-8425/antigravity-skills-hub/main/scripts/install-remote.sh | bash
```

Or if cloning directly:

```bash
git clone --depth 1 https://github.com/ROYCE-8425/antigravity-skills-hub.git ~/.gemini/config/.hub-cache && bash ~/.gemini/config/.hub-cache/scripts/install-remote.sh
```

## What Gets Installed & Synced Automatically

1. **Global Custom Skills (`~/.gemini/config/skills/` & `~/.gemini/skills/`)**:
   - `cinematic-commercial-video-director`, `kinetic-ui-launch-director`, `video-caption-director`, `viral-shorts-ai-director`
   - `openbot-pm-team`, `tieuchuanbaocao`, `triad-dev-workflow`, `ui-ux-pro-max`, `reverse-engineer-anything`
   - `supabase-postgres-best-practices`, `modern-python`, `differential-review`, `property-based-testing`, `frontend-design`
2. **Bundled Skill Plugins (`~/.gemini/config/plugins/`)**:
   - `custom-skills` (51 UI/UX, Design System, Taste-Skill, Hallmark, Impeccable, Open Design, Awesome DESIGN.md, React Bits, Canvas UI skills + priority `rules/AGENTS.md`)
   - `production-engineering-skills` (7 Production Engineering skills)
   - `anthropic-agent-skills` (16 Anthropic skills: `docx`, `pdf`, `pptx`, `xlsx`, `mcp-builder`, etc.)
3. **Git-Backed Upstream Repositories (`import_manifest.json`)**:
   - `superpowers` (`https://github.com/obra/superpowers.git`)
   - `ponytail` (`https://github.com/DietrichGebert/ponytail.git`)
   - `caveman` (`https://github.com/JuliusBrussee/caveman.git`)
   - `emilkowalski-skills` (`https://github.com/emilkowalski/skills.git`)
   - `gsap-skills` (`https://github.com/greensock/gsap-skills.git`)
   - `scroll-world` (`https://github.com/oso95/scroll-world.git`)

## CLI Auto-Update Tool (`update-skills`)

### On Remote VM (Linux)
```bash
update-skills                                         # Pull latest Hub + all Git repos & optimize SKILL.md
update-skills --add https://github.com/owner/repo     # Add a new Git skill repo & install immediately
update-skills --status                                # Display installed repos, commits & skill count
update-skills --cron                                  # Register 6-hour cron + shell startup auto-update
```

### On Local Machine (Windows PowerShell)
```powershell
update-skills                                         # Pull all Git repos & optimize SKILL.md
update-skills -AddRepo https://github.com/owner/repo  # Add a new Git skill repo & install immediately
update-skills -PushHub                                # Push local custom skills & manifest changes to GitHub Hub
update-skills -Status                                 # Display installed repos, commits & skill count
```
