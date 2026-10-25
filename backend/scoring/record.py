"""Record test clips: python -m scoring.record <word> <kind> <count>
   kind = correct | wrong | other
"""
import os
import sys

import sounddevice as sd
import soundfile as sf

SR = 16000       # 16 kHz, same as the app will send
SECONDS = 2.5

word, kind, count = sys.argv[1], sys.argv[2], int(sys.argv[3])
folder = os.path.join("scoring", "data", word)
os.makedirs(folder, exist_ok=True)

for i in range(1, count + 1):
    input(f"[{kind} {i}/{count}] press Enter, then say it...")
    audio = sd.rec(int(SR * SECONDS), samplerate=SR, channels=1, dtype="int16")
    sd.wait()
    path = os.path.join(folder, f"{kind}_{i}.wav")
    sf.write(path, audio, SR)
    print("saved", path)