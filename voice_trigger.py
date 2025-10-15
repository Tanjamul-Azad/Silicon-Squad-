import os
import time
import signal
import subprocess
import speech_recognition as sr
import motor_control as mc

# === Path to your mobility program ===
MOBILITY_SCRIPT = "/home/user/Desktop/care_companion/human_detect.py"
mobility_process = None

# === Speak feedback via espeak ===
def speak(text: str):
    print(f"💬 {text}")
    os.system(f'espeak "{text}" 2>/dev/null || true')

# === Find webcam microphone automatically ===
def find_c270_index():
    names = sr.Microphone.list_microphone_names()
    print("🎧 Available microphones:", names)
    for i, n in enumerate(names):
        if "C270" in n or "WEBCAM" in n:
            print(f"✅ Using mic '{n}' (index {i})")
            return i
    print("⚠️ Webcam mic not found, using fallback index 2")
    return 2

# === Start mobility script ===
def start_mobility():
    global mobility_process
    if mobility_process is None:
        speak("Starting mobility system")
        print("🚗 Launching human_detect.py ...")
        mobility_process = subprocess.Popen(
            ["python3", MOBILITY_SCRIPT], preexec_fn=os.setsid
        )
    else:
        print("ℹ️ Mobility already running")

# === Stop mobility and move backward ===
def stop_mobility():
    global mobility_process
    if mobility_process:
        print("🛑 Stopping mobility system...")
        try:
            os.killpg(os.getpgid(mobility_process.pid), signal.SIGTERM)
        except Exception as e:
            print(f"⚠️ stop error: {e}")
        mobility_process = None
    speak("Going back")
    mc.backward(60)
    time.sleep(1.5)
    mc.stop()

# === Match voice command text ===
def match_command(text: str):
    t = text.lower().strip()
    # split for quick fuzzy matching
    words = t.replace(",", " ").replace(".", " ").split()

    # anything that sounds like "come kiki"
    if ("come" in words and any(w.startswith("ki") or "key" in w for w in words)) \
       or "kiki" in t or "cookie" in t or "kom kiki" in t:
        return "COME"

    # anything that sounds like "go"
    if "go" in words or "goh" in t or "gow" in t:
        return "GO"

    return None


# === Listen once and return recognized text ===
def listen_once(recognizer: sr.Recognizer, mic: sr.Microphone):
    print("\n🎤 Listening for 'Come KIKI' or 'Go'...")
    with mic as source:
        recognizer.dynamic_energy_threshold = True
        recognizer.pause_threshold = 0.6
        print("🔈 Calibrating noise (1 s)...")
        recognizer.adjust_for_ambient_noise(source, duration=1.0)
        print(f"🔎 Energy threshold: {int(recognizer.energy_threshold)}")
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=3.0)

    # Save what we heard for debugging
    try:
        wav_bytes = audio.get_wav_data()
        with open("/tmp/last_cmd.wav", "wb") as f:
            f.write(wav_bytes)
        print("💾 Saved /tmp/last_cmd.wav (play with: aplay /tmp/last_cmd.wav)")
    except Exception as e:
        print(f"⚠️ Couldn’t save wav: {e}")

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand audio (speak clearer or closer)")
        return None
    except sr.RequestError as e:
        print(f"⚠️ Recognition service error: {e}")
        return None

# === Main ===
if __name__ == "__main__":
    speak("Voice trigger active")
    print("🚀 Voice Trigger Started — say 'Come KIKI' to begin, 'Go' to stop/return")

    mic_index = find_c270_index()
    mic = sr.Microphone(device_index=mic_index, sample_rate=16000, chunk_size=1024)
    r = sr.Recognizer()

    try:
        while True:
            text = listen_once(r, mic)
            if not text:
                continue
            cmd = match_command(text)
            if cmd == "COME":
                start_mobility()
            elif cmd == "GO":
                stop_mobility()
            else:
                print("❓ No valid trigger detected")
            time.sleep(0.3)
    except KeyboardInterrupt:
        print("\n🛑 Exiting...")
        try:
            stop_mobility()
        finally:
            mc.stop()
