# RETURNS from a table the set length of each designed gesture
def get_gesture_length(gesture_name):
    if gesture_name == "wait1":
        return 1.0
    elif gesture_name == "wait2":
        return 2.0
    elif gesture_name == "wait3":
        return 3.0
    elif gesture_name == "wait4":
        return 4.0
    elif gesture_name == "wait5":
        return 5.0
    elif gesture_name == 'wave':
        return 5.0
    elif gesture_name == 'shocked':
        return 2.2
    elif gesture_name == 'scared':
        return 2.4
    elif gesture_name == 'talk1':
        return 4.2
    elif gesture_name == 'display_left':
        return 2.0
    elif gesture_name == 'display_right':
        return 2.0
    elif gesture_name == 'plane':
        return 6.0
    elif gesture_name == 'imagination':
        return 4.6
    elif gesture_name == 'init':
        return 0.4
    elif gesture_name == 'hand_circle':
        return 3.8
    elif gesture_name == 'look_at_hands':
        return 7.6
    elif gesture_name == 'raise_up':
        return 5.8
    elif gesture_name == 'typing':
        return 5.6
    else:
        return 0.0

# RETURNS the pepper stored behavior file from a table according to gesture name
def get_behavior_name(gesture):
    if gesture == "wave":
        return "movement-2e59ad/wave"
    elif gesture == "shocked":
        return "movement-2e59ad/shocked"
    elif gesture == "scared":
        return "movement-2e59ad/scared"
    elif gesture == "talk1":
        return "movement-2e59ad/talk1"
    elif gesture == "display_left":
        return "movement-2e59ad/display_left"
    elif gesture == "display_right":
        return "movement-2e59ad/display_right"
    elif gesture == "plane":
        return "movement-2e59ad/plane"
    elif gesture == "imagination":
        return "movement-2e59ad/imagination"
    elif gesture == "init":
        return "movement-2e59ad/init"
    elif gesture == "hand_circle":
        return "movement-2e59ad/hand_circle"
    elif gesture == "look_at_hands":
        return "movement-2e59ad/look_at_hands"
    elif gesture == "raise_up":
        return "movement-2e59ad/raise_up"
    elif gesture == "typing":
        return "movement-2e59ad/typing"
    else:
        return "movement-2e59ad/init"


def get_voice_name(voice):
    if voice == 1:            #COMMON LADY
        return "tts_models/en/jenny/jenny"
    elif voice == 2:     #CREEPY
        return "tts_models/en/blizzard2013/capacitron-t2-c50"
    elif voice == 3:       #OLDER LADY
        return "tts_models/en/ljspeech/tacotron2-DDC"
    elif voice == 4:           #STUDDRE OLD LADY
        return "tts_models/en/ljspeech/glow-tts"
    elif voice == 5:      #OLDER LADY
        return "tts_models/en/ljspeech/tacotron2-DCA"
    elif voice == 6:           #AFRICAN MAN
        return "tts_models/yor/openbible/vits"
        # elif voice == "bark":         #BROKEN
        #     return "tts_models/multilingual/multi-dataset/bark"

    # 14: tts_models / en / ljspeech / speedy - speech
    # 16: tts_models / en / ljspeech / vits
    # 17: tts_models / en / ljspeech / vits - -neon
    # 18: tts_models / en / ljspeech / fast_pitch
    # 19: tts_models / en / ljspeech / overflow
    # 20: tts_models / en / ljspeech / neural_hmm
    # 21: tts_models / en / vctk / vits
    # 22: tts_models / en / vctk / fast_pitch
    # 23: tts_models / en / sam / tacotron - DDC
    # 24: tts_models / en / blizzard2013 / capacitron - t2 - c50
    # 25: tts_models / en / blizzard2013 / capacitron - t2 - c150_v2
    # 26: tts_models / en / multi - dataset / tortoise - v2
    # 32: tts_models / uk / mai / glow - tts
