import os
import time
import requests
from dotenv import load_dotenv
from pypresence import Presence
import threading
from pystray import Icon, Menu, MenuItem
from PIL import Image

load_dotenv()

RA_USERNAME = os.getenv("RA_USERNAME")
RA_API_KEY = os.getenv("RA_API_KEY")
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
POLL_SECONDS = int(os.getenv("POLL_SECONDS", "120"))


def get_user_profile(username, api_key):
    url = "https://retroachievements.org/API/API_GetUserProfile.php"
    params = {
        "u": username,
        "y": api_key,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def get_game(game_id, username, api_key):
    url = "https://retroachievements.org/API/API_GetGame.php"
    params = {
        "i": game_id,
        "z": username,
        "y": api_key,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def get_user_recent_achievements(username, api_key, minutes=120):
    url = "https://retroachievements.org/API/API_GetUserRecentAchievements.php"
    params = {
        "u": username,
        "y": api_key,
        "m": minutes,
    }

    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


def connect_discord(client_id):
    rpc = Presence(client_id)
    rpc.connect()
    return rpc


def run_presence():
    try:
        rpc = connect_discord(DISCORD_CLIENT_ID)
        print("Connected to Discord.")

        last_game_id = None
        last_achievement_id = None
        last_achievement_title = None
        start_time = int(time.time())

        while True:
            profile = get_user_profile(RA_USERNAME, RA_API_KEY)

            rich_presence = profile.get("RichPresenceMsg")
            game_id = profile.get("LastGameID")

            if not game_id:
                print("No game detected.")
                time.sleep(180)
                continue

            recent_achievement_title = None
            recent_achievement_id = None

            recent_achievements = get_user_recent_achievements(
                RA_USERNAME,
                RA_API_KEY,
                minutes=120,
            )

            if recent_achievements:
                current_game_id = int(game_id)

                for achievement in recent_achievements:
                    achievement_game_id = achievement.get("GameID")

                    if achievement_game_id is not None and int(achievement_game_id) == current_game_id:
                        recent_achievement_title = achievement.get("Title")
                        recent_achievement_id = achievement.get("AchievementID")
                        break

            game_changed = game_id != last_game_id
            achievement_changed = recent_achievement_id != last_achievement_id
            should_update = game_changed or achievement_changed

            if game_changed:
                print(f"Game changed -> {game_id}")
            elif achievement_changed:
                print(f"Achievement changed -> {recent_achievement_id}")

            if should_update:
                game = get_game(game_id, RA_USERNAME, RA_API_KEY)

                game_name = game.get("Title")
                console_name = game.get("ConsoleName")

                icon_url = None
                icon_path = game.get("ImageIcon")
                if icon_path:
                    icon_url = f"https://retroachievements.org{icon_path}"
                    print("Icon URL:", icon_url)

                print("Updating Discord...")
                print("Game:", game_name)
                print("Console:", console_name)

                if game_changed:
                    start_time = int(time.time())

                clean_presence = None

                if rich_presence:
                    rp_lower = rich_presence.lower()
                    game_lower = (game_name or "").lower()

                    if game_lower not in rp_lower:
                        clean_presence = rich_presence

                if clean_presence:
                    base_details = (
                        f"{clean_presence} on {console_name}"
                        if console_name else clean_presence
                    )
                else:
                    base_details = (
                        f"Playing {game_name} on {console_name}"
                        if console_name else f"Playing {game_name}"
                    )

                details_text = f"🎮 {base_details}"

                display_achievement_title = recent_achievement_title or last_achievement_title

                if display_achievement_title:
                    state_text = f"🏆 {display_achievement_title}"
                else:
                    state_text = None

                rpc.update(
                    details=details_text,
                    state=state_text,
                    large_image=icon_url if icon_url else "ra_logo",
                    large_text=game_name or "RetroAchievements",
                    start=start_time,
                )

                last_game_id = game_id
                last_achievement_id = recent_achievement_id
                if recent_achievement_title:
                    last_achievement_title = recent_achievement_title
                
            else:
                print(f"No change... (checked at {time.strftime('%H:%M:%S')})")

            time.sleep(POLL_SECONDS)

    except Exception as error:
        print("Something went wrong in background thread:")
        print(error)


def on_quit(icon, item):
    icon.stop()
    os._exit(0)


def setup_tray():
    image = Image.open("ra_logo.png")
    menu = Menu(
        MenuItem("Quit", on_quit)
    )
    return Icon("RADRichPresence", image, "RAD Rich Presence", menu)


def main():
    if not RA_USERNAME or not RA_API_KEY or not DISCORD_CLIENT_ID:
        print("Missing values in .env file.")
        input("Press Enter to close...")
        return

    worker = threading.Thread(target=run_presence, daemon=True)
    worker.start()

    tray = setup_tray()
    tray.run()


if __name__ == "__main__":
    main()