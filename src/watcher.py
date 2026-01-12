#!/usr/bin/env python3
"""
Angular Rate Estimation Watcher Agent
Bu agent repository'deki değişiklikleri izler ve diğer agentlarla iletişim kurar.
"""

import time
import subprocess
import os
import datetime
import re

MY_AGENT_NAME = "GitHubCopilot"
LOG_PATH = "communication/general.md"
PUSH_COOLDOWN = 20  # seconds


class WatcherState:
    """Watcher agent'ın durumunu tutar"""
    def __init__(self):
        self.last_push_time = 0
        self.buffer = []
        self.remote_head = None

    def update_head(self, new_head):
        self.remote_head = new_head

    def reset(self):
        self.last_push_time = 0
        self.buffer = []


state = WatcherState()


def get_remote_head():
    """Remote repository'nin HEAD SHA'sını alır"""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "origin", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        sha = result.stdout.split()[0] if result.stdout else None
        return sha
    except subprocess.CalledProcessError:
        return None


def fetch_origin():
    """Origin'i fetch eder"""
    try:
        subprocess.run(["git", "fetch", "origin"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False


def get_diff_files(old_sha, new_sha):
    """İki commit arasındaki değişen dosyaları listeler"""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-status", old_sha, new_sha],
            capture_output=True,
            text=True,
            check=True
        )
        files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split(maxsplit=1)
                if len(parts) == 2:
                    status, filename = parts
                    files.append((status, filename))
        return files
    except subprocess.CalledProcessError:
        return []


def get_file_content_at_sha(filename, sha):
    """Belirli bir commit'teki dosya içeriğini alır"""
    try:
        result = subprocess.run(
            ["git", "show", f"{sha}:{filename}"],
            capture_output=True,
            text=True
        )
        return result.stdout if result.returncode == 0 else ""
    except Exception:
        return ""


def analyze_changes(filename, old_sha, new_sha):
    """Dosya değişikliklerini analiz eder"""
    report = f"📝 Değişiklik tespit edildi: {filename}\n"
    
    if filename.endswith('.py'):
        old_content = get_file_content_at_sha(filename, old_sha)
        new_content = get_file_content_at_sha(filename, new_sha)
        
        old_lines = len(old_content.split('\n'))
        new_lines = len(new_content.split('\n'))
        delta = new_lines - old_lines
        
        report += f"   Satır değişikliği: {delta:+d} (Toplam: {new_lines})\n"
        
        # Basit fonksiyon analizi
        old_funcs = set(re.findall(r'def\s+(\w+)\s*\(', old_content))
        new_funcs = set(re.findall(r'def\s+(\w+)\s*\(', new_content))
        
        added_funcs = new_funcs - old_funcs
        removed_funcs = old_funcs - new_funcs
        
        if added_funcs:
            report += f"   ➕ Yeni fonksiyonlar: {', '.join(added_funcs)}\n"
        if removed_funcs:
            report += f"   ➖ Silinen fonksiyonlar: {', '.join(removed_funcs)}\n"
    
    elif filename.endswith('.md'):
        report += "   📄 Dokümantasyon güncellemesi\n"
    
    return report


def check_missed_messages():
    """Kaçırılan mesajları kontrol eder"""
    try:
        if not os.path.exists(LOG_PATH):
            return
        
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Son mesajı bul
        last_msg = None
        for line in reversed(lines):
            if line.strip() and "]:" in line:
                last_msg = line
                break
        
        if last_msg and f"[{MY_AGENT_NAME}]" not in last_msg:
            # Son mesaj benden değil, yanıt gerekebilir
            if "@" + MY_AGENT_NAME.lower() in last_msg.lower():
                print(f"[Kaçırılan Mesaj Tespit Edildi]: {last_msg.strip()}")
                
    except Exception as e:
        print(f"Mesaj kontrolünde hata: {e}")


def buffer_reply(reply):
    """Yanıtı buffer'a ekler"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"\n[{timestamp}] [{MY_AGENT_NAME}]: {reply}"
    state.buffer.append(entry)


def flush_buffer_if_needed(force=False):
    """Buffer'ı gerekirse flushlayıp push eder"""
    if not state.buffer:
        return
    
    now = time.time()
    if not force and (now - state.last_push_time) < PUSH_COOLDOWN:
        print(f"⏳ Cooldown aktif ({PUSH_COOLDOWN - int(now - state.last_push_time)}s kaldı)")
        return
    
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            for entry in state.buffer:
                f.write(entry)
        
        subprocess.run(["git", "add", LOG_PATH], check=True)
        subprocess.run(["git", "commit", "-m", f"Agent update from {MY_AGENT_NAME}"], check=True)
        subprocess.run(["git", "push"], check=True)
        
        print(f"✅ {len(state.buffer)} mesaj push edildi!")
        state.buffer = []
        state.last_push_time = now
        
    except Exception as e:
        print(f"❌ Push hatası: {e}")


def process_remote_changes(remote_sha):
    """Remote değişikliklerini işler"""
    if not state.remote_head:
        state.update_head(remote_sha)
        print(f"🔄 İlk senkronizasyon: {remote_sha[:8]}")
        return
    
    if state.remote_head == remote_sha:
        return
    
    old_sha = state.remote_head
    print(f"\n🔔 Yeni değişiklik tespit edildi!")
    print(f"   {old_sha[:8]} -> {remote_sha[:8]}")
    
    # Fetch ve değişiklikleri analiz et
    if fetch_origin():
        changed_files = get_diff_files(old_sha, remote_sha)
        
        if changed_files:
            report_parts = []
            for status, filename in changed_files:
                if filename == LOG_PATH:
                    continue  # Kendi log dosyamızı analiz etme
                
                analysis = analyze_changes(filename, old_sha, remote_sha)
                report_parts.append(analysis)
            
            if report_parts:
                full_report = "\n".join(report_parts)
                buffer_reply(full_report)
        
        # Yeni HEAD'i güncelle
        state.update_head(remote_sha)
        
        # Kaçırılan mesajları kontrol et
        check_missed_messages()
        
        # Buffer'ı flush et
        flush_buffer_if_needed()


def monitor():
    """Ana izleme döngüsü"""
    print(f"🤖 {MY_AGENT_NAME} başlatıldı!")
    print(f"📂 Dizin: {os.getcwd()}")
    print(f"📊 İzleme modu: 60 saniye aralıklarla\n")
    
    poll_count = 0
    
    while True:
        try:
            poll_count += 1
            print(f"[Polling #{poll_count}] Kontrol ediliyor...")
            
            remote_sha = get_remote_head()
            if remote_sha:
                process_remote_changes(remote_sha)
            else:
                print("⚠️ Remote HEAD alınamadı")
            
            # Periyodik mesaj kontrolü
            if poll_count % 5 == 0:
                check_missed_messages()
            
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n\n👋 Watcher agent durduruluyor...")
            flush_buffer_if_needed(force=True)
            break
        except Exception as e:
            print(f"❌ Hata: {e}")
            time.sleep(60)


if __name__ == "__main__":
    monitor()
