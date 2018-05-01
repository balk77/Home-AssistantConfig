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

        # zolder temperatuur te hoog
        self.listen_state(self.main, "input_boolean.zolder_te_warm")
        self.listen_state(self.main, "input_boolean.zolder_veel_te_warm")

        #self.listen_state(self.main, "input_number.boilerstatus_dummy")
        #desiredStateHW = self.boilerstatus





    def main(self, entity, attribute, old, new, kwargs):
        self.log("   ")
        # get the fan level for the current humidity level
        desiredStateHUM = self.humidity_level()
        # get the fan level for the current boiler status level
        desiredStateHW = self.boilerstatus
        curr_fanstate =  self.get_state("input_select.fanstate")

        desiredStateZOLDER = self.zolder_ventilatie_status

        self.log(desiredStateZOLDER)


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


        # self.timestamp_high is set to current time (seconds)
        # if not set, make it zero
        try:
            self.timestamp_high
        except:
            self.timestamp_high = 0

        self.shower = self.get_state("input_boolean.shower")

        self.log("Douch status:")
        self.log(self.shower)



        # self.log("douche init: ")
        # self.log(self.shower)


        # Wish to delay reverting to medium or low levels with a delay
        timestamp_delta_high = time.time()-self.timestamp_high
        # self.log(timestamp_delta_high)

        runout_time = 900 # seconds
        if desiredStateHUM == "full":
            self.setfanstate("full")
            status = self.set_state("input_boolean.shower", state="on")
        elif desiredStateHW == "high" or desiredStateHUM == "high":
            # Close the ventilation for the attic to force airflow from bathroom
            self.set_value("input_number.zolder_ventilatie", 0)

            if desiredStateHW == "high" and desiredStateHUM == "high":
                    status = self.set_state("input_boolean.shower", state="on")


            # xx = self.get_state("input_boolean.shower")
            # self.log("Showerrrr 2:")
            # self.log(xx)

            # record curren time stamp to facilitate runout time
            self.timestamp_high = time.time()
            if desiredStateHUM == "high" or desiredStateZOLDER == "high":
                self.setfanstate("high")
            else:
                # start fan in high mode with 60 seconds delay
                # Short usage of hot water does nor require fan to switch on
                # boiler status is reported every 10 seconds
                if curr_fanstate != "high":
                    self.run_in(self.fanstatehighdelay, 60)
        elif desiredStateZOLDER == "high":
            self.setfanstate("high")
        elif desiredStateHUM == "medium" or desiredStateZOLDER == "medium": # and timestamp_delta_high > runout_time:
            #self.log("komen we bij medium?")
            if self.shower == "on":
                self.run_in(self.fanstatedowndelay, 900)

                #self.log("effe wachten medium")
            else:
                self.set_value("input_number.zolder_ventilatie", 100)
                #self.log("fan medium")
                self.setfanstate("medium")
            # reset timestamp_high
            self.timestamp_high = 0
        elif desiredStateHW == "low" or desiredStateHUM == "low" or desiredStateZOLDER == "low":
            #self.log("komen we bij low?")
            if self.shower == "on":
                self.run_in(self.fanstatedowndelay, 900)

                #self.log("effe wachten low")
            else:
                self.set_value("input_number.zolder_ventilatie", 100)
                #self.log("fan medium")
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
        #humdelta = float(self.get_state("input_number.humdelta_dummy"))

        # if humdelta < 2:
        #     # fanstate low
        #     desiredState = "low"
        # elif humdelta >= 2 and humdelta < 4:
        #     # fanstate medium
        #     desiredState = "medium"
        # if humdelta >= 4 and humdelta < 8:
        #     # fanstate high
        #     desiredState = "high"
        # if humdelta >= 8:
        #     desiredState = "full"


        if humdelta < 5:
            # fanstate low
            desiredState = "low"
        elif humdelta >= 5 and humdelta < 10:
            # fanstate medium
            desiredState = "medium"
        if humdelta >= 10 and humdelta < 15:
            # fanstate high
            desiredState = "high"
        if humdelta >= 15:
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

    def zolder_ventilatie_status(self, entity, attribute, old, new, kwargs):
        # als de zolder te warm is, zet fan aan
        zolder_te_warm = self.get_state("input_boolean.zolder_te_warm")
        zolder_veel_te_warm = self.get_state("input_boolean.zolder_veel_te_warm")

        if zolder_veel_te_warm == "on":
            return "high"
        elif zolder_te_warm == "on":
            return "medium"
        else:
            return "low"


    def fanstatehighdelay(self, kwargs):
        boilerstatus = self.get_state("sensor.wk_boilerstatus")
        if boilerstatus == "HW":
            self.setfanstate("high")

    def fanstatedowndelay(self, kwargs):
        self.set_state("input_boolean.shower", state="off")

        self.main

    def setfanstate(self, desiredState):
        curState = self.get_state("input_select.fanstate")
        if desiredState != curState:
            self.set_state("input_select.fanstate", state=desiredState)