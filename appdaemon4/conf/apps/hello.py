import appdaemon.plugins.hass.hassapi as hass
import datetime
#
# Hellow World App
#
# Args:
#

class HelloWorld(hass.Hass):

    def initialize(self):
        self.log("Hello from AppDaemon")

        # dimtime = datetime.time(8, 50, 0)
        
        # self.run_daily(self.changesetting, dimtime,node_id=14,parameter=19,value=0)


    def changesetting(self, kwargs):
        #self.log("setting parameter")
        # self.call_service("zwave/set_config_parameter", node_id=kwargs["node_id"],parameter=kwargs["parameter"],value=kwargs["value"])
        topic = "OpenZWave/1/command/setvalue/"
        payload = '{ "ValueIDKey": 5348024920047633, "Value":'+str(kwargs["value"])+'}'
        self.call_service("mqtt/publish", topic=topic, payload=payload)
    
    

        # payload = '{ "ValueIDKey": 5348024785829905, "Value":'+str(value)+'}'
        # # payload = '{ "ValueIDKey": 5348024785829905, "Value":10}'
        # self.log(payload)
        # self.call_service("mqtt/publish", topic=topic, payload=payload)


    #     self.listen_state(self.inputhandler, "light.wk_eettafel_plafond_level", old = "off", new = "on")
    #     self.listen_state(self.inputhandler, "input_boolean.test_2")
    #     dimtime = datetime.time(0, 0, 1)
    #     brighttime = datetime.time(7, 0, 0)
    #     self.run_daily(self.changesetting, dimtime,node_id=13,parameter=19,value=4)
    #     self.run_daily(self.changesetting, brighttime,node_id=13,parameter=19,value=99)


    #     fetch_sunriseset_time = datetime.time(19, 2, 0)
    #     self.run_daily(self.fetch_sunriseset, fetch_sunriseset_time)
    #     self.fetch_sunriseset(1)

          
        

    # def fetch_sunriseset(self, kwargs):
    #     self.sunrise_custom = self.sunrise().strftime("%H:%M:%S")
    #     self.sunset_custom = self.sunset().strftime("%H:%M:%S")


    # def changesetting(self, kwargs):
    #     #self.log("setting parameter")
    #     self.call_service("zwave/set_config_parameter", node_id=kwargs["node_id"],parameter=kwargs["parameter"],value=kwargs["value"])



    # def inputhandler(self, entity, attribute, old, new, kwargs):
    #     # now = datetime.datetime.now()
    #     workday_sensor = self.get_state("binary_sensor.workday_sensor")
