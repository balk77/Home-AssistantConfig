import appdaemon.appapi as appapi
import time
from babel.numbers import format_number, format_decimal


class wasserdroger(appapi.AppDaemon):
    def initialize(self):
        self.listen_state(self.inputhandler, self.args["trigger"], old="off", new="on")
        self.listen_state(self.inputhandler, self.args["trigger"], old="on", new="off")

    def inputhandler(self, entity, attribute, old, new, kwargs):

        action = self.get_state(self.args["trigger"])
        self.log(action)

        kwh = self.get_state(self.args["kwhsensor"])
        timestamp = str(round(time.time()))
        appliance = self.args["appliance"]

        path = '/home/sander/'+appliance+'.csv'
        f = open(path,'a')
        #self.log(timestamp+";"+str(format_decimal(kwh, locale='de'))+";"+appliance+" "+self.action+"\n")
        self.log("action schrijf:")

        f.write(timestamp+";"+str(format_decimal(kwh, locale='de'))+";"+appliance+" "+action+"\n")
        f.close()
