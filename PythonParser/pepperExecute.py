import time

from pepper_robot.robot import *
import pepper_robot.config
import qi
import naoqi
import sys
import fileinput
import csv
from main import get_gesture_length
PEPPER_PORT = 9559
PEPPER_IP = '192.168.50.155'


def run_behavior(ip, port, behavior_name):
    sesh = qi.Session()
    try:
        sesh.connect("tcp://" + ip + ":" + str(port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + ip + "\" on port " + str(port) + ".\nPlease check your script "
                                                                                    "arguments. Run with -h option "
                                                                                    "for help.")
        sys.exit(1)

    behavior_mng_service = sesh.service("ALBehaviorManager")
    getBehaviors(behavior_mng_service)
    launchAndStopBehavior(behavior_mng_service, behavior_name)
    defaultBehaviors(behavior_mng_service, behavior_name)


def getBehaviors(behavior_mng_service):
    """
    Know which behaviors are on the robot.
    """
    names = behavior_mng_service.getInstalledBehaviors()
    print ("Behaviors on the robot:")
    print (names)
    names = behavior_mng_service.getRunningBehaviors()
    print ("Running behaviors:")
    print (names)


def launchAndStopBehavior(behavior_mng_service, behavior_name):
    """
    Launch and stop a behavior, if possible.
    """
    # Check that the behavior exists.
    if behavior_mng_service.isBehaviorInstalled(behavior_name):
        # Check that it is not already running.
        if not behavior_mng_service.isBehaviorRunning(behavior_name):
            # Launch behavior. This is a blocking call, use _async=True if you do not
            # want to wait for the behavior to finish.
            behavior_mng_service.runBehavior(behavior_name, _async=True)
            time.sleep(0.5)
        else:
            print ("Behavior is already running.")
    else:
        print ("Behavior not found.")

    names = behavior_mng_service.getRunningBehaviors()
    print ("Running behaviors:")
    print (names)

    # Stop the behavior.
    if behavior_mng_service.isBehaviorRunning(behavior_name):
        behavior_mng_service.stopBehavior(behavior_name)
        time.sleep(1.0)
    else:
        print ("Behavior is already stopped.")
    names = behavior_mng_service.getRunningBehaviors()
    print ("Running behaviors:")
    print (names)


def defaultBehaviors(behavior_mng_service, behavior_name):
    """
    Set a behavior as default and remove it from default behavior.
    """
    # Get default behaviors.
    names = behavior_mng_service.getDefaultBehaviors()
    print ("Default behaviors:")
    print (names)
    # Add behavior to default.
    behavior_mng_service.addDefaultBehavior(behavior_name)
    names = behavior_mng_service.getDefaultBehaviors()
    print ("Default behaviors:")
    print (names)
    # Remove behavior from default.
    behavior_mng_service.removeDefaultBehavior(behavior_name)
    names = behavior_mng_service.getDefaultBehaviors()
    print ("Default behaviors:")
    print (names)


# RETURNS the pepper stored behavior file from a table according to gesture name
def get_behavior_name(gesture):
    if gesture == "wave":
        return "dancemoves-a0f94b/Wave and bow"
    elif gesture == "shocked":
        return "animations/Stand/Emotions/Negative/Shocked_1"

def main(session):
    # setup CIIRC Pepper API qi wrapper
    pepper = Pepper(PEPPER_IP, PEPPER_PORT)

    # Testing Below
    tts = session.service("ALTextToSpeech")
    behavior_service = session.service("ALBehaviorManager")
    audio_player_service = session.service("ALAudioPlayer")

    with open("outputs/voices.csv", 'r') as vf, open("outputs/gestures.csv", 'r') as gf:
        voice_reader = csv.reader(vf)
        gesture_reader = csv.reader(gf)
        line_number = 1
        for row_v, row_g in voice_reader, gesture_reader:   # for each script line
            pepper.upload_file('outputs/' + 'line' + str(line_number) + '.mp3')     # scp upload
            fileId = audio_player_service.loadFile('outputs/' + 'line' + str(line_number) + '.mp3')
            if len(row_v) == 1:     # if voice is longer than gesture
                # pepper.play_sound('line' + str(line_number) + '.mp3')
                audio_player_service.play(fileId, _async=True)
                for i in row_g:
                    if row_g[i].replace('.', '', 1).isdigit():    # if gesture column is a delay
                        time.sleep(row_g[i])
                    else:
                        behavior_service.runBehavior(get_behavior_name(row_g[i]), _async=False)  # _async is False = wait for finish
                        behavior_service.stopBehavior(get_behavior_name(row_g[i]))
            else:    # if gesture is longer than voice
                behavior_service.runBehavior((get_gesture_length(row_g[0])), _async=False)
                behavior_service.stopBehavior(get_behavior_name(row_g[0]))
                if row_v[0] > get_gesture_length(row_g[0]):     # if the first gesture is shorter than voice delay
                    time.sleep(row_v[0] - get_gesture_length(row_g[0]))     # sleeps the difference in delay
                # pepper.play_sound('line' + str(line_number) + '.mp3')
                audio_player_service.play(fileId, _async=True)
                if len(row_g) > 1:   # the next gestures
                    for i in row_g:
                        if row_g[i+1].replace('.', '', 1).isdigit():    # if is delay
                            time.sleep(row_g[i + 1])
                        else:  # if is behavior
                            behavior_service.runBehavior(get_behavior_name(row_g[i + 1]), _async=False)
                            behavior_service.stopBehavior(get_behavior_name(row_g[i + 1]))
            line_number += 1


    # tts.say(text)
    # behavior_mng_service = session.service("ALBehaviorManager")
    # if gestures[0] == "wave":
    #     run_behavior(PEPPER_IP, PEPPER_PORT, "dancemoves-a0f94b/Wave and bow")
    #     time.sleep(11.0)
    #     behavior_mng_service.stopBehavior("dancemoves-a0f94b/Wave and bow")
    # elif gestures[0] == "shocked":
    #     run_behavior(PEPPER_IP, PEPPER_PORT, "animations/Stand/Emotions/Negative/Shocked_1")
    #     time.sleep(4.5)
    #     behavior_mng_service.stopBehavior("animations/Stand/Emotions/Negative/Shocked_1")
    # run_behavior(PEPPER_IP, PEPPER_PORT, "boot-config/animations/poseInitUp")
    # time.sleep(1.2)
    # run_behavior(PEPPER_IP, PEPPER_PORT, "boot-config/animations/poseInitUp")
    #
    # pepper.play_sound(output_file)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    session = qi.Session()
    try:
        session.connect("tcp://" + PEPPER_IP + ":" + str(PEPPER_PORT))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + PEPPER_IP + "\" on port " + str(PEPPER_PORT) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)