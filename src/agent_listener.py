import time
import os
import datetime
import subprocess

AGENT_NAME = "GitHubCopilot"
LOG_PATH = "communication/general.md"
POLL_INTERVAL = 15  # saniye
# If ENABLE_REPLY is False, the listener will NOT write replies to `communication/general.md`.
# This enables silent monitoring mode requested by the user.
ENABLE_REPLY = True
# If SILENT is True the script will avoid printing to stdout.
SILENT = True
# Heartbeat: post an "active" message every HEARTBEAT_INTERVAL seconds
HEARTBEAT_INTERVAL = 30


def get_last_message():
    if not os.path.exists(LOG_PATH):
        return None
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Son mesajı bul
    for line in reversed(lines):
        if line.strip() and "]:" in line:
            return line.strip()
    return None


def git_pull():
    try:
        subprocess.run(["git", "pull", "--no-rebase"], check=False, capture_output=True)
    except Exception:
        pass


def should_reply(last_msg):
    if not last_msg:
        return False
    # Kendi mesajımızı tekrar yanıtlamayalım
    if f"[{AGENT_NAME}]" in last_msg:
        return False
    # Eğer bize mention varsa veya genel bir soru ise yanıtla (but only if replies enabled)
    if not ENABLE_REPLY:
        return False
    if f"@{AGENT_NAME.lower()}" in last_msg.lower() or "?" in last_msg:
        return True
    return False


def generate_reply(last_msg):
    # Basit mantık: mention veya soru varsa selamla
    if "merhaba" in last_msg.lower():
        return "Merhaba! Ben buradayım ve repoyu izliyorum. Bir isteğiniz olursa mention atabilirsiniz."
    if "test" in last_msg.lower():
        return "Test fonksiyonları ve senaryoları için önerilerim hazır. Detay ister misiniz?"
    if "?" in last_msg:
        return "Sorunuzu aldım, analiz ediyorum. Kısa sürede dönüş yapacağım."
    if f"@{AGENT_NAME.lower()}" in last_msg.lower():
        return "Mention için teşekkürler! Size nasıl yardımcı olabilirim?"
    return None


def append_message(reply):
    """Append reply to communication log (only used when ENABLE_REPLY True)."""
    if not ENABLE_REPLY:
        return
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}] [{AGENT_NAME}]: {reply}"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    # Commit & push the reply so other agents see it remotely
    try:
        subprocess.run(["git", "add", LOG_PATH], check=False, capture_output=True)
        subprocess.run(["git", "commit", "-m", f"Agent reply from {AGENT_NAME}"], check=False, capture_output=True)
        subprocess.run(["git", "push"], check=False, capture_output=True)
    except Exception:
        pass

    if not SILENT:
        print(f"Yanıt eklendi: {reply}")


def main():
    if not SILENT:
        print(f"{AGENT_NAME} polling ile mesajları izliyor...")
    last_seen = None
    last_heartbeat = 0
    while True:
        try:
            # Ensure latest remote messages are pulled before checking
            git_pull()
            last_msg = get_last_message()
            if last_msg and last_msg != last_seen:
                if not SILENT:
                    print(f"Son mesaj: {last_msg}")
                if should_reply(last_msg):
                    reply = generate_reply(last_msg)
                    if reply:
                        append_message(reply)
                # Update last_seen regardless to avoid reprocessing same message
                last_seen = last_msg
            # Heartbeat to show active presence to other agents (commits a short message)
            now = time.time()
            if ENABLE_REPLY and (now - last_heartbeat) >= HEARTBEAT_INTERVAL:
                try:
                    append_message("status: active")
                    last_heartbeat = now
                except Exception:
                    pass
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            if not SILENT:
                print("\nDinleme sonlandırıldı.")
            break
        except Exception as e:
            if not SILENT:
                print(f"Hata: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
