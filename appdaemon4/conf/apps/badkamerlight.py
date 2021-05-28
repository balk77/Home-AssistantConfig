import appdaemon.plugins.hass.hassapi as hass
import datetime
import time



class badkamerlight(hass.Hass):
    def initialize(self):
        
        # self.listen_state(self.inputhandler, "light.badkamer_plafond_level", old = "off", new = "on")
        self.listen_state(self.inputhandler, "light.badkamer_plafond_level", old = "off", new = "on")
        # self.listen_state(self.inputhandler, "light.wk_eettafel_plafond_level", old = "off", new = "on")

        
        dimtime = datetime.time(0, 0, 1)
        brighttime = datetime.time(7, 0, 0)
        self.run_daily(self.changesetting, dimtime,value=4)
        self.run_daily(self.changesetting, brighttime,value=99)


        fetch_sunriseset_time = datetime.time(19, 2, 0)
        self.run_daily(self.fetch_sunriseset, fetch_sunriseset_time)
        self.fetch_sunriseset(1)

        # self.run_in(self.changesetting, 1,value=17)

        
        

    def fetch_sunriseset(self, kwargs):
        self.sunrise_custom = self.sunrise().strftime("%H:%M:%S")
        self.sunset_custom = self.sunset().strftime("%H:%M:%S")


    # def changesetting(self, kwargs):
    def changesetting(self, value):
        # self.log("jaja")
        
        value = value['value']
        # self.log(str(value))
        # self.call_service("zwave/set_config_parameter", node_id=kwargs["node_id"],parameter=kwargs["parameter"],value=kwargs["value"])
        # value
        #OpenZW Beta
        topic = "OpenZWave/1/command/setvalue/"
        payload = '{ "ValueIDKey": 5348024785829905, "Value":'+str(value)+'}'
        self.call_service("mqtt/publish", topic=topic, payload=payload)

        # Zwave JS2MQTT
        topic = "zwavejsmqtt/_CLIENTS/ZWAVE_GATEWAY-zwavejs2mqtt/api/writeValue/set"
        payload = '{ "args":[{"nodeId":13, "commandClass":112, "endpoint":0, "property":19},'+str(value)+']}'
        # self.call_service("mqtt/publish", topic=topic, payload=payload)
        parameter="Forced switch on brightness level"
        entity_id="light.badkamer_plafond_level"
        self.call_service("zwave_js/set_config_parameter", entity_id=entity_id, parameter=parameter, value=value)



    def inputhandler(self, entity, attribute, old, new, kwargs):
        # now = datetime.datetime.now()
        workday_sensor = self.get_state("binary_sensor.workday_sensor")
        douchecounter = float(self.get_state("counter.douches"))

        # self.setlight(brightness=26, transition=0)
        # self.run_in(self.setlightfade, 20, brightness=255, transition=30)

        if self.now_is_between(self.sunrise_custom, self.sunset_custom):
            sundown = False
            sunup = True
        
        else:
            sundown = True
            sunup = False
            
        
        # self.log(sundown)

        if workday_sensor == "on" and self.now_is_between("0:00:00", "05:00:00"):
            self.setlight(brightness=26, transition=0)
            self.run_in(self.changesetting, 1, value=10)
        elif workday_sensor == "off" and self.now_is_between("0:00:00", "07:00:00"):
            self.setlight(brightness=26, transition=0)
            self.run_in(self.changesetting, 1, value=10)
        # test of Linda en Sander beiden gedoucht hebben
        elif douchecounter < 2:
            if workday_sensor == "on" and self.now_is_between("5:00:00", "08:00:00"):
                # self.log("wd=on, between 0->8, douchecounter < 2")
                self.setlight(brightness=26, transition=0)
                self.run_in(self.setlightfade, 20, brightness=255, transition=30)
                self.run_in(self.changesetting, 1,value=10)
            elif workday_sensor == "on" and sundown and self.now_is_between("8:00:00", "11:00:00"):
                # self.log("wd=on, between 8->11, douchecounter < 2, sundown")
                self.setlight(brightness=26, transition=0)
                self.run_in(self.setlightfade, 20, brightness=255, transition=30)
                self.run_in(self.changesetting, 1,value=10)
            elif workday_sensor == "off" and sundown and self.now_is_between("7:00:00", "11:00:00"):
                # self.log("wd=off, between 7->11, douchecounter < 2")
                self.setlight(brightness=26, transition=0)
                self.run_in(self.setlightfade, 20, brightness=255, transition=30)
                self.run_in(self.changesetting, 1,value=10)
            elif workday_sensor == "off" and sunup and self.now_is_between("7:00:00", "9:00:00"):
                # self.log("wd=off, between 7->9, douchecounter < 2, sunup")
                self.setlight(brightness=26, transition=0)
                self.run_in(self.setlightfade, 2, brightness=255, transition=10)
                self.run_in(self.changesetting, 1,value=10)
            else:
                # self.log("else")
                self.setlight(brightness=254, transition=1)
                self.run_in(self.changesetting, 1,value=99)
        else:
            self.setlight(brightness=254, transition=1)
            # self.log("aan")
            self.run_in(self.changesetting, 1, value=99)

    def setlight(self, brightness, transition):
        self.turn_on("light.badkamer_plafond_level", brightness=brightness, transition=transition)
        # self.turn_on("light.wk_eettafel_plafond_level", brightness=brightness, transition=transition)

    def setlightfade(self, kwargs):
        state = self.get_state("light.badkamer_plafond_level")
        # state = self.get_state("light.wk_eettafel_plafond_level")
        
        if state == "on":
            transition=kwargs['transition']
            if transition > 10:
                for i in range(10):
                    brightness = kwargs['brightness'] * (i+1) / 10
                    self.log(i)
                    delay = transition/10
                    self.setlight(brightness=brightness, transition=0)
                    time.sleep(delay)
                    self.log(delay)
                    # self.turn_on("light.badkamer_plafond_level", brightness=brightness)

            else:
                self.turn_on("light.badkamer_plafond_level", brightness=kwargs['brightness'], transition=kwargs['transition'])

    

