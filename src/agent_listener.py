import time
import os
import datetime

AGENT_NAME = "GitHubCopilot"
LOG_PATH = "communication/general.md"
POLL_INTERVAL = 15  # saniye


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


def should_reply(last_msg):
    if not last_msg:
        return False
    # Kendi mesajımızı tekrar yanıtlamayalım
    if f"[{AGENT_NAME}]" in last_msg:
        return False
    # Eğer bize mention varsa veya genel bir soru ise yanıtla
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
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}] [{AGENT_NAME}]: {reply}"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
    print(f"Yanıt eklendi: {reply}")


def main():
    print(f"{AGENT_NAME} polling ile mesajları izliyor...")
    last_seen = None
    while True:
        try:
            last_msg = get_last_message()
            if last_msg and last_msg != last_seen:
                print(f"Son mesaj: {last_msg}")
                if should_reply(last_msg):
                    reply = generate_reply(last_msg)
                    if reply:
                        append_message(reply)
                last_seen = last_msg
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\nDinleme sonlandırıldı.")
            break
        except Exception as e:
            print(f"Hata: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
