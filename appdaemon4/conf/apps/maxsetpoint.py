import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timezone, timedelta
#
# Hellow World App
#
# Args:
#

class maxsetpoint(hass.Hass):

    def initialize(self):
        
        self.temp_array = [15]
        self.max_temperature_setpoint = 15

        max_age = self.args["max_age"]
        interval = self.args["interval"]
        self.max_array_size = max_age/interval
        self.log(self.max_array_size)

        self.run_every(self.inputhandler, "now", interval)

    def inputhandler(self, kwargs):
        newsetpoint = float(self.get_state("sensor.thermostaat_tempsetpoint"))
        if len(self.temp_array) >= self.max_array_size:
            self.temp_array.pop(0)
        
        # temp_array = 
        self.temp_array.append(newsetpoint)
        if max(self.temp_array) > self.max_temperature_setpoint:
            self.max_temperature_setpoint = max(self.temp_array)
            # self.log(max(self.temp_array))
            self.call_service("input_number/set_value",entity_id="input_number.max_temperature_setpoint",value=self.max_temperature_setpoint)
        

    
    

      