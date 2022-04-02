import rospy
from vectordrive.msg import thrusterPercents
from rocon_std_msgs.msg import StringArray

#Publishers
rospy.init_node('thruster_tester')
horiz_pub = rospy.Publisher('rov/cmd_horizontal_vdrive', thrusterPercents, queue_size=1)
vert_pub = rospy.Publisher('rov/cmd_vertical_vdrive', thrusterPercents, queue_size=1)

#Keyboard Sub and Callback
def keyCallback(data):
    if data.data <= 4:
        thrusterHList[data.data - 1] = abs(thrusterHList[data.data - 1] - 100)
    if data.data >= 5:
        thrusterVList[data.data - 5] = abs(thrusterVList[data.data - 5] - 100)

#Subscribers
teleop_sub = rospy.Subscriber('rov/thruster_testing', StringArray, keyCallback)

def main():

    #Create the horizontal and vertical messages
    thrusterVValues = thrusterPercents()
    thrusterHValues = thrusterPercents()

    #These lists store the values that will be assigned to the messages and published
    thrusterHList = [0, 0, 0, 0]
    thrusterVList = [0, 0, 0, 0]

    while True:
        #Update the thruster values
        thrusterHValues.t1 = thrusterHList[0]
        thrusterHValues.t2 = thrusterHList[1]
        thrusterHValues.t3 = thrusterHList[2]
        thrusterHValues.t4 = thrusterHList[3]

        thrusterVValues.t1 = thrusterVList[0]
        thrusterVValues.t2 = thrusterVList[1]
        thrusterVValues.t3 = thrusterVList[2]
        thrusterVValues.t4 = thrusterVList[3]

        #Publish the updated thruster values
        horiz_pub.publish(thrusterHValues)
        vert_pub.publish(thrusterVValues)
if __name__ == "__main__":
    main()
