import appdaemon.plugins.hass.hassapi as hass
import time


# if HW for 1 minute: fan high for 15 minute
# if humdelta high: fan high for 15 minute
# if fanstate = high: zolder_ventilatie: off
# if HW: zolder_ventilatie: off

class fancontrol(hass.Hass):
    def initialize(self):
        # Listen for state change of ventilation requirements
        # self.log("   ")
        self.itho_reason_old = "x"
        itho_reason = "x"

        # Change in humidity_level
        self.listen_state(self.main, "sensor.humdelta")
        #self.listen_state(self.main, "input_number.humdelta_dummy")

        # change in boiler status
        self.listen_state(self.main, "sensor.wk_boilerstatus")
        #self.listen_state(self.boiler_to_low, "sensor.wk_boilerstatus", old="HW")

        # change in attic temperature
        # self.listen_state(self.main,"sensor.zolder_max_t")

        self.listen_state(self.main, "input_boolean.shower")
        self.listen_state(self.main, "input_boolean.showerfanrunout")
        #desiredStateHW = self.boilerstatus
        #self.log(self.get_state("input_boolean.vakantie"))
        self.listen_state(self.main, "input_boolean.test")


    def send_message(self, **kwargs):
        self.log(kwargs['msg'])
        try:
            self.call_service('notify/telegram',
                                message_id="last",
                                title="*"+kwargs['title']+"*",
                                message=kwargs['msg'],
                                disable_notification="true")
                            
        except:
            try:
                self.call_service('notify/telegram',
                                message_id="last",
                                message=kwargs['msg'],
                                disable_notification="true")
            except:
                self.log("error")


    def main(self, entity, attribute, old, new, kwargs):
        # self.log(self.itho_reason_old)

        itho_reason="x"

        #self.log(self.get_state("input_boolean.vakantie"))
        if self.get_state("input_boolean.vakantie") == "off":

            # get the fan level for the current humidity level
            desiredStateHUM = self.humidity_level()
            # get the fan level for the current boiler status level
            desiredStateHW = self.boilerstatus()
            # self.log("Douche status:")
            
            # self.log("fancontrol: "+desiredStateHUM)

            

            desiredStateZOLDER = self.zolder_ventilatie_status()
            showerfanrunout = self.get_state("input_boolean.showerfanrunout")

            if showerfanrunout == "on":
                
                if desiredStateHUM == "full":
                    self.setfanstate("High")
                    itho_reason="Humidity high, fan FULL, runout"
                    
                else:
                    self.setfanstate("High")
                    itho_reason="Humidity high, fan high, runout"
                    
                    
            elif desiredStateHUM == "full":
                # Close the ventilation for the attic to force airflow from bathroom
                
                self.call_service("cover/close_cover", entity_id="cover.zolder_ventilatie")


                # self.setfanstate("full")
                self.setfanstate("High")
                itho_reason="Humidity high, fan FULL"
                
                
                self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower")
            elif desiredStateZOLDER == "full":
                
                self.call_service("cover/open_cover", entity_id="cover.zolder_ventilatie")

                itho_reason="Zolder temp high, fan FULL"
                
                # self.setfanstate("full")
                self.setfanstate("High")
            elif desiredStateZOLDER == "high":
                
                self.call_service("cover/open_cover", entity_id="cover.zolder_ventilatie")
                itho_reason="Zolder temp high, fan HIGH"
                
                # self.setfanstate("high")
                self.setfanstate("High")
            
            elif desiredStateHW == "high":
                # Close the ventilation for the attic to force airflow from bathroom
                
                self.call_service("cover/close_cover", entity_id="cover.zolder_ventilatie")

                # shower is on
                # self.setfanstate("high")
                self.setfanstate("High")
                itho_reason="Douche actief, fan HIGH"
                
            elif desiredStateHUM == "high":
                # Close the ventilation for the attic to force airflow from bathroom
                
                self.call_service("cover/close_cover", entity_id="cover.zolder_ventilatie")

                # record curren time stamp to facilitate runout time
                
                # self.setfanstate("high")
                self.setfanstate("High")
                itho_reason="Humidity high, fan HIGH"
                
                

            elif desiredStateHUM == "medium" or desiredStateZOLDER == "medium": 
                
                
                self.call_service("cover/open_cover", entity_id="cover.zolder_ventilatie")
                #self.log("fan medium")
                if desiredStateHUM == "medium" and desiredStateZOLDER == "medium":
                    msg = "Badkamer hum  = medium, zolder temp = medium, fan MED"
                elif desiredStateHUM == "medium":
                    msg = "Badkamer hum  = medium, fan MED"
                elif desiredStateZOLDER == "medium":
                    msg = "zolder temp = medium, fan MED"
                    
                
                # self.setfanstate("medium")
                self.setfanstate("Medium")
            elif desiredStateHW == "low" or desiredStateHUM == "low" or desiredStateZOLDER == "low":

                
                self.call_service("cover/open_cover", entity_id="cover.zolder_ventilatie")
                
                itho_reason="fan LOW"
                
                # self.setfanstate("low")
                self.setfanstate("Low")
            
            if itho_reason != self.itho_reason_old:
                self.itho_reason_old = itho_reason
                
                # self.log(self.itho_reason_old)
                self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)



    #def humidity_level(self, entity, attribute, old, new, kwargs):
    def humidity_level(self):
        # humdelta unit of measurement is mg/m3
        # HASS has a sensor that receives the lowest absolute humidity in the past
        # two hours. Delta between current humidity and lowest is humdelta
        humdelta = float(self.get_state("sensor.humdelta"))
        # humdelta_average = float(self.get_state("sensor.humdelta_sma"))
        # humdelta = max(humdelta_single,humdelta_average)
        #self.log(humdelta)
        desiredState = ""

        relhum = float(self.get_state("sensor.badkamer_relhumidity"))
        #humdelta = float(self.get_state("input_number.humdelta_dummy"))

        # if humdelta < 2:
        #     # fanstate low
        #     desiredState = "low"
        # elif humdelta >= 2 and humdelta < 4:
        #     # fanstate medium
        #     desiredState = "medium"
        # elif humdelta >= 4 and humdelta < 8:
        #     # fanstate high
        #     desiredState = "high"
        # elif humdelta >= 8:
        #     desiredState = "full"

        humidity_to_full = self.get_state("input_boolean.humidity_to_full")
        humidity_to_high = self.get_state("input_boolean.humidity_to_high")
        humidity_to_medium = self.get_state("input_boolean.humidity_to_medium")
        # self.log(humidity_to_medium)

        # humidity_to_full = False
        # humidity_to_high = False
        # humidity_to_medium = False
        

        low_upper = 10
        med_upper = 15
        high_upper = 20

        if humidity_to_full == "on":
            desiredState = "full"
        else:
            if relhum > 95 or humdelta >= high_upper:
                desiredState = "full"
                self.call_service("input_boolean/turn_on", entity_id="input_boolean.humidity_to_full")            
            elif humidity_to_high == "on":
                desiredState = "high"
            else:
                if humdelta >= med_upper and humdelta < high_upper:
                    # fanstate high
                    desiredState = "high"
                    self.call_service("input_boolean/turn_on", entity_id="input_boolean.humidity_to_high")
                elif humidity_to_medium == "on":
                    desiredState = "medium"
                else:
                    if humdelta >= low_upper and humdelta < med_upper:
                        # fanstate medium
                        desiredState = "medium"
                        self.call_service("input_boolean/turn_on", entity_id="input_boolean.humidity_to_medium")
                    elif humdelta < low_upper:
                        # fanstate low
                        desiredState = "low"
        # self.log("desiredState")
        # self.log(desiredState)
        return desiredState

    def boilerstatus(self):
        # when hot water is reported, return "high"
        boilerstatus = self.get_state("input_boolean.shower")
        runoutstatus = self.get_state("input_boolean.showerfanrunout")
        # self.log("boiler status:")
        
        # self.log(boilerstatus)
        if boilerstatus == "on" or runoutstatus == "on": #  or boilerstatus == 2:
            return "high"
        else:
            return "low"

    def zolder_ventilatie_status(self):
        # als de zolder te warm is, zet fan aan
        #zolder_max_t = float(self.get_state("sensor.zolder_max_t"))
        zolder_max_t = 20
        #zolder_delta_t = float(self.get_state("sensor.zolder_delta_t"))
        zolder_delta_t = 1

        if zolder_delta_t < 0:
            if zolder_max_t >= 38:
                return "full"
            elif 35 < zolder_max_t < 38:
                return "high"
            elif 22 < zolder_max_t < 35:
                return "medium"
            else:
                return "low"
        else:
            return "low"



    def setfanstate(self, desiredState):
        # self.log("desiredState: "+desiredState)
        # if desiredState == "full" or desiredState == "high":
        #     desiredState = "High"
        # elif desiredState == "medium":
        #     desiredState = "Medium"
        # elif desiredState == "low":
        #     desiredState = "Low"
        # self.log("desiredState")
        # self.log(desiredState)

        


        self.call_service("fan/turn_on", entity_id="fan.itho",speed=desiredState)
        # curState = self.get_state("input_select.fanstate")
        # if desiredState != curState:
        #     self.call_service("input_select/select_option", entity_id="input_select.fanstate", option=desiredState)
            
