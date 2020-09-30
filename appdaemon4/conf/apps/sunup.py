import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
#
# Hellow World App
#
# Args:
#

class sunup(hass.Hass):

    def initialize(self):
        self.log("Hello from AppDaemon")
        # self.run_every(self.inputhandler,datetime.datetime.now(),10)
        now = datetime.datetime.now()
        now_offset = now + datetime.timedelta(seconds=2)
        self.run_every(self.inputhandler,now_offset,60)

        self.log(datetime.datetime.now().hour)
        self.log(datetime.datetime.now().strftime("%H:%M:%S"))


        

    def inputhandler(self, kwargs):

        if self.sunrise() > self.sunset():
          sunup_custom = True
          sundown_custom = False
        else:
          sunup_custom = False
          sundown_custom = True
        
        # self.log("sunup_custom: "+str(sunup_custom))
        # self.log("AD API sun_up: "+str(self.sun_up()))

        path = '/conf/sunup.csv'
        f = open(path,'a')
        timestamp = str(round(time.time()))
        timestamp = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        

        f.write(timestamp+";"+str(sunup_custom)+";"+str(sundown_custom)+";"+str(self.sun_up())+";"+str(self.sun_down())+";"+str(self.sunrise())+";"+str(self.sunset())+"\n")
        f.close()
      
      
        #   self.log(data)
        #   # self.log(data['service_data']['entity_id'])
        #   entity_id = data['service_data']['entity_id']
        #   temperature = data['service_data']['temperature']
        #   self.log(entity_id)
        #   self.log(temperature)
      


