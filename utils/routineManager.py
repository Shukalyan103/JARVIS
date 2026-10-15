import os
import sys
import json
import time
import shutil
import subprocess
import webbrowser
from colorama import Fore, Style, init

init(autoreset=True)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "routine_config.json")

DEFAULT_ROUTINE = {
    "routine_name": "Daily Workspace Routine",
    "delay_between_apps_seconds": 3,
    "apps": [
        {
            "name": "Visual Studio Code",
            "voice_announcement": "Opening Visual Studio Code",
            "type": "executable",
            "primary_command": "code",
            "project_path": "",
            "fallback_paths": [
                "%LOCALAPPDATA%\\Programs\\Microsoft VS Code\\Code.exe"
            ]
        },
        {
            "name": "Google Chrome",
            "voice_announcement": "Opening Google Chrome",
            "type": "executable",
            "primary_command": "chrome",
            "fallback_paths": [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
            ]
        },
        
    ]
}


def load_routine_config():
    """Loads routine configuration or creates default if missing."""
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(Fore.RED + f"[RoutineManager] Error loading config: {e}. Using defaults.")
    
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_ROUTINE, f, indent=2)
    return DEFAULT_ROUTINE


def launch_single_app(app):
    """
    Launches an application based on its config entry.
    Handles executable paths, Windows URIs, project directories, and browser fallbacks.
    Supports 'project_path' or 'args' to open specific workspaces/folders.
    """
    import shlex

    app_name = app.get("name", "Unknown Application")
    primary_cmd = app.get("primary_command", "")
    fallback_paths = app.get("fallback_paths", [])
    web_fallback = app.get("web_fallback", "")
    project_path = app.get("project_path") or app.get("directory") or app.get("folder")
    raw_args = app.get("args", [])

    print(Fore.CYAN + f"\n[RoutineManager] 🚀 Preparing to launch: {app_name}...")

    # Collect project path / command line arguments
    app_args = []
    if project_path:
        expanded_project = os.path.expandvars(os.path.expanduser(str(project_path).strip()))
        if not os.path.isabs(expanded_project):
            expanded_project = os.path.abspath(expanded_project)
        app_args.append(expanded_project)

    if isinstance(raw_args, str):
        if raw_args.strip():
            try:
                app_args.extend(shlex.split(os.path.expandvars(raw_args), posix=False))
            except Exception:
                app_args.append(os.path.expandvars(raw_args))
    elif isinstance(raw_args, list):
        for arg in raw_args:
            app_args.append(os.path.expandvars(str(arg)))

    # 1. Try explicit fallback paths if they exist
    for path_template in fallback_paths:
        expanded_path = os.path.expandvars(path_template)
        exe_part = None
        extra_args = []

        if os.path.isfile(expanded_path):
            exe_part = expanded_path
        elif ".exe " in expanded_path.lower():
            idx = expanded_path.lower().find(".exe ") + 4
            candidate_exe = expanded_path[:idx].strip('\"\'')
            if os.path.isfile(candidate_exe):
                exe_part = candidate_exe
                try:
                    extra_args = shlex.split(expanded_path[idx:].strip(), posix=False)
                except Exception:
                    extra_args = [expanded_path[idx:].strip()]
        elif os.path.exists(expanded_path.split(" ", 1)[0]):
            parts = expanded_path.split(" ", 1)
            exe_part = parts[0]
            if len(parts) > 1:
                extra_args = [parts[1]]

        if exe_part and os.path.exists(exe_part):
            try:
                full_args = extra_args + app_args
                if full_args:
                    subprocess.Popen([exe_part] + full_args, shell=True)
                else:
                    if hasattr(os, "startfile"):
                        os.startfile(exe_part)
                    else:
                        subprocess.Popen([exe_part])
                print(Fore.GREEN + f"  ✓ Successfully launched {app_name} via {exe_part}")
                return True, exe_part
            except Exception as e:
                print(Fore.YELLOW + f"  ! Could not launch path {exe_part}: {e}")

    # 2. Check if primary command is in system PATH
    cmd_tokens = []
    if primary_cmd and not primary_cmd.endswith(":"):
        try:
            cmd_tokens = shlex.split(primary_cmd, posix=False)
        except Exception:
            cmd_tokens = primary_cmd.split()

    if cmd_tokens:
        base_cmd = cmd_tokens[0]
        cmd_inline_args = cmd_tokens[1:]
        resolved_cmd = shutil.which(base_cmd)
        if resolved_cmd:
            try:
                full_cmd_args = cmd_inline_args + app_args
                if full_cmd_args or resolved_cmd.endswith((".bat", ".cmd")):
                    subprocess.Popen([resolved_cmd] + full_cmd_args, shell=True)
                else:
                    if hasattr(os, "startfile"):
                        os.startfile(resolved_cmd)
                    else:
                        subprocess.Popen([resolved_cmd])
                print(Fore.GREEN + f"  ✓ Successfully launched {app_name} from PATH: {resolved_cmd}")
                return True, resolved_cmd
            except Exception as e:
                print(Fore.YELLOW + f"  ! Error launching resolved command {resolved_cmd}: {e}")

    # 3. Try Windows protocol URI (e.g. spotify:, discord:)
    if primary_cmd.endswith(":"):
        try:
            if hasattr(os, "startfile"):
                os.startfile(primary_cmd)
                print(Fore.GREEN + f"  ✓ Successfully launched {app_name} using protocol: {primary_cmd}")
                return True, primary_cmd
        except Exception as e:
            print(Fore.YELLOW + f"  ! Protocol launch failed for {primary_cmd}: {e}")

    # 4. Fallback to web link if provided (e.g. Discord web)
    if web_fallback:
        try:
            print(Fore.YELLOW + f"  ℹ Application not found locally. Launching web version: {web_fallback}")
            webbrowser.open(web_fallback)
            return True, web_fallback
        except Exception as e:
            print(Fore.RED + f"  ✗ Failed to open web fallback: {e}")

    print(Fore.RED + f"  ✗ Could not locate or launch {app_name}")
    return False, "Not found"


def is_routine_trigger(text):
    """
    Determines if the spoken or typed text corresponds to the daily routine command.
    Forgiving pattern matching allows for natural variations.
    """
    if not text:
        return False
    
    cleaned = text.lower().strip()

    # Exact key phrases
    exact_triggers = [
        "start my daily routine",
        "start daily routine",
        "start my routine",
        "start routine",
        "begin daily routine",
        "begin routine",
        "open my daily routine",
        "open daily routine",
        "open routine",
        "run my daily routine",
        "run daily routine",
        "execute daily routine",
        "launch daily routine",
        "daily routine",
        "start my daily daily routine", # in case user repeats
        "start daily daily routine",
    ]

    for trigger in exact_triggers:
        if trigger in cleaned:
            return True

    # Combination rules (e.g., "jarvis, daily routine please")
    routine_words = ["routine", "rountine", "rutine", "routin"]
    has_routine = any(rw in cleaned for rw in routine_words)
    has_action = any(verb in cleaned for verb in ["start", "begin", "open", "run", "launch", "execute"])
    has_daily = "daily" in cleaned or "morning" in cleaned

    if has_routine and (has_daily or has_action):
        return True

    return False


def execute_daily_routine(speak_callback=None):
    """
    Executes the daily routine:
    1. Announces start of routine.
    2. Opens each software one by one.
    3. Speaks announcements and waits for the configured delay.
    4. Announces completion.
    """
    config = load_routine_config()
    apps = config.get("apps", [])
    delay = config.get("delay_between_apps_seconds", 3)

    print(Fore.MAGENTA + Style.BRIGHT + "\n==============================================")
    print(Fore.MAGENTA + Style.BRIGHT + "       JARVIS DAILY ROUTINE INITIATED         ")
    print(Fore.MAGENTA + Style.BRIGHT + "==============================================\n")

    if speak_callback:
        speak_callback("Initiating your daily routine, sir. Setting up your workspace.")

    for index, app in enumerate(apps, start=1):
        app_name = app.get("name", f"Application {index}")
        announcement = app.get("voice_announcement", f"Opening {app_name}")

        print(Fore.YELLOW + f"[{index}/{len(apps)}] {announcement}...")
        if speak_callback:
            speak_callback(announcement)

        success, detail = launch_single_app(app)

        # Wait between apps so system can launch them gracefully
        if index < len(apps):
            print(Fore.BLUE + f"Waiting {delay} seconds before opening next application...")
            time.sleep(delay)

    print(Fore.GREEN + Style.BRIGHT + "\n[Routine Complete] All daily routine applications have been launched.\n")
    if speak_callback:
        speak_callback("All daily routine applications are open, sir. Your workstation is ready.")


if __name__ == "__main__":
    print("Testing Daily Routine Manager:")
    execute_daily_routine()
