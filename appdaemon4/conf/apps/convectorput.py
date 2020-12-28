import appdaemon.plugins.hass.hassapi as hass
import datetime


class convectorput(hass.Hass):
    def initialize(self):
        #self.listen_state(self.inputhandler, "sensor.ch_aanvoer")
        # self.listen_state(self.required_state_on, "binary_sensor.heating", new="on")
        # self.listen_state(self.control, "sensor.ch_aanvoer")
        self.listen_state(self.control, "sensor.convector_aanvoer_temperatuur")

        # self.listen_state(self.required_state_off, "binary_sensor.heating", new="off")
        #self.listen_state(self.inputhandler, "input_boolean.convector_fan")
        self.listen_state(self.disable_fan, "input_boolean.convector_fan_disabled", new="on")
    
    def disable_fan(self, entity, attribute, old, new, kwargs):
        self.run_in(self.stopfan, 1)
    
    def control(self, entity, attribute, old, new, kwargs):
        ch_aanvoer_raw = self.get_state("sensor.convector_aanvoer_temperatuur")
        self.log(ch_aanvoer_raw)
        currentstate = self.get_state("input_select.convector_fanspeed")
        if ch_aanvoer_raw != "unknown" or ch_aanvoer_raw != "undefined":
            try:
                ch_aanvoer = float(ch_aanvoer_raw)
                
                # self.log(type(ch_aanvoer))

                

                if ch_aanvoer > 35:
                    convector_fan_disabled = self.get_state("input_boolean.convector_fan_disabled")
                    if convector_fan_disabled == "on":
                        required_state = "off"
                    else:
                        required_state = "on"
                    self.log(required_state)
                    actual_temp = float(self.get_state("sensor.wk_thermostaat_pv"))

                    setpoint = float(self.get_state("sensor.thermostaat_tempsetpoint"))
                    
                    # if 1 < (setpoint - actual_temp) < 2 and currentstate != "Medium":
                    if 1 < (setpoint - actual_temp) < 2:
                        self.call_service("input_select/select_option", entity_id="input_select.convector_fanspeed", option="Medium")
                        self.turn_on("light.convectorput", brightness=self.args["med"]+20)
                        self.handle = self.run_in(self.runfan, 5, speed=self.args["med"])
                        # self.log("Convectorput aan (medium)")
                    # if setpoint - actual_temp >= 2 and currentstate != "High":
                    if setpoint - actual_temp >= 2:
                        self.call_service("input_select/select_option", entity_id="input_select.convector_fanspeed", option="High")
                        self.turn_on("light.convectorput", brightness=self.args["max"])
                        # self.log("Convectorput aan (max)")
                    # elif currentstate != "Low":
                    else:
                        self.call_service("input_select/select_option", entity_id="input_select.convector_fanspeed", option="Low")
                        self.turn_on("light.convectorput", brightness=self.args["min"]+20)
                        self.handle = self.run_in(self.runfan, 5, speed=self.args["min"])
                        # self.log("Convectorput aan (normal)")
                    # else:
                        # self.log("Convectorput is al op snelheid")
                elif currentstate != "Off":
                    self.run_in(self.stopfan, 240)
                else:
                    self.log("Tsja")
                    
            except:
                self.log("error gevonden")

    def stopfan(self,x):
        self.call_service("input_select/select_option", entity_id="input_select.convector_fanspeed", option="Off")
        self.turn_off("light.convectorput")

    def runfan(self, speed):
        speed = speed["speed"]
        self.log(speed)
        self.turn_on("light.convectorput", brightness=speed)
    
    def required_state_off(self, entity, attribute, old, new, kwargs):
        self.run_in(self.stopfan, 240)                    

    # def required_state_on(self, entity, attribute, old, new, kwargs):
    #     ch_aanvoer = float(self.get_state("sensor.ch_aanvoer"))

    #     #required_state = self.get_state("binary_sensor.heating")
    #     # self.log(required_state)
    #     convector_fan_disabled = self.get_state("input_boolean.convector_fan_disabled")
    #     if convector_fan_disabled == "on":
    #         required_state = "off"
    #     ch_aanvoer = float(self.get_state("sensor.ch_aanvoer"))
    #     actual_temp = float(self.get_state("sensor.wk_multisensor_temperature"))
    #     setpoint = float(self.get_state("sensor.wk_thermostaat_hass_sp"))
    #     #spotify_state = self.get_state("media_player.spotify")
    #     currentstate = self.get_state("light.convectorput", attribute="brightness")
        
    #     # self.log("Huidige fan speed: {}".format(currentstate))
    #     # self.log("aanvoer temp: {}".format(ch_aanvoer))

    #     # if spotify_state == "playing":
    #     #     minimum = self.args["med"]
    #     # else:
    #     #     minimum = self.args["min"]
        
    #     # if required_state == "on":

    #     if ch_aanvoer > 35:
    #         # self.log(ch_aanvoer)
    #         #self.call_service("timer/start", entity_id="timer.convectorput_runout", duration=900)
    #         if 1 < (setpoint - actual_temp) < 2 and currentstate != self.args["med"]:
    #             self.turn_on("light.convectorput", brightness=self.args["med"]+20)
    #             self.handle = self.run_in(self.runfan, 5, speed=self.args["med"])
    #             # self.log("Convectorput aan (medium)")
    #         if setpoint - actual_temp >= 2 and currentstate != self.args["max"]:
    #             self.turn_on("light.convectorput", brightness=self.args["max"])
    #             # self.log("Convectorput aan (max)")
    #         elif currentstate != self.args["min"]:
    #             self.turn_on("light.convectorput", brightness=self.args["min"]+20)
    #             self.handle = self.run_in(self.runfan, 5, speed=self.args["min"])
    #             # self.log("Convectorput aan (normal)")
    #         # else:
    #         #     self.log("Convectorput is al op snelheid")
    #     else:
    #         self.run_in(self.stopfan, 240)
    #         #self.turn_off("light.convectorput_2")
    #         #self.log("Convectorput idle (koud)")
    #     # else:
    #     #     self.run_in(self.stopfan, 240)
    #     #     #self.turn_off("light.convectorput_2")
    #     #     #self.log("Convectorput DBE uitgeschakeld")

    

