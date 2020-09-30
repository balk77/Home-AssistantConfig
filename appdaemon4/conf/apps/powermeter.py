import appdaemon.plugins.hass.hassapi as hass


class powermeter(hass.Hass):

    def initialize(self):

        self.listen_state(self.inputhandler, "input_boolean.test",new="on")

    

    def inputhandler(self, entity, attribute, old, new, kwargs):
        
        newstate = self.get_state("sensor.ch_aanvoer")
        newtime = self.now()

        self.call_service("input_boolean/turn_off", entity_id="input_boolean.test")
