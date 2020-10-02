import appdaemon.plugins.hass.hassapi as hass
import datetime
#import urllib.request
import requests

class thermostaatavond(hass.Hass):
    def initialize(self):
        self.listen_state(self.switchon, "sensor.thermostaat_tempsetpoint")
        self.listen_state(self.switchoff, "group.woonkamer", new="off")
        # self.switchon(self,self,self,self,self)

        

    def switchon(self, entity, attribute, old, new, kwargs):
        # self.log("ping")
        
        # now = datetime.datetime.now()

        # if (now.hour >= 20 or now.hour < 2 ):
        if self.now_is_between("20:00:00", "02:00:00"):
            avond = 1

            self.log("avond: ")
            self.log(avond)

            maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")
            nefit_disable_clock_mode = self.get_state("input_boolean.nefit_disable_clock_mode")
            temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
            lights_woonkamer = self.get_state("group.woonkamer")
            thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram") 

            if (temp_sp < 15.1 and thermostaat_activeprogram == "0" and lights_woonkamer == "on" and nefit_disable_clock_mode == "off"):
                self.log("setting temperature to: " + maxtempsetpoint)
                self.call_service("climate/set_temperature", entity_id="climate.hc1", temperature=maxtempsetpoint)
                # self.call_service("mqtt/publish", topic="woonkamer/woonkamer/thermostaat/temperature/set", payload=maxtempsetpoint, retain=True)
        else:
            avond = 0

        # if (temp_sp < 15.1 and avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "on" and nefit_disable_clock_mode == "off"):
        #     self.log("setting temperature to:" + maxtempsetpoint)
        #     self.call_service("mqtt/publish", topic="woonkamer/woonkamer/thermostaat/temperature/set", payload=maxtempsetpoint, retain=True)

    def switchoff(self, entity, attribute, old, new, kwargs):
        # Zet verwarming uit wanneer lichten uit gaan tussen 20:00 en 2:00
        
        # now = datetime.datetime.now()
        
        # if (now.hour >= 20 or now.hour < 2 ):
        if self.now_is_between("20:00:00", "02:00:00"):
            avond = 1
            lights_woonkamer = self.get_state("group.woonkamer")
            thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
            if (thermostaat_activeprogram == "0" and lights_woonkamer == "off"):
                payload = 15
                self.call_service("climate/set_temperature", entity_id="climate.hc1", temperature=payload)
                # self.call_service("mqtt/publish", topic="woonkamer/woonkamer/thermostaat/temperature/set", payload=payload, retain=True)
            
            
                self.call_service("input_boolean/turn_on", entity_id="input_boolean.huis_slaapstand")
            
                # self.call_service("input_boolean/turn_on", entity_id="input_boolean.iftt_temp_triggered")
                # self.call_service("input_number/set_value", entity_id="input_number.iftt_temp_triggered_sp", value=15)
        else:
            avond = 0

        
