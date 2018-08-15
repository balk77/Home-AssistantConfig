import appdaemon.plugins.hass.hassapi as hass

class vakantie(hass.Hass):
    def initialize(self):
        
        self.listen_state(self.inputhandler, "input_boolean.vakantie")
        


    def inputhandler(self, entity, attribute, old, new, kwargs):
        #self.log("ping")
        vakantie = self.get_state("input_boolean.vakantie")
        
        if vakantie == "on":
            self.turn_off("switch.fibaro_switch_switch")
        else:
            self.turn_on("switch.fibaro_switch_switch")

