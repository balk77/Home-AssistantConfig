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

        # Change in humidity_level
        self.listen_state(self.main, "sensor.humdelta")
        #self.listen_state(self.main, "input_number.humdelta_dummy")

        # change in boiler status
        self.listen_state(self.main, "sensor.wk_boilerstatus")
        #self.listen_state(self.boiler_to_low, "sensor.wk_boilerstatus", old="HW")

        # change in attic temperature
        self.listen_state(self.main,"sensor.zolder_max_t")

        #self.listen_state(self.main, "input_number.boilerstatus_dummy")
        #desiredStateHW = self.boilerstatus
        #self.log(self.get_state("input_boolean.vakantie"))


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
        #self.log(self.get_state("input_boolean.vakantie"))
        if self.get_state("input_boolean.vakantie") == "off":

            # self.log("   ")
            # get the fan level for the current humidity level
            desiredStateHUM = self.humidity_level()
            # get the fan level for the current boiler status level
            desiredStateHW = self.boilerstatus
            curr_fanstate =  self.get_state("input_select.fanstate")

            desiredStateZOLDER = self.zolder_ventilatie_status()

            # when hot water is reported, return "high"
            boilerstatus = self.get_state("sensor.wk_boilerstatus")
            #boilerstatus = self.get_state("input_number.boilerstatus_dummy")

            # try:
            #     self.counter
            # except:
            #     self.counter = 0
            #
            # self.counter = self.counter + 1


            if boilerstatus == "HW": #  or boilerstatus == 2:
                desiredStateHW = "high"
            else:
                desiredStateHW = "low"


            # self.log("Hot Water:")
            # self.log(desiredStateHW)
            #
            # self.log("humidity:")
            # self.log(desiredStateHUM)
            #
            # self.log("zolder fan:")
            # self.log(desiredStateZOLDER)


            # self.timestamp_high is set to current time (seconds)
            # if not set, make it zero
            try:
                self.timestamp_high
            except:
                self.timestamp_high = 0

            self.shower = self.get_state("input_boolean.shower")

            # self.log("Douche status:")
            # self.log(self.shower)



            # self.log("douche init: ")
            # self.log(self.shower)


            # Wish to delay reverting to medium or low levels with a delay
            timestamp_delta_high = time.time()-self.timestamp_high
            # self.log(timestamp_delta_high)

            runout_time = 900 # seconds
            if desiredStateZOLDER == "full":
                #self.set_state("input_number.zolder_ventilatie", state=100)
                self.call_service("input_number/set_value", entity_id="input_number.zolder_ventilatie", value=100)
                itho_reason="Zolder temp high, fan FULL"
                self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
                #self.set_state("sensor.itho_reason", state="Zolder temp high, fan FULL")
                self.setfanstate("full")
            elif desiredStateZOLDER == "high":
                #self.set_state("input_number.zolder_ventilatie", state=100)
                self.call_service("input_number/set_value", entity_id="input_number.zolder_ventilatie", value=100)
                #self.set_state("sensor.itho_reason", state="Zolder temp high, fan HIGH")
                itho_reason="Zolder temp high, fan HIGH"
                self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
                self.setfanstate("high")
            elif desiredStateHUM == "full":
                self.setfanstate("full")
                itho_reason="Humidity high, fan FULL"
                self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
                #self.set_state("sensor.itho_reason", state="Humidity high, fan FULL")
                self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower")
                #status = self.set_state("input_boolean.shower", state="on")
            elif desiredStateHW == "high" or desiredStateHUM == "high":
                # Close the ventilation for the attic to force airflow from bathroom
                #self.set_state("input_number.zolder_ventilatie", state=0)
                self.call_service("input_number/set_value", entity_id="input_number.zolder_ventilatie", value=0)


                if desiredStateHW == "high" and desiredStateHUM == "high":
                    self.call_service("input_boolean/turn_on", entity_id="input_boolean.shower")
                    #status = self.set_state("input_boolean.shower", state="on")


                # xx = self.get_state("input_boolean.shower")
                # self.log("Showerrrr 2:")
                # self.log(xx)

                # record curren time stamp to facilitate runout time
                self.timestamp_high = time.time()
                badkamer_light = self.get_state("light.badkamer_plafond_level")


                if desiredStateHUM == "high":
                    self.setfanstate("high")
                    itho_reason="Humidity high, fan HIGH"
                    self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
                    #self.set_state("sensor.itho_reason", state="Humidity high, fan HIGH")
                elif badkamer_light == "On" and curr_fanstate != "high":
                    # start fan in high mode with 60 seconds delay
                    # Short usage of hot water does nor require fan to switch on
                    # boiler status is reported every 10 seconds
                    itho_reason="Humidity high, shower, fan HIGH"
                    self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
                    #self.set_state("sensor.itho_reason", state="Humidity high, shower, fan HIGH")
                    self.run_in(self.fanstatehighdelay, 60)

            elif desiredStateHUM == "medium" or desiredStateZOLDER == "medium": # and timestamp_delta_high > runout_time:
                #self.log("komen we bij medium?")
                if self.shower == "on":
                    self.run_in(self.fanstatedowndelay, 900)

                    #self.log("effe wachten medium")
                else:
                    #self.set_state("input_number.zolder_ventilatie", state=100)
                    self.call_service("input_number/set_value", entity_id="input_number.zolder_ventilatie", value=100)
                    #self.log("fan medium")
                    if desiredStateHUM == "medium" and desiredStateZOLDER == "medium":
                        msg = "Badkamer hum  = medium, zolder temp = medium, fan MED"
                    elif desiredStateHUM == "medium":
                        msg = "Badkamer hum  = medium, fan MED"
                    elif desiredStateZOLDER == "medium":
                        msg = "zolder temp = medium, fan MED"
                        
                    #self.set_state("sensor.itho_reason", state=msg)
                    self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=msg)
                    self.setfanstate("medium")
                # reset timestamp_high
                self.timestamp_high = 0
            elif desiredStateHW == "low" or desiredStateHUM == "low" or desiredStateZOLDER == "low":
                #self.log("komen we bij low?")
                if self.shower == "on":
                    self.run_in(self.fanstatedowndelay, 900)

                    #self.log("effe wachten low")
                else:
                    self.call_service("input_number/set_value", entity_id="input_number.zolder_ventilatie", value=100)
                    # input_number.set_value
                    # self.set_state("input_number.zolder_ventilatie", state=100)
                    #self.log("fan medium")
                    itho_reason="fan LOW"
                    self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
                    self.setfanstate("low")
                # reset timestamp_high
                self.timestamp_high = 0
            # self.log("counter:")
            # self.log(self.counter)


    #def humidity_level(self, entity, attribute, old, new, kwargs):
    def humidity_level(self):
        # humdelta unit of measurement is mg/m3
        # HASS has a sensor that receives the lowest absolute humidity in the past
        # two hours. Delta between current humidity and lowest is humdelta
        humdelta = float(self.get_state("sensor.humdelta"))
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

        low_upper = 10
        med_upper = 15
        high_upper = 20

        if relhum > 95:
            desiredState = "full"
        elif humdelta < low_upper:
            # fanstate low
            desiredState = "low"
        elif humdelta >= low_upper and humdelta < med_upper:
            # fanstate medium
            desiredState = "medium"
        elif humdelta >= med_upper and humdelta < high_upper:
            # fanstate high
            desiredState = "high"
        elif humdelta >= high_upper:
            desiredState = "full"
        return desiredState

    def boilerstatus(self, entity, attribute, old, new, kwargs):
        # when hot water is reported, return "high"
        boilerstatus = self.get_state("sensor.wk_boilerstatus")
        #boilerstatus = self.get_state("input_number.boilerstatus_dummy")
        if boilerstatus == "HW": #  or boilerstatus == 2:
            return "high"
        else:
            return "low"

    #def zolder_ventilatie_status(self, entity, attribute, old, new, kwargs):
    def zolder_ventilatie_status(self):
        # als de zolder te warm is, zet fan aan
        zolder_max_t = float(self.get_state("sensor.zolder_max_t"))
        zolder_delta_t = float(self.get_state("sensor.zolder_delta_t"))

        # self.log("lala")
        # self.log(zolder_max_t)
        # self.log(zolder_delta_t)

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


    def fanstatehighdelay(self, kwargs):
        boilerstatus = self.get_state("sensor.wk_boilerstatus")
        if boilerstatus == "HW":
            self.setfanstate("high")
            itho_reason="Douche aan, fan HIGH"
            self.call_service("input_text/set_value", entity_id="input_text.itho_reason", value=itho_reason)
            #self.set_state("sensor.itho_reason", state="Douche aan, fan HIGH")
            

    def fanstatedowndelay(self, kwargs):
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.shower")

        #self.set_state("input_boolean.shower", state="off")

        self.main

    def setfanstate(self, desiredState):
        curState = self.get_state("input_select.fanstate")
        if desiredState != curState:
            self.call_service("input_select/select_option", entity_id="input_select.fanstate", option=desiredState)
            #self.set_state("input_select.fanstate", state=desiredState)
