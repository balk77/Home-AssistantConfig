import appdaemon.plugins.hass.hassapi as hass

import requests

class thermostaat_mqtt(hass.Hass):
    def initialize(self):
        
        self.listen_state(self.program_enable, "input_boolean.nefit_programma",new="on")
        self.listen_state(self.inputhandler, "sensor.wk_thermostaat_hass_sp")



    def inputhandler(self, entity, attribute, old, new, kwargs):
        self.log("ping")
        temp_sp_hass = float(self.get_state("sensor.wk_thermostaat_hass_sp"))

        headers = {'Content-type': 'application/json'}
        #myurl = "http://127.0.0.1:8124"
        myurl = "http://192.168.0.194:8124"
        command1 = "/bridge/heatingCircuits/hc1/temperatureRoomManual"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"
        command3 = "/bridge/heatingCircuits/hc1/manualTempOverride/temperature"

        body1 = temp_sp_hass
        body2 = "on"
        body3 = temp_sp_hass
        self.log("new setpoint & command:")
        self.log(body1)
        self.log(body2)

        #if(temp_sp_hass != temp_sp_thermostaat):

        r1 = requests.post(myurl+command1, verify=False, json={"value": body1}, headers = headers)
        self.log(r1.status_code)
        self.log(r1.text)

        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        self.log(r2.status_code)
        self.log(r2.text)

        r3 = requests.post(myurl+command3, verify=False, json={"value": body3}, headers = headers)
        self.log(r3.status_code)
        self.log(r3.text)

        self.call_service("input_boolean/turn_off", entity_id="input_boolean.nefit_programma")

        #self.set_state("input_boolean.nefit_programma", state="off")

        self.run_in(self.test_physical_thermostat, 60)

    def test_physical_thermostat(self, kwargs):
        desired_sp = float(self.get_state("sensor.wk_thermostaat_hass_sp"))
        actual_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        self.log("desired SP:")
        self.log(desired_sp)
        self.log("actual SP:")
        self.log(actual_sp)

        if desired_sp != actual_sp:
            
            self.log("retry setting temperature")
            self.inputhandler(self,"x","x","x","x")
            #self.call_service("homeassistant/turn_off", entity_id=entity_id)




    def program_enable(self, entity, attribute, old, new, kwargs):

        headers = {'Content-type': 'application/json'}
        #myurl = "http://127.0.0.1:8124"
        myurl = "http://192.168.0.194:8124"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"

        body2 = "off"


        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        self.log(r2.status_code)
        self.log(r2.text)


