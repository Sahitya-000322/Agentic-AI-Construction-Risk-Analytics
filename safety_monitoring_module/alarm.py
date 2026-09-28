import os

def play_alarm(status):

    if "Missing" in status:
        print("🔊 Alarm Triggered!")
        os.system("afplay sounds/mixkit-emergency-alert-alarm-1007.wav")

    else:
        print("✅ No Alarm Needed")