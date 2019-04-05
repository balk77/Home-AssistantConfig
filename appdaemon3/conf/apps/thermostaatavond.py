import appdaemon.plugins.hass.hassapi as hass
import datetime
#import urllib.request
import requests

class thermostaatavond(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler1, "sensor.thermostaat_tempsetpoint")
        self.listen_state(self.inputhandler2, "group.woonkamer", new="off")

        

    def inputhandler1(self, entity, attribute, old, new, kwargs):
        
        temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        lights_woonkamer = self.get_state("group.woonkamer")
        thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
        now = datetime.datetime.now()
        maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")

        nefit_disable_clock_mode = self.get_state("input_boolean.nefit_disable_clock_mode")

        if (now.hour >= 20 or now.hour < 2 ):
            avond = 1
        else:
            avond = 0

        if (temp_sp < 15.1 and avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "on" and nefit_disable_clock_mode == "off"):
            self.call_service("mqtt/publish", topic="woonkamer/woonkamer/thermostaat/temperature/set", payload=maxtempsetpoint, retain=True)

    def inputhandler2(self, entity, attribute, old, new, kwargs):
        # Zet verwarming uit wanneer lichten uit gaan tussen 20:00 en 2:00
        lights_woonkamer = self.get_state("group.woonkamer")
        thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
        now = datetime.datetime.now()
        
        if (now.hour >= 20 or now.hour < 2 ):
            avond = 1
        else:
            avond = 0

        if (avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "off"):
            payload = 15
            self.call_service("mqtt/publish", topic="woonkamer/woonkamer/thermostaat/temperature/set", payload=payload, retain=True)
            
            
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.huis_slaapstand")
            
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.iftt_temp_triggered")
            self.call_service("input_number/set_value", entity_id="input_number.iftt_temp_triggered_sp", value=15)
