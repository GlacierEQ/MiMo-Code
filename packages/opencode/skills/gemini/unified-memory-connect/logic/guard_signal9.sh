#!/data/data/com.termux/files/usr/bin/bash
# APEX Signal 9 Guard & Monitor for Google Tablet / Android
# v1.0 - Synthesized: 2026-06-03

C_GREEN="\033[92m"
C_RED="\033[91m"
C_YELLOW="\033[93m"
C_CYAN="\033[96m"
C_BOLD="\033[1m"
C_RESET="\033[0m"

echo -e "${C_BOLD}${C_CYAN}🛡️  APEX SIGNAL 9 GUARD & MONITORS FOR GOOGLE TABLET${C_RESET}"
echo -e "──────────────────────────────────────────────────────────────────────"

# 1. Check Active Process Count
PROCESS_COUNT=$(ps -efww | grep -v grep | wc -l)
MAX_SAFE_PROCESSES=28

echo -e " ▸ Current active processes in Termux: ${C_BOLD}${PROCESS_COUNT}${C_RESET} / 32 limit"

if [ "$PROCESS_COUNT" -gt "$MAX_SAFE_PROCESSES" ]; then
    echo -e " ⚠️  ${C_RED}${C_BOLD}WARNING:${C_RESET} You are close to Android's 32-process phantom process limit!"
    echo -e "    Spawning more tasks may trigger a sudden Signal 9 crash of Termux."
    echo -e "    Run ${C_YELLOW}ps -efww${C_RESET} to inspect and terminate redundant background processes."
else
    echo -e " ▸ Process count check: ${C_GREEN}SAFE (${PROCESS_COUNT} running)${C_RESET}"
fi

echo -e "──────────────────────────────────────────────────────────────────────"
echo -e "${C_BOLD}📖 RESEARCH SUMMARY: SIGNAL 9 ON GOOGLE TABLET${C_RESET}"
echo -e "On modern Android (12 through 16) running on Google Tablets / Pixel Tablet:"
echo -e "1. ${C_BOLD}Phantom Process Killer (PPK)${C_RESET} terminates any app spawning > 32 child processes."
echo -e "2. ${C_BOLD}Background CPU Restrictions${C_RESET} terminate child processes using high background CPU."
echo -e "3. ${C_BOLD}Battery Optimization / Suspend${C_RESET} freezes Termux when the screen goes off."

echo -e "\n${C_BOLD}🛠️  PERMANENT WORKAROUNDS (Choose One):${C_RESET}"
echo -e "  ${C_BOLD}Option A: Developer Options Toggle (Easiest on Android 14/15/16)${C_RESET}"
echo -e "    1. Go to Google Tablet ${C_BOLD}Settings > About Tablet${C_RESET}."
echo -e "    2. Tap ${C_BOLD}Build number${C_RESET} 7 times to enable Developer Options."
echo -e "    3. Go to ${C_BOLD}Settings > System > Developer Options${C_RESET}."
echo -e "    4. Find and enable: ${C_GREEN}${C_BOLD}Disable child process restrictions${C_RESET}."

echo -e "\n  ${C_BOLD}Option B: Wireless Debugging & Local ADB Setup${C_RESET}"
echo -e "    If the toggle is missing, you can disable it directly from Termux:"
echo -e "    1. Enable ${C_BOLD}Wireless Debugging${C_RESET} under Developer Options."
echo -e "    2. Tap 'Wireless Debugging' and click 'Pair device with pairing code'."
echo -e "    3. In Termux, install ADB: ${C_YELLOW}pkg install android-tools${C_RESET}"
echo -e "    4. Pair your device: ${C_YELLOW}adb pair localhost:<port_from_screen>${C_RESET} and enter code."
echo -e "    5. Connect to ADB: ${C_YELLOW}adb connect localhost:<port_from_main_screen>${C_RESET}"
echo -e "    6. Execute the APEX guard command below to disable restrictions permanently."

echo -e "\n${C_BOLD}⚡ RUN THIS IN TERMUX AFTER ADB CONNECTION IS ESTABLISHED:${C_RESET}"
echo -e "  ${C_GREEN}adb shell \"/system/bin/device_config set_sync_disabled_for_tests persistent\""
echo -e "  adb shell \"/system/bin/device_config put activity_manager max_phantom_processes 2147483647\""
echo -e "  adb shell settings put global settings_enable_monitor_phantom_procs false${C_RESET}"
echo -e "──────────────────────────────────────────────────────────────────────"
