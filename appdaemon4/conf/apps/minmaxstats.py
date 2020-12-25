import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timezone, timedelta


class minmaxstats(hass.Hass):

    def initialize(self):
        
        self.array = [self.args["initial_value"]]
        self.datapoint = self.args["initial_value"]

        # select min or max
        self.stat_type = self.args["stat_type"]

        max_age = self.args["max_age"]
        interval = self.args["interval"]
        self.max_array_size = max_age/interval
        # self.log(self.max_array_size)

        self.run_every(self.inputhandler, "now", interval)


    def inputhandler(self, kwargs):
        # self.log(self.get_state(self.args["enity_id"]))
        newdatapoint = float(self.get_state(self.args["enity_id"]))
        
        
        if len(self.array) >= self.max_array_size:
            self.array.pop(0)
        
        self.log(min(self.array))
        self.array.append(newdatapoint)

        if self.stat_type == "max":
            if max(self.array) > self.datapoint:
                update = True
                self.datapoint = max(self.array)
                # self.log(max(self.array))
            else:
                update = False
        elif self.stat_type == "min":
            if min(self.array) < self.datapoint:
                update = True
                self.datapoint = min(self.array)
                # self.log(min(self.array))
            else:
                update = False
            

        if update:
            self.call_service("input_number/set_value",entity_id=self.args["input_number"],value=self.datapoint)
        

    
    

      
