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
        return 1

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
    else:
        return "boot-config/animations/poseInit"

