#!/usr/bin/python
import sys
from PyQt4.QtGui import *
from functools import partial
import yaml 
import rospy
from std_msgs.msg import String

# load the yaml file
with open('yaml_example.yaml', 'r') as stream:
    datamap = yaml.safe_load(stream)

# create ros publisher and initiate node
pub = rospy.Publisher('inputs', String, queue_size=10, latch=True)
rospy.init_node('inputs')

# convert the directory in yaml file to an object
class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

s = Struct(**datamap)
input_button_Number = len(s.inputs) # number of the input buttons = number of items under inputs directory
output_button_Number = len(s.outputs) # number of the output buttons = number of items under outputs directory
input_button_Name = []
output_button_Name = []

# add the string under the node directory to the array of the button names
for catagory in s.inputs:
    input_button_Name.append(s.inputs[catagory]['node'])

for catagory in s.outputs:
    output_button_Name.append(s.outputs[catagory]['node'])

# class of the gui
class ButtonGui(QWidget):

    input_buttons = []
    output_buttons = []
   
    def __init__(self):
        super(QWidget,self).__init__()

        self.init_UI()


    def init_UI(self): 
        for x in range(0, input_button_Number):
            self.input_buttons.append(QPushButton(input_button_Name[x],self)) # create QPushButtons with names specified in the yaml file
            self.input_buttons[x].setStyleSheet("background-color: red") 
            self.input_buttons[x].setCheckable(True) # set the button to checkable button
            self.input_buttons[x].move(10, 30 + 50 * x) # set the position of the button 
            self.input_buttons[x].clicked[bool].connect(partial(self.set_color, x)) # connect the event of clicking button to the call back function (change color and publish status)

        for x in range (0, output_button_Number):
             self.output_buttons.append(QPushButton(output_button_Name[x],self))
             self.output_buttons[x].move(200, 30 + 50 * x)
        
        
        self.setGeometry(500, 300, 400, 300)
        self.setWindowTitle('Status')    
        self.label1 = QLabel(self)
        self.label1.move(15,5)
        self.label1.setText('inputs')
        self.label2 = QLabel(self)
        self.label2.move(215,5)
        self.label2.setText('outputs')
        self.show()

    def set_color(self, n):
        if self.input_buttons[n].isChecked() == True:
            self.input_buttons[n].setStyleSheet("background-color: green")
            '''print(input_button_Name[n]+' is on')'''
            pub.publish(input_button_Name[n]+' is on')
        if self.input_buttons[n].isChecked() == False:
            self.input_buttons[n].setStyleSheet("background-color: red")
            '''print(input_button_Name[n]+' is off')'''
            pub.publish(input_button_Name[n]+' is off')
 
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = ButtonGui()
    sys.exit(app.exec_())

