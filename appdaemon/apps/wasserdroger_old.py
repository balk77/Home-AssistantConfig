import appdaemon.appapi as appapi
import time
from babel.numbers import format_number, format_decimal




class wasserdroger(appapi.AppDaemon):
    def initialize(self):
        # Listen for state change of ventilation requirements

        #self.listen_state(self.washer_pwrup, "sensor.washer_pwrup", old=False, new=True, action="on", appliance="washer")
        #self.listen_state(self.washer_pwrup, "sensor.washer_pwrup", old=True, new=False, action="off", appliance="washer")
        self.listen_state(self.inputhandler, self.args["trigger"])
        #self.listen_state(self.washer_pwrup, "input_boolean.wasser_test", "on", "off", action="off", appliance="washer")
        self.log("lalala "+self.args["trigger"])



    def inputhandler(self, entity, attribute, old, new, kwargs):
        delay = 180
        if self.get_state(self.args["trigger"]) == True:
            self.action = "on"
        else:
            self.action = "off"
        #self.action = self.get_state(self.args["trigger"])
        self.appliance = self.args["appliance"]
        self.log(self.appliance + " gaat: " + self.action)
        self.log(self.action)

        self.run_in(self.actionhandler, delay)


    def actionhandler(self, kwargs):
        appliance = self.args["appliance"]
        kwh = self.get_state(self.args["kwhsensor"])
        timestamp = str(round(time.time()))

        path = '/home/sander/'+appliance+'.csv'
        f = open(path,'a')
        #self.log(timestamp+";"+str(format_decimal(kwh, locale='de'))+";"+appliance+" "+self.action+"\n")

        f.write(timestamp+";"+str(format_decimal(kwh, locale='de'))+";"+appliance+" "+self.action+"\n")
        f.close()

        self.log(self.appliance)
        status = self.set_state("input_boolean."+appliance+"_switch", state = self.action)


        if self.action == "off":
            message = self.args["message"]
            status = self.call_service("notify/pushbullet", message=message, target="device/Nexus5X")
