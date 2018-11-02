import appdaemon.plugins.hass.hassapi as hass

class douche(hass.Hass):
    def initialize(self):
        

        self.listen_state(self.inputhandler, "sensor.wk_boilerstatus", duration=60)
        self.listen_state(self.inputhandler, "binary_sensor.hotwateron")
        self.listen_state(self.inputhandler, "sensor.hw_aanvoer")
        self.listen_state(self.runout_on, "input_boolean.shower", new="on", duration=60)
        
        self.listen_state(self.shower_off, "input_boolean.shower", new="off", duration=30)
        self.listen_state(self.runout_off, "timer.fanrunout", new="idle", duration=10)



    def inputhandler(self, entity, attribute, old, new, kwargs):
        
        wk_boilerstatus = self.get_state("sensor.wk_boilerstatus")
        hotwateron_positive_gradient = self.get_state("binary_sensor.hotwateron")
        hotwateron_negative_gradient = self.get_state("binary_sensor.hotwateroff")
        if self.get_state("sensor.hw_aanvoer") == "unavailable":
            self.log("sensor.hw_aanvoer  = unavailable")
            quit()
        else:
            hw_aanvoer_temp = float(self.get_state("sensor.hw_aanvoer"))
            
        lamp = self.get_state("light.badkamer_plafond_level")
        curr_shower_state = self.get_state("input_boolean.shower")
        #curr_shower_state = self.get_state("input_boolean.shower_alt")
        # self.log("wk_boilerstatus")
        # self.log(wk_boilerstatus)
        # self.log("hotwateron_positive_gradient")
        # self.log(hotwateron_positive_gradient)
        # self.log("hotwateron_negative_gradient")
        # self.log(hotwateron_negative_gradient)
        # self.log("curr_shower_state")
        # self.log(curr_shower_state)

        #if (lamp == "on" and curr_shower_state == "off" and hotwateron_negative_gradient == "off" and
        if (lamp == "on" and hotwateron_negative_gradient == "off" and
            (
                wk_boilerstatus == "HW" or 
                (hotwateron_positive_gradient == "on" or hw_aanvoer_temp > 40) 
                
            )):
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower") 
            #self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower_alt") 
            #shower is active
        elif (curr_shower_state == "on" and
            (
                wk_boilerstatus == "CH" or 
                wk_boilerstatus == "No" or 
                hotwateron_negative_gradient == "on"
                
            )):

            self.call_service("input_boolean/turn_off", entity_id="input_boolean.shower") 
            #self.call_service("input_boolean/turn_off", entity_id="input_boolean.shower_alt") 

    def runout_on(self, entity, attribute, old, new, kwargs):
        #self.switch_runout(action="on")
        self.log("runout = aan, douche is aan")
        # self.run_in(self.switch_runout, 1, action="on")
        #self.call_service("input_boolean/turn_on", entity_id="input_boolean.showerfanrunout")
        # self.call_service("timer/cancel", entity_id="timer.fanrunout")
        # self.call_service("timer/start", entity_id="timer.fanrunout", duration=900)
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.showerfanrunout")
    

            

    def shower_off(self, entity, attribute, old, new, kwargs):
        self.call_service("timer/cancel", entity_id="timer.fanrunout")
        self.call_service("timer/start", entity_id="timer.fanrunout", duration=900)
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.showerfanrunout")
        
        self.log("runout = aan, douche is uit")
        # self.run_in(self.switch_runout, 900, action="off")

    def runout_off(self, entity, attribute, old, new, kwargs):
        self.log("runout = uit")
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.showerfanrunout")

            
#    def runout_off(self, entity, attribute, old, new, kwargs):
#         self.log("runout = uit")
#         self.run_in(self.switch_runout, 900, action="off")

#     def switch_runout(self, kwargs):
#         self.log(kwargs['action'])
#         if kwargs['action'] == "on":
#             self.call_service("input_boolean/turn_on", entity_id="input_boolean$
#         elif kwargs['action'] == "off":
#             self.call_service("input_boolean/turn_off", entity_id="input_boolea$


