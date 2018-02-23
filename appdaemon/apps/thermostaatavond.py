import appdaemon.appapi as appapi
import datetime
#import urllib.request
import requests

class thermostaatavond(appapi.AppDaemon):
    def initialize(self):
        self.listen_state(self.inputhandler1, "sensor.thermostaat_tempsetpoint")
        self.listen_state(self.inputhandler2, "group.woonkamer", new="off")

    def inputhandler1(self, entity, attribute, old, new, kwargs):
        temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        lights_woonkamer = self.get_state("group.woonkamer")
        thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
        now = datetime.datetime.now()
        maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")



        headers = {'Content-type': 'application/json'}
        myurl = "http://127.0.0.1:8124"
        command1 = "/bridge/heatingCircuits/hc1/temperatureRoomManual"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"
        command3 = "/bridge/heatingCircuits/hc1/manualTempOverride/temperature"




        if (now.hour >= 20 or now.hour < 2 ):
            avond = 1
        else:
            avond = 0

        if (temp_sp < 15.1 and avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "on"):
            body1 = maxtempsetpoint
            body2 = "on"
            body3 = maxtempsetpoint

            r1 = requests.post(myurl+command1, verify=False, json={"value": body1}, headers = headers)
            self.log(r1.status_code)
            self.log(r1.text)

            r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
            self.log(r2.status_code)
            self.log(r2.text)

            r3 = requests.post(myurl+command3, verify=False, json={"value": body3}, headers = headers)
            self.log(r3.status_code)
            self.log(r3.text)

            self.set_state("input_boolean.iftt_temp_triggered, state="on")

    def inputhandler2(self, entity, attribute, old, new, kwargs):
        temp_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        lights_woonkamer = self.get_state("group.woonkamer")
        thermostaat_activeprogram = self.get_state("sensor.thermostaat_activeprogram")
        now = datetime.datetime.now()
        maxtempsetpoint = self.get_state("sensor.maxtempsetpoint")



        headers = {'Content-type': 'application/json'}
        myurl = "http://127.0.0.1:8124"
        command1 = "/bridge/heatingCircuits/hc1/temperatureRoomManual"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"
        command3 = "/bridge/heatingCircuits/hc1/manualTempOverride/temperature"




        if (now.hour >= 20 or now.hour < 2 ):
            avond = 1
        else:
            avond = 0

        if (avond == 1 and thermostaat_activeprogram == "0" and lights_woonkamer == "off"):
            body1 = 15
            body2 = "on"
            body3 = 15

            r1 = requests.post(myurl+command1, verify=False, json={"value": body1}, headers = headers)
            self.log(r1.status_code)
            self.log(r1.text)

            r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
            self.log(r2.status_code)
            self.log(r2.text)

            r3 = requests.post(myurl+command3, verify=False, json={"value": body3}, headers = headers)
            self.log(r3.status_code)
            self.log(r3.text)

            self.set_state("input_boolean.huis_slaapstand", state="on")
            self.set_state("input_boolean.iftt_temp_triggered, state="on")
            self.set_state("input_number.iftt_temp_triggered_sp, state="15")
