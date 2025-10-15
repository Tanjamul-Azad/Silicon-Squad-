import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("🎤 Say something (e.g. 'Come KIKI' or 'Go') ...")
    audio = r.listen(source)

print("🎧 Processing...")
try:
    text = r.recognize_google(audio)
    print("✅ Google heard:", text)
except sr.UnknownValueError:
    print("❌ Could not understand audio")
except sr.RequestError as e:
    print(f"⚠️ Network error: {e}")
