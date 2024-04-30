import time
# from pepper_robot.robot import *
# import pepper_robot.config
import qi
import sys
import csv
import execnet
import os
# import playsound


sys.path.insert(1, os.path.realpath(os.path.pardir))

def call_python_version(Version, Module, Function, ArgumentList):
    gw = execnet.makegateway("popen//python=python%s" % Version)
    channel = gw.remote_exec("""
        from %s import %s as the_function
        channel.send(the_function(*channel.receive()))
    """ % (Module, Function))
    channel.send(ArgumentList)
    return channel.receive()

from gesturesConfig import *
# from playFile import *

# to find PEPPER_IP & PEPPER_PORT
from config import *

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


def main(session):
    # setup CIIRC Pepper API qi wrapper
    # pepper = Pepper(PEPPER_IP, PEPPER_PORT)

    behavior_service = session.service("ALBehaviorManager")
    audio_player_service = session.service("ALAudioPlayer")
    # behavior_service.runBehavior(get_behavior_name('init'), _async=False)  # _async is False = wait for finish

    # print "in main"  # TEMP

    init_time = time.time()     #TEMP
    with open("../outputs/commandFile.csv", 'r') as file:
        file_reader = csv.reader(file)
        line_number = 0     # line number incrementer for file name
        current_time = 0.0
        # print "before file reader" # TEMP
        behavior_service.runBehavior(get_behavior_name('init'),_async=False)  # _async is False = wait for finish
        for row in file_reader:   # for each script line
            if line_number == 0: #skips the header row of csv
                line_number += 1
                continue

            while current_time < float(row[0]):
                current_time = time.time() - init_time
                # print("Current time: " + str(current_time))     # TEMP

            if row[1].find('.wav') != -1: #if current row is a voice file, play sound
                behavior_service.runBehavior(get_behavior_name('init'), _async=False)  # _async is False = wait for finish
                file_name = '../outputs/' + row[1]
                # print("Current Time: " + str(current_time) + "\tFile Name: " + str(file_name))      #TEMP
                call_python_version("3.9", "playFile", "play", [file_name, False])      # play the sound before gestures, (True means wait)
            else:   #if current row is a gesture, play 'init' then gesture, then 'init'
                # behavior_service.runBehavior(get_behavior_name('init'), _async=False)  # _async is False = wait for finish
                behavior_service.runBehavior(get_behavior_name(row[1]), _async=False)  # _async is False = wait for finish
                # behavior_service.runBehavior(get_behavior_name('init'), _async=False)  # _async is False = wait for finish
                # current_time += get_gesture_length(row[1])
            line_number += 1    # line number increment for file name
    behavior_service.runBehavior(get_behavior_name('init'), _async=False)  #    _async is False = wait for finish


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