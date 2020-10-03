import appdaemon.plugins.hass.hassapi as hass
import datetime
import requests

class thermostaatavond(hass.Hass):
    def initialize(self):
        self.listen_state(self.switchon, "sensor.thermostaat_tempsetpoint")
        self.listen_state(self.switchoff, "group.woonkamer", new="off")
        self.listen_state(self.switchoff, "input_boolean.huis_slaapstand", new="on")
                 

    def switchon(self, entity, attribute, old, new, kwargs):
        if self.now_is_between("20:00:00", "02:00:00"):
            avond = 1

            self.log("avond: ")
            self.log(avond)

            # maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")
            maxtempsetpoint = self.get_state("input_number.max_temperature_setpoint")
            nefit_disable_clock_mode = self.get_state("input_boolean.nefit_disable_clock_mode")
            temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
            lights_woonkamer = self.get_state("group.woonkamer")
            thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram") 
            huis_slaapstand = self.get_state("input_boolean.huis_slaapstand") 


            # if (temp_sp < 15.1 and thermostaat_activeprogram == "0" and lights_woonkamer == "on" and nefit_disable_clock_mode == "off"):
            if (temp_sp < 15.1  and huis_slaapstand == "off" and nefit_disable_clock_mode == "off"):
                self.log("setting temperature to: " + maxtempsetpoint)
                self.call_service("climate/set_temperature", entity_id="climate.hc1", temperature=maxtempsetpoint)
                
        else:
            avond = 0


    def switchoff(self, entity, attribute, old, new, kwargs):
        # Zet verwarming uit wanneer lichten uit gaan tussen 20:00 en 2:00
        if self.now_is_between("20:00:00", "02:00:00"):
            avond = 1
            # lights_woonkamer = self.get_state("group.woonkamer")
            # thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
            # if (thermostaat_activeprogram == "0" and lights_woonkamer == "off"):
            
            payload = 15
            self.call_service("climate/set_temperature", entity_id="climate.hc1", temperature=payload)
        else:
            avond = 0

        
