import appdaemon.plugins.hass.hassapi as hass
import datetime
#import urllib.request
import requests

class thermostaatavond(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler1, "sensor.thermostaat_tempsetpoint")
        self.listen_state(self.inputhandler2, "group.woonkamer", new="off")

        # Run daily at 7pm

        # time = datetime.time(2, 0, 0)
        # self.run_daily(self.run_daily_c, runtime)

    def inputhandler1(self, entity, attribute, old, new, kwargs):
        temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        lights_woonkamer = self.get_state("group.woonkamer")
        thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
        now = datetime.datetime.now()
        maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")

        if (now.hour >= 20 or now.hour < 2 ):
            avond = 1
        else:
            avond = 0

        if (temp_sp < 15.1 and avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "on"):
            self.set_value("input_number.hass_tempsetpoint",maxtempsetpoint)


    def inputhandler2(self, entity, attribute, old, new, kwargs):
        # Zet verwarming uit wanneer lichten uit gaan tussen 20:00 en 2:00
        temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        lights_woonkamer = self.get_state("group.woonkamer")
        thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
        now = datetime.datetime.now()
        maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")



        if (now.hour >= 20 or now.hour < 2 ):
            avond = 1
        else:
            avond = 0

        if (avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "off"):
            self.set_value("input_number.hass_tempsetpoint",15)
            self.set_state("input_boolean.huis_slaapstand", state="on")
            self.set_state("input_boolean.iftt_temp_triggered", state="on")
            self.set_value("input_number.iftt_temp_triggered_sp", 15)
