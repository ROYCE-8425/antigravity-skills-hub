#!/usr/bin/env bash
# ==============================================================================
# Antigravity Remote VM One-Command Bootstrap Installer
# ==============================================================================
# Installs all Custom Skills, UI/UX Rules, Production Engineering Skills,
# Anthropic Skills, and 6 Git-backed Plugin Repos (superpowers, ponytail,
# caveman, emilkowalski-skills, gsap-skills, scroll-world), plus the
# `update-skills` CLI tool and automatic background sync on Antigravity Remote VM.
# ==============================================================================

set -euo pipefail
export GIT_TERMINAL_PROMPT=0

HUB_REPO="https://github.com/ROYCE-8425/antigravity-skills-hub.git"
GLOBAL_CONFIG_DIR="${HOME}/.gemini/config"
HUB_CACHE_DIR="${GLOBAL_CONFIG_DIR}/.hub-cache"
SCRIPTS_DIR="${GLOBAL_CONFIG_DIR}/scripts"

mkdir -p "${GLOBAL_CONFIG_DIR}" "${SCRIPTS_DIR}" "${HOME}/.local/bin"

echo "=================================================================="
echo "  ANTIGRAVITY REMOTE VM SKILLS & AUTO-UPDATER BOOTSTRAP"
echo "=================================================================="

if [[ ! -d "${HUB_CACHE_DIR}/.git" ]]; then
  rm -rf "${HUB_CACHE_DIR}"
  git clone --depth 1 "${HUB_REPO}" "${HUB_CACHE_DIR}"
else
  git -C "${HUB_CACHE_DIR}" fetch origin main
  git -C "${HUB_CACHE_DIR}" reset --hard origin/main
fi

cp -f "${HUB_CACHE_DIR}/import_manifest.json" "${GLOBAL_CONFIG_DIR}/import_manifest.json"
cp -f "${HUB_CACHE_DIR}/scripts/update-skills.sh" "${SCRIPTS_DIR}/update-skills.sh"
chmod +x "${SCRIPTS_DIR}/update-skills.sh"

# Run full sync + cron registration + status display
bash "${SCRIPTS_DIR}/update-skills.sh"
bash "${SCRIPTS_DIR}/update-skills.sh" --cron
bash "${SCRIPTS_DIR}/update-skills.sh" --status
