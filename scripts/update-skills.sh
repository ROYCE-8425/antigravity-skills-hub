#!/usr/bin/env bash
# ==============================================================================
# Antigravity Skills & Plugins Auto-Updater + Repo Sync Tool (Linux / Remote VM)
# ==============================================================================
# Usage:
#   update-skills                                   # Sync Hub + all Git repos & optimize SKILL.md
#   update-skills --add https://github.com/u/r [id] # Add new Git skill repo to manifest & install
#   update-skills --status                          # Show repo status & skill counts
#   update-skills --cron                            # Register auto-update in crontab & ~/.bashrc
# ==============================================================================

set -uo pipefail
export GIT_TERMINAL_PROMPT=0

GLOBAL_CONFIG_DIR="${HOME}/.gemini/config"
HUB_CACHE_DIR="${GLOBAL_CONFIG_DIR}/.hub-cache"
PLUGINS_DIR="${GLOBAL_CONFIG_DIR}/plugins"
SKILLS_DIR="${GLOBAL_CONFIG_DIR}/skills"
SCRIPTS_DIR="${GLOBAL_CONFIG_DIR}/scripts"
LOGS_DIR="${GLOBAL_CONFIG_DIR}/logs"
LOG_FILE="${LOGS_DIR}/skill-updates.log"
MANIFEST_FILE="${GLOBAL_CONFIG_DIR}/import_manifest.json"
CONFIG_JSON="${GLOBAL_CONFIG_DIR}/config.json"
STATE_FILE="${GLOBAL_CONFIG_DIR}/last_skills_update.json"
DEFAULT_HUB_REPO="https://github.com/ROYCE-8425/antigravity-skills-hub.git"

mkdir -p "${PLUGINS_DIR}" "${SKILLS_DIR}" "${SCRIPTS_DIR}" "${LOGS_DIR}" "${HOME}/.local/bin"

QUIET=0
ACTION="sync"
ADD_URL=""
ADD_NAME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --quiet|-q)
      QUIET=1
      shift
      ;;
    --status|-s)
      ACTION="status"
      shift
      ;;
    --cron|-c)
      ACTION="cron"
      shift
      ;;
    --add|-a)
      ACTION="add"
      ADD_URL="${2:-}"
      ADD_NAME="${3:-}"
      shift 2 || shift
      [[ -n "${ADD_NAME}" && ! "${ADD_NAME}" =~ ^- ]] && shift || true
      ;;
    *)
      shift
      ;;
  esac
done

log_msg() {
  local level="$1"
  local msg="$2"
  local ts
  ts="$(date '+%Y-%m-%d %H:%M:%S')"
  echo "[${ts}] [${level}] ${msg}" >> "${LOG_FILE}"
  if [[ "${QUIET}" -eq 0 ]]; then
    case "${level}" in
      SUCCESS) printf "\033[0;32m[SUCCESS]\033[0m %s\n" "${msg}" ;;
      WARN)    printf "\033[0;33m[WARN]\033[0m    %s\n" "${msg}" ;;
      ERROR)   printf "\033[0;31m[ERROR]\033[0m   %s\n" "${msg}" ;;
      *)       printf "\033[0;36m[INFO]\033[0m    %s\n" "${msg}" ;;
    esac
  fi
}

if [[ "${ACTION}" == "status" ]]; then
  if [[ -f "${STATE_FILE}" ]]; then
    python3 - "${STATE_FILE}" <<'PYEOF'
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as f:
    st = json.load(f)
print("=== ANTIGRAVITY SKILLS STATUS (REMOTE VM) ===")
print(f"Last Updated : {st.get('last_updated')}")
print(f"Total Skills : {st.get('valid_skills')} / {st.get('total_skills')} valid")
print(f"Health       : {st.get('status')}")
print("\nGit Plugin Repositories:")
print(f"{'NAME':<24} {'BRANCH':<10} {'COMMIT':<10} {'REMOTE'}")
print("-" * 80)
for p in st.get("git_plugins", []):
    print(f"{p.get('name',''):<24} {p.get('branch',''):<10} {p.get('commit',''):<10} {p.get('remote','')}")
PYEOF
  else
    echo "No status file found yet. Run: update-skills"
  fi
  exit 0
fi

if [[ "${ACTION}" == "cron" ]]; then
  SCRIPT_REAL="${SCRIPTS_DIR}/update-skills.sh"
  chmod +x "${SCRIPT_REAL}"
  ln -sf "${SCRIPT_REAL}" "${HOME}/.local/bin/update-skills"
  if [[ -w "/usr/local/bin" ]]; then
    ln -sf "${SCRIPT_REAL}" "/usr/local/bin/update-skills" 2>/dev/null || true
  fi
  if command -v crontab >/dev/null 2>&1; then
    (crontab -l 2>/dev/null | grep -v "update-skills.sh" || true; echo "0 */6 * * * bash \"${SCRIPT_REAL}\" --quiet >/dev/null 2>&1") | crontab - 2>/dev/null || true
    log_msg "SUCCESS" "Registered crontab job (every 6 hours) for update-skills.sh"
  fi
  for rc in "${HOME}/.bashrc" "${HOME}/.profile"; do
    if [[ -f "${rc}" ]] && ! grep -q "antigravity-skills-auto-sync" "${rc}"; then
      cat >> "${rc}" <<'RCEOF'

# >>> antigravity-skills-auto-sync >>>
export PATH="$HOME/.local/bin:$PATH"
if [ -x "$HOME/.gemini/config/scripts/update-skills.sh" ]; then
  _LAST_UPD="$HOME/.gemini/config/last_skills_update.json"
  if [ ! -f "$_LAST_UPD" ] || [ -n "$(find "$_LAST_UPD" -mmin +720 2>/dev/null)" ]; then
    (nohup bash "$HOME/.gemini/config/scripts/update-skills.sh" --quiet >/dev/null 2>&1 &)
  fi
fi
# <<< antigravity-skills-auto-sync <<<
RCEOF
    fi
  done
  log_msg "SUCCESS" "Installed 'update-skills' CLI command and background auto-sync hook!"
  exit 0
fi

if [[ "${ACTION}" == "add" ]]; then
  if [[ -z "${ADD_URL}" ]]; then
    log_msg "ERROR" "Usage: update-skills --add <github_repo_url> [plugin_name]"
    exit 1
  fi
  python3 - "${MANIFEST_FILE}" "${ADD_URL}" "${ADD_NAME}" "${DEFAULT_HUB_REPO}" <<'PYEOF'
import json, os, sys
manifest_path, url, name, default_hub = sys.argv[1], sys.argv[2].strip(), sys.argv[3].strip(), sys.argv[4]
if not url.endswith(".git"):
    url += ".git"
if not name:
    name = os.path.splitext(os.path.basename(url))[0].lower()
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"hubRepo": default_hub, "imports": []}
if not any(item.get("name") == name for item in data.get("imports", [])):
    data.setdefault("imports", []).append({
        "name": name,
        "source": url,
        "branch": "main",
        "components": ["skills"],
        "pluginJson": {
            "name": name,
            "displayName": name,
            "version": "1.0.0",
            "description": f"Auto-synced skill plugin from {url}"
        }
    })
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Added {name} ({url}) to import_manifest.json")
else:
    print(f"{name} already exists in import_manifest.json")
PYEOF
fi

log_msg "INFO" "========== STARTING ANTIGRAVITY AGENT SKILLS SYNC =========="

# 1. Sync custom skills & manifest from Master Hub Repo (if configured)
HUB_REPO="$(python3 -c 'import json,sys,os; p=sys.argv[1]; print(json.load(open(p)).get("hubRepo","") if os.path.exists(p) else sys.argv[2])' "${MANIFEST_FILE}" "${DEFAULT_HUB_REPO}" 2>/dev/null || echo "${DEFAULT_HUB_REPO}")"

if [[ -n "${HUB_REPO}" ]]; then
  log_msg "INFO" "Syncing Custom Skills & Manifest from Hub: ${HUB_REPO}..."
  if [[ ! -d "${HUB_CACHE_DIR}/.git" ]]; then
    rm -rf "${HUB_CACHE_DIR}"
    git clone --depth 1 "${HUB_REPO}" "${HUB_CACHE_DIR}" >/dev/null 2>&1 || true
  else
    git -C "${HUB_CACHE_DIR}" fetch origin main >/dev/null 2>&1 || true
    git -C "${HUB_CACHE_DIR}" reset --hard origin/main >/dev/null 2>&1 || true
  fi

  if [[ -d "${HUB_CACHE_DIR}/.git" ]]; then
    if [[ -f "${HUB_CACHE_DIR}/import_manifest.json" && "${ACTION}" != "add" ]]; then
      cp -f "${HUB_CACHE_DIR}/import_manifest.json" "${MANIFEST_FILE}"
    fi
    if [[ -d "${HUB_CACHE_DIR}/skills" ]]; then
      cp -rf "${HUB_CACHE_DIR}/skills/"* "${SKILLS_DIR}/" 2>/dev/null || true
    fi
    if [[ -d "${HUB_CACHE_DIR}/plugins" ]]; then
      for pdir in "${HUB_CACHE_DIR}/plugins/"*; do
        [[ -d "${pdir}" ]] || continue
        pname="$(basename "${pdir}")"
        mkdir -p "${PLUGINS_DIR}/${pname}"
        cp -rf "${pdir}/"* "${PLUGINS_DIR}/${pname}/" 2>/dev/null || true
      done
    fi
    if [[ -f "${HUB_CACHE_DIR}/scripts/update-skills.sh" ]]; then
      cp -f "${HUB_CACHE_DIR}/scripts/update-skills.sh" "${SCRIPTS_DIR}/update-skills.sh"
      chmod +x "${SCRIPTS_DIR}/update-skills.sh"
      ln -sf "${SCRIPTS_DIR}/update-skills.sh" "${HOME}/.local/bin/update-skills"
    fi
    log_msg "SUCCESS" "Synced custom skills, plugins, and manifest from Hub!"
  fi
fi

# 2. Clone or update all Git-backed plugins from import_manifest.json
python3 - "${MANIFEST_FILE}" "${PLUGINS_DIR}" <<'PYEOF'
import json, os, subprocess, sys

manifest_path, plugins_dir = sys.argv[1], sys.argv[2]
if not os.path.exists(manifest_path):
    sys.exit(0)

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

for item in manifest.get("imports", []):
    name = item["name"]
    source = item["source"]
    target = os.path.join(plugins_dir, name)
    git_dir = os.path.join(target, ".git")
    if not os.path.isdir(git_dir):
        print(f"[CLONE] Cloning {name} from {source}...")
        if os.path.exists(target):
            subprocess.run(["rm", "-rf", target], check=False)
        subprocess.run(["git", "clone", "--depth", "1", source, target], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
PYEOF

# 3. Update all Git repositories in ~/.gemini/config/plugins/ and restore plugin.json + hooks.json
for pdir in "${PLUGINS_DIR}"/*; do
  [[ -d "${pdir}/.git" ]] || continue
  pname="$(basename "${pdir}")"
  branch="$(git -C "${pdir}" rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")"
  [[ -z "${branch}" || "${branch}" == "HEAD" ]] && branch="main"

  git -C "${pdir}" fetch origin "${branch}" >/dev/null 2>&1 || true
  local_sha="$(git -C "${pdir}" rev-parse HEAD 2>/dev/null || echo "")"
  remote_sha="$(git -C "${pdir}" rev-parse "origin/${branch}" 2>/dev/null || echo "")"

  if [[ -n "${local_sha}" && -n "${remote_sha}" && "${local_sha}" != "${remote_sha}" ]]; then
    git -C "${pdir}" reset --hard "origin/${branch}" >/dev/null 2>&1 || true
    new_sha="$(git -C "${pdir}" rev-parse --short HEAD 2>/dev/null || echo "")"
    log_msg "SUCCESS" "Updated ${pname} to latest commit (${new_sha})"
  else
    git -C "${pdir}" reset --hard HEAD >/dev/null 2>&1 || true
    short_sha="${local_sha:0:7}"
    log_msg "INFO" "${pname} is up to date (${branch} @ ${short_sha})"
  fi

  if [[ -f "${pdir}/hooks/hooks.json" && ! -f "${pdir}/hooks.json" ]]; then
    cp -f "${pdir}/hooks/hooks.json" "${pdir}/hooks.json"
  fi
done

# 4. Restore plugin.json manifests, optimize SKILL.md frontmatters, enable plugins in config.json, and write state
python3 - "${GLOBAL_CONFIG_DIR}" <<'PYEOF'
import datetime, glob, json, os, re, subprocess, sys

config_dir = sys.argv[1]
plugins_dir = os.path.join(config_dir, "plugins")
skills_dir = os.path.join(config_dir, "skills")
manifest_path = os.path.join(config_dir, "import_manifest.json")
config_json_path = os.path.join(config_dir, "config.json")
state_path = os.path.join(config_dir, "last_skills_update.json")

manifest = {}
if os.path.exists(manifest_path):
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

manifest_map = {item["name"]: item for item in manifest.get("imports", []) if "name" in item}

# Restore plugin.json for all plugins
if os.path.isdir(plugins_dir):
    for pname in sorted(os.listdir(plugins_dir)):
        pdir = os.path.join(plugins_dir, pname)
        if not os.path.isdir(pdir):
            continue
        pj_path = os.path.join(pdir, "plugin.json")
        if pname in manifest_map and "pluginJson" in manifest_map[pname]:
            with open(pj_path, "w", encoding="utf-8") as f:
                json.dump(manifest_map[pname]["pluginJson"], f, indent=2, ensure_ascii=False)
        elif not os.path.exists(pj_path):
            with open(pj_path, "w", encoding="utf-8") as f:
                json.dump({"name": pname, "displayName": pname, "version": "1.0.0"}, f, indent=2)

# Ensure all plugins are enabled in ~/.gemini/config/config.json
cfg = {}
if os.path.exists(config_json_path):
    try:
        with open(config_json_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except Exception:
        cfg = {}

plugins_cfg = cfg.setdefault("plugins", {})
if os.path.isdir(plugins_dir):
    for pname in sorted(os.listdir(plugins_dir)):
        pdir = os.path.join(plugins_dir, pname)
        if os.path.isdir(pdir) and os.path.exists(os.path.join(pdir, "plugin.json")):
            entry = plugins_cfg.setdefault(pname, {})
            entry["enabled"] = True

with open(config_json_path, "w", encoding="utf-8") as f:
    json.dump(cfg, f, indent=2, ensure_ascii=False)

# Validate & optimize all SKILL.md files (UTF-8 no BOM, description <= 160 chars)
total_skills = 0
valid_skills = 0
skill_files = []
for root_dir in [plugins_dir, skills_dir]:
    if os.path.isdir(root_dir):
        for r, _, files in os.walk(root_dir):
            if "SKILL.md" in files:
                skill_files.append(os.path.join(r, "SKILL.md"))

fm_re = re.compile(r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$", re.DOTALL)
name_re = re.compile(r"^name:\s*(.+)$", re.MULTILINE)
desc_block_re = re.compile(r"^description:\s*[>|][-+]?\s*\r?\n((?:[ \t]+[^\r\n]+\r?\n?)+)", re.MULTILINE)
desc_line_re = re.compile(r"^description:\s*(.+)$", re.MULTILINE)

for sf in skill_files:
    total_skills += 1
    try:
        with open(sf, "r", encoding="utf-8-sig") as f:
            content = f.read()
    except Exception:
        continue
    m = fm_re.match(content)
    if not m:
        continue
    fm, body = m.group(1), m.group(2)
    nm = name_re.search(fm)
    if not nm or "description:" not in fm:
        continue
    valid_skills += 1
    skill_name = nm.group(1).strip().strip("\"'")
    desc = ""
    db = desc_block_re.search(fm)
    if db:
        desc = re.sub(r"\r?\n\s*", " ", db.group(1)).strip().strip("\"'")
    else:
        dl = desc_line_re.search(fm)
        if dl:
            desc = dl.group(1).strip().strip("\"'")
    if len(fm) > 240 or len(desc) > 160:
        if len(desc) > 160:
            cut = desc[:155]
            last_dot = cut.rfind(". ")
            if last_dot > 70:
                desc = cut[:last_dot + 1]
            else:
                last_space = cut.rfind(" ")
                desc = (cut[:last_space] if last_space > 70 else cut) + "..."
        desc_safe = desc.replace('"', "'").replace("\n", " ").replace("\r", " ")
        new_content = f'---\nname: {skill_name}\ndescription: "{desc_safe}"\n---\n\n{body}'
        with open(sf, "w", encoding="utf-8") as f:
            f.write(new_content)

# Also symlink all skills into ~/.gemini/skills/ and ~/.gemini/antigravity/skills/ so Remote VM native skill tools see every skill
for target_root in ["~/.gemini/skills", "~/.gemini/antigravity/skills"]:
    alt_skills_dir = os.path.expanduser(target_root)
    os.makedirs(alt_skills_dir, exist_ok=True)
    for sf in skill_files:
        sdir = os.path.dirname(sf)
        sname = os.path.basename(sdir)
        if sname in ("skills", ""):
            sname = os.path.basename(os.path.dirname(sdir))
        dst = os.path.join(alt_skills_dir, sname)
        if not os.path.exists(dst) and not os.path.islink(dst):
            try:
                os.symlink(sdir, dst)
            except Exception:
                pass

# Copy global UI/UX rules to ~/.gemini/AGENTS.md if not present
rules_src = os.path.join(plugins_dir, "custom-skills", "rules", "AGENTS.md")
rules_dst = os.path.expanduser("~/.gemini/AGENTS.md")
if os.path.exists(rules_src) and not os.path.exists(rules_dst):
    try:
        import shutil
        shutil.copyfile(rules_src, rules_dst)
    except Exception:
        pass

# Collect git plugin statuses
git_plugins = []
if os.path.isdir(plugins_dir):
    for pname in sorted(os.listdir(plugins_dir)):
        pdir = os.path.join(plugins_dir, pname)
        if os.path.isdir(os.path.join(pdir, ".git")):
            branch = subprocess.run(["git", "-C", pdir, "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip() or "main"
            commit = subprocess.run(["git", "-C", pdir, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
            remote = subprocess.run(["git", "-C", pdir, "config", "--get", "remote.origin.url"], capture_output=True, text=True).stdout.strip()
            git_plugins.append({"name": pname, "branch": branch, "commit": commit, "remote": remote})

state = {
    "last_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total_skills": total_skills,
    "valid_skills": valid_skills,
    "git_plugins": git_plugins,
    "status": "healthy"
}
with open(state_path, "w", encoding="utf-8") as f:
    json.dump(state, f, indent=2, ensure_ascii=False)

print(f"VALIDATED:{valid_skills}/{total_skills}")
PYEOF

log_msg "SUCCESS" "========== COMPLETED ANTIGRAVITY SKILLS SYNC =========="
