import os
import time
import subprocess
import speech_recognition as sr
import RPi.GPIO as GPIO
from telegram import Bot
import datetime
import sounddevice as sd
from scipy.io.wavfile import write

# === Paths ===
MOBILITY_SCRIPT = "/home/user/Desktop/care_companion/human_detect.py"
VOICE_FILE = "/home/user/Desktop/care_companion/help_voice.wav"  # temp voice file

# === Telegram Bot Credentials ===
TELEGRAM_TOKEN = "8254072265:AAFGV0bg2MO8yjeSlyhBJXjybRgBtx60IRg"

CHAT_ID = "6897658812"

# === GPIO Setup ===
BUZZER_PIN = 17
LED_PIN = 27
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(LED_PIN, GPIO.OUT)

# === Voice Feedback ===
def speak(text):
    print(f"💬 {text}")
    os.system(f'espeak \"{text}\" 2>/dev/null || true')

# === Local Emergency Alert ===
def emergency_alert():
    print("🚨 Activating buzzer + LED...")
    for _ in range(5):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(0.3)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(0.3)
    print("✅ Local alert finished.")

# === Record short voice message ===
def record_voice_message(filename=VOICE_FILE, duration=5, fs=44100):
    print("🎙️ Recording live voice message...")
    try:
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()
        write(filename, fs, recording)
        print(f"✅ Voice message saved: {filename}")
        return filename
    except Exception as e:
        print(f"⚠️ Voice recording failed: {e}")
        return None

# === Telegram Message + Recorded Voice ===
def send_telegram_alert():
    print("📲 Sending Telegram alert + your recorded voice...")
    bot = Bot(token=TELEGRAM_TOKEN)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Text alert
    message = (
        f"🚨 *CARE COMPANION ALERT!* \n"
        f"🕒 *Time:* {timestamp}\n"
        f"Patient has triggered HELP command!\n"
        f"Please check immediately."
    )
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode="Markdown")

    # Record and send your live voice
    voice_file = record_voice_message()
    if voice_file and os.path.exists(voice_file):
        with open(voice_file, "rb") as vf:
            bot.send_voice(chat_id=CHAT_ID, voice=vf, caption="🎙️ Patient's live voice message")
        print("✅ Voice message sent via Telegram.")
        os.remove(voice_file)   # delete after sending
    else:
        print("⚠️ No voice file recorded.")

# === Human Detection ===
def start_human_detect():
    speak("Starting mobility and human detection")
    subprocess.run(["python3", MOBILITY_SCRIPT])
    speak("Human detection completed")

# === Command Matching ===
def match_command(text):
    t = text.lower().strip()
    if any(word in t for word in ["come", "hello", "helo", "halo", "asho", "ashok","kam","kem","cam","came","kaam"]):
        return "COME"
    elif any(word in t for word in ["help", "bacha", "bachao", "help me", "sos", "hel", "hal"]):
        return "HELP"
    return None

# === Main Program ===
if __name__ == "__main__":
    speak("Voice trigger active")
    print("🚀 Ready — say 'Come' or 'Help'")

    # Detect microphone
    mic_index = None
    names = sr.Microphone.list_microphone_names()
    for i, n in enumerate(names):
        if "C270" in n or "WEBCAM" in n:
            mic_index = i
            print(f"✅ Using mic '{n}' (index {i})")

    mic = sr.Microphone(device_index=mic_index) if mic_index is not None else sr.Microphone()
    r = sr.Recognizer()
    r.energy_threshold = 4000
    r.dynamic_energy_threshold = False

    # Calibrate mic
    with mic as src:
        print("🔈 Calibrating for 1 second...")
        r.adjust_for_ambient_noise(src, duration=1)

    try:
        with mic as src:
            print("\n🎤 Say 'Come' or 'Help' ...")
            audio = r.listen(src, timeout=None, phrase_time_limit=2)

        try:
            cmd_text = r.recognize_google(audio, language="en-US").lower()
            print(f"🗣️ Heard: {cmd_text}")
        except Exception:
            print("❌ Could not understand audio")
            cmd_text = ""

        cmd = match_command(cmd_text)
        if cmd == "COME":
            print("🚀 COME command detected")
            start_human_detect()
            speak("Task completed")

        elif cmd == "HELP":
            print("🚨 HELP command detected")
            speak("Emergency detected. Notifying caregiver.")
            emergency_alert()
            send_telegram_alert()
            speak("Caregiver notified successfully.")

        else:
            print("❓ No valid trigger detected")

    except KeyboardInterrupt:
        print("\n🛑 Exiting voice trigger...")
        GPIO.cleanup()
