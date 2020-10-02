import appdaemon.plugins.hass.hassapi as hass

class douche(hass.Hass):
    def initialize(self):
        

        self.listen_state(self.inputhandler, "sensor.wk_boilerstatus", duration=60)
        self.listen_state(self.inputhandler, "input_boolean.tap_water_delay")
        self.listen_state(self.emstap, "binary_sensor.tap_water", new="on", duration=20)
        self.listen_state(self.emstap, "binary_sensor.tap_water", new="off")
        # self.listen_state(self.inputhandler, "binary_sensor.hotwateron")
        self.listen_state(self.inputhandler, "sensor.current_flow_temperature")
        self.listen_state(self.runout_on, "input_boolean.shower", new="on", duration=60)
        
        self.listen_state(self.shower_off, "input_boolean.shower", new="off", duration=30)
        self.listen_state(self.runout_off, "timer.fanrunout", new="idle", duration=10)

        self.log(self.get_state("light.badkamer_plafond_level"))


    def emstap(self, entity, attribute, old, new, kwargs):
        emstap = self.get_state("binary_sensor.tap_water")
        if emstap == "on":
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.tap_water_delay") 
        else:
            self.call_service("input_boolean/turn_off", entity_id="input_boolean.tap_water_delay")


    def inputhandler(self, entity, attribute, old, new, kwargs):
        # self.log("ping")
        wk_boilerstatus = self.get_state("sensor.wk_boilerstatus")
        
        if self.get_state("sensor.current_flow_temperature") == "unavailable" or self.get_state("sensor.current_flow_temperature") == "unknown":
            self.log("sensor.current_flow_temperature  = unavailable")
            hw_aanvoer_temp = 20
        else:
            hw_aanvoer_temp = float(self.get_state("sensor.current_flow_temperature"))
            
        lamp = self.get_state("light.badkamer_plafond_level")
        curr_shower_state = self.get_state("input_boolean.shower")
        tap_water_delay = self.get_state("input_boolean.tap_water_delay")
        
        # self.log("wk_boilerstatus: "+wk_boilerstatus)
        
        # self.log("curr_shower_state: "+curr_shower_state)

        if (lamp == "on"  and
            (
                wk_boilerstatus == "HW" 
                
            )):
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower") 
            #shower is active
        elif tap_water_delay == "on" and lamp == "on":
            self.log("tap delay shower on")
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower") 
        elif (curr_shower_state == "on" and
            (
                wk_boilerstatus == "CH" or 
                wk_boilerstatus == "No" or 
                hotwateron_negative_gradient == "on" or
                tap_water_delay == "off"
                
            )):

            self.call_service("input_boolean/turn_off", entity_id="input_boolean.shower") 
            

    def runout_on(self, entity, attribute, old, new, kwargs):
        self.log("runout = aan, douche is aan")
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.showerfanrunout")
    

            

    def shower_off(self, entity, attribute, old, new, kwargs):
        self.call_service("timer/cancel", entity_id="timer.fanrunout")
        self.call_service("timer/start", entity_id="timer.fanrunout", duration=900)
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.showerfanrunout")
        
        self.log("runout = aan, douche is uit")
        

    def runout_off(self, entity, attribute, old, new, kwargs):
        self.log("runout = uit")
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.showerfanrunout")

 