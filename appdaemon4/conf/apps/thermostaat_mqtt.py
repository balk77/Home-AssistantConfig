import appdaemon.plugins.hass.hassapi as hass

import requests

class thermostaat_mqtt(hass.Hass):
    def initialize(self):
        
        # self.listen_state(self.program_enable, "input_boolean.nefit_programma",new="on")

        # TIJDELIJK UIT:
        # self.listen_state(self.inputhandler, "sensor.wk_thermostaat_hass_sp")

        #self.listen_state(self.manualorclockmode, "input_boolean.nefit_disable_clock_mode")
        self.listen_state(self.nefit_disable_clock_mode, "input_boolean.nefit_disable_clock_mode", new="on")
        self.listen_state(self.nefit_enable_clock_mode, "input_boolean.nefit_disable_clock_mode", new="off")

        self.handle = self.listen_event(self.inputhandler_event, "call_service", domain = "climate", service = "set_temperature")


    def inputhandler_event(self, event_name, data, kwargs):
        # self.log("ping")
        entity_id = data['service_data']['entity_id']
        temperature = data['service_data']['temperature']
        # self.log(entity_id)
        # self.log(temperature)
        
        if entity_id == "climate.hc1":
            # self.log("ping")
            vakantie = self.get_state("input_boolean.vakantie")
            if vakantie == "off":
                self.run_in(self.temperatureset,0,temp_sp_hass=temperature)
            else:
                self.log("Vakantiemodus actief; thermostaat uitgeschakeld.")

    def inputhandler(self, entity, attribute, old, new, kwargs):
        self.log("ping")
        temp_sp_hass = float(self.get_state("sensor.wk_thermostaat_hass_sp"))
        vakantie = self.get_state("input_boolean.vakantie")
        if vakantie == "off":
            self.run_in(self.temperatureset,0,temp_sp_hass=temp_sp_hass)
        else:
            self.log("Vakantiemodus actief; thermostaat uitgeschakeld.")
    
    def temperatureset(self, kwargs):
        temp_sp_hass = float(kwargs["temp_sp_hass"])

        headers = {'Content-type': 'application/json'}
        #myurl = "http://127.0.0.1:8124"
        myurl = "http://192.168.0.9:8124"
        command1 = "/bridge/heatingCircuits/hc1/temperatureRoomManual"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"
        command3 = "/bridge/heatingCircuits/hc1/manualTempOverride/temperature"

        body1 = temp_sp_hass
        body2 = "on"
        body3 = temp_sp_hass
        # self.log("new setpoint & command:")
        # self.log(body1)
        # self.log(body2)
        # self.log(body3)

        #if(temp_sp_hass != temp_sp_thermostaat):

        r1 = requests.post(myurl+command1, verify=False, json={"value": body1}, headers = headers)
        # self.log(r1.status_code)
        # self.log("r1"+r1.text)

        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        # self.log(r2.status_code)
        # self.log("r2"+r2.text)

        r3 = requests.post(myurl+command3, verify=False, json={"value": body3}, headers = headers)
        # self.log(r3.status_code)
        # self.log("r3"+r3.text)

        self.call_service("input_boolean/turn_off", entity_id="input_boolean.nefit_programma")

        self.run_in(self.test_physical_thermostat, 60)

    def test_physical_thermostat(self, kwargs):
        desired_sp = float(self.get_state("sensor.wk_thermostaat_hass_sp"))
        try:
            actual_sp = float(self.get_state("sensor.current_set_temperature"))
        except:
            actual_sp = float(self.get_state("sensor.thermostaat_tempsetpoint"))
            
        # self.log("desired SP:")
        # self.log(desired_sp)
        # self.log("actual SP:")
        # self.log(actual_sp)

        if desired_sp != actual_sp:
            
            self.log("retry setting temperature")
            self.inputhandler(self,"x","x","x","x")
            #self.call_service("homeassistant/turn_off", entity_id=entity_id)




    def program_enable(self, entity, attribute, old, new, kwargs):

        headers = {'Content-type': 'application/json'}
        #myurl = "http://127.0.0.1:8124"
        myurl = "http://192.168.0.9:8124"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"

        body2 = "off"


        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        # self.log(r2.status_code)
        # self.log(r2.text)

    def nefit_disable_clock_mode(self, entity, attribute, old, new, kwargs):
        self.log("disabling clock mode")
        self.run_in(self.manualorclockmode, 0, body2="manual")
        self.run_in(self.temperatureset, 0, temp_sp_hass=15)

    def nefit_enable_clock_mode(self, entity, attribute, old, new, kwargs):
        self.log("enabling clock mode")
        self.run_in(self.manualorclockmode, 0, body2="clock")
        headers = {'Content-type': 'application/json'}
        #myurl = "http://127.0.0.1:8124"
        myurl = "http://192.168.0.9:8124"
        command2 = "/bridge/heatingCircuits/hc1/manualTempOverride/status"

        body2 = "off"


        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        # self.log(r2.status_code)
        # self.log(r2.text)

    def manualorclockmode(self, kwargs):

        #nefit_disable_clock_mode = self.get_state("input_boolean.nefit_disable_clock_mode")
        body2 = kwargs["body2"]

        # if nefit_disable_clock_mode == "off":
        #     body2 = "clock"
        # else:
        #     body2 = "manual"

        headers = {'Content-type': 'application/json'}
        #myurl = "http://127.0.0.1:8124"
        myurl = "http://192.168.0.9:8124"
        command2 = "/bridge/heatingCircuits/hc1/usermode"

        


        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        # self.log(r2.status_code)
        # self.log(r2.text)

#curl -XPOST http://19bridge/heatingCircuits/hc1/usermode -d '{"value":"manual"}' -H 'Content-Type: application/json'

# bij indrukken knop:
# 1. manualorclockmode = on
# 2. ingestelde temperatuur = 15
# Bij beweging:
# 1. manualorclockmode = off
# 2. program_enable  = true