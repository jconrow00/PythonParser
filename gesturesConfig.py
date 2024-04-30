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
    elif gesture_name == "wait6":
        return 6.0
    elif gesture_name == "wait7":
        return 7.0
    elif gesture_name == 'wave':
        return 4.2
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
    elif gesture_name == 'proposition':
        return 5.0
    elif gesture_name == 'chuckle':
        return 3.6
    elif gesture_name == 'laugh':
        return 3.6
    elif gesture_name == 'head_tilt':
        return 2.0
    elif gesture_name == 'head_bobble':
        return 2.8
    elif gesture_name == 'what':
        return 1.0
    elif gesture_name == 'power_up':
        return 2.0
    elif gesture_name == 'blink_lights':
        return 1.5
    elif gesture_name == 'scan':
        return 3.3
    elif gesture_name == 'no':
        return 2.6
    elif gesture_name == 'beep_boop':
        return 2.0
    elif gesture_name == 'nudge':
        return 2.0
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
    elif gesture == "proposition":
        return "movement-2e59ad/proposition"
    elif gesture == "chuckle":
        return "movement-2e59ad/chuckle"
    elif gesture == "laugh":
        return "movement-2e59ad/laugh"
    elif gesture == "head_tilt":
        return "movement-2e59ad/head_tilt"
    elif gesture == "head_bobble":
        return "movement-2e59ad/head_bobble"
    elif gesture == "what":
        return "movement-2e59ad/what"
    elif gesture == "power_up":
        return "movement-2e59ad/power_up"
    elif gesture == "blink_lights":
        return "movement-2e59ad/blink_lights"
    elif gesture == 'scan':
        return "movement-2e59ad/scan"
    elif gesture == 'no':
        return "movement-2e59ad/no"
    elif gesture == 'beep_boop':
        return "movement-2e59ad/beep_boop"
    elif gesture == 'nudge':
        return "movement-2e59ad/nudge"
    else:
        return "movement-2e59ad/init"


def get_voice_name(voice):
    if voice == 1:         #COMMON LADY                 GOOD
        return "tts_models/en/jenny/jenny"
    elif voice == 2:       #CLEAR CONFIDENT WOMAN        GOOD
        return "tts_models/en/ljspeech/vits"
    elif voice == 3:      #SLOW MIXED UNSETTLING        GOOD
        return "tts_models/en/sam/tacotron-DDC"
    elif voice == 4:     #CLEAR SERIOUS WOMAN           GOOD
        return "tts_models/en/ljspeech/overflow"
    elif voice == 5:     #CLEAR ROBO WOMAN             GOOD
        return "tts_models/en/ljspeech/vits--neon"
    elif voice == 6:       #OLDER LADY                  GOOD
        return "tts_models/en/ljspeech/tacotron2-DDC"
    elif voice == 7:       #FAST QUIET CREEPY           OK
        return "tts_models/en/blizzard2013/capacitron-t2-c150_v2"
    elif voice == 8:       #SLOW ROBO OLD LADY          OK
        return "tts_models/en/ljspeech/glow-tts"
    elif voice == 9:      #OLDER LADY                   OK
        return "tts_models/en/ljspeech/tacotron2-DCA"
    elif voice == 10:      #CLEAR STROKE                 OK
        return "tts_models/en/ljspeech/neural_hmm"
    elif voice == 11:     #CLEAR HICCUP WOMAN           OK
        return "tts_models/en/ljspeech/fast_pitch"
    elif voice == 12:     #SLOW STUTTER WOMAN           OK
        return "tts_models/en/ljspeech/tacotron2-DCA"
    elif voice == 13:     #CLEAR BAD PRONOUNCE WOMAN    OK
        return "tts_models/en/ljspeech/tacotron2-DDC_ph"
    elif voice == 14:  # WOBBLE WOMAN                   BAD
        return "tts_models/en/ljspeech/speedy-speech"
    elif voice == 15:  # HALF POSSESSED WOMAN           BAD
        return "tts_models/en/ljspeech/glow-tts"
    elif voice == 16:  # AFRICAN MAN                     BAD
        return "tts_models/yor/openbible/vits"

        # elif voice == 17:     #BROKEN use_phonemes
        #     return "vocoder_models/en/ljspeech/multiband-melgan"
        # elif voice == 18:     #BROKEN use_phonemes
        #     return "vocoder_models/en/ljspeech/univnet"
        # elif voice == 19:     #BROKEN use_phonemes
        #     return "vocoder_models/en/blizzard2013/hifigan_v2"
        # elif voice == 20:     #BROKEN use_phonemes
        #     return "vocoder_models/en/vctk/hifigan_v2"
        # elif voice == 21:     #BROKEN use_phonemes
        #     return "vocoder_models/en/sam/hifigan_v2"
        # elif voice == 9:      #STUPID
        #     return "tts_models/en/vctk/fast_pitch"
        # elif voice == 7:           #BROKEN
        #     return "tts_models/en/multi-dataset/tortoise-v2"
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
