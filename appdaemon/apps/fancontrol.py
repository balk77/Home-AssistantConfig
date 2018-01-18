import appdaemon.appapi as appapi
import time

# if HW for 1 minute: fan high for 15 minute
# if humdelta high: fan high for 15 minute
# if fanstate = high: zolder_ventilatie: off
# if HW: zolder_ventilatie: off

class fancontrol(appapi.AppDaemon):
    def initialize(self):
        # Listen for state change of ventilation requirements

        # Change in humidity_level
        self.listen_state(self.main, "sensor.humdelta")
        #self.listen_state(self.main, "input_number.humdelta_dummy")

        # change in boiler status
        self.listen_state(self.main, "sensor.wk_boilerstatus")
        #self.listen_state(self.main, "input_number.boilerstatus_dummy")
        #desiredStateHW = self.boilerstatus





    def main(self, entity, attribute, old, new, kwargs):
        # get the fan level for the current humidity level
        desiredStateHUM = self.humidity_level()
        # get the fan level for the current boiler status level
        desiredStateHW = self.boilerstatus

        # when hot water is reported, return "high"
        boilerstatus = self.get_state("sensor.wk_boilerstatus")
        #boilerstatus = self.get_state("input_number.boilerstatus_dummy")


        if boilerstatus == "HW": #  or boilerstatus == 2:
            desiredStateHW = "high"
        else:
            desiredStateHW = "low"

        # self.log(desiredStateHW)


        # self.timestamp_high is set to current time (seconds)
        # if not set, make it zero
        try:
            self.timestamp_high
        except:
            self.timestamp_high = 0

        # Wish to delay reverting to medium or low levels with a delay
        timestamp_delta_high = time.time()-self.timestamp_high
        # self.log(timestamp_delta_high)

        runout_time = 900 # seconds

        if desiredStateHW == "high" or desiredStateHUM == "high":
            # Close the ventilation for the attic to force airflow from bathroom
            self.set_state("input_number.zolder_ventilatie", state=0)

            # record curren time stamp to facilitate runout time
            self.timestamp_high = time.time()
            if desiredStateHUM == "high":
                self.setfanstate("high")
            else:
                # start fan in high mode with 60 seconds delay
                # Short usage of hot water does nor require fan to switch on
                # boiler status is reported every 10 seconds
                self.run_in(self.fanstatehighdelay, 60)

        elif desiredStateHUM == "medium" and timestamp_delta_high > runout_time:
            self.set_state("input_number.zolder_ventilatie", state=100)
            #self.log("fan medium")
            self.setfanstate("medium")
            # reset timestamp_high
            self.timestamp_high = 0
        elif (desiredStateHW == "low" or desiredStateHUM == "low") and timestamp_delta_high > runout_time:
            self.set_state("input_number.zolder_ventilatie", state=100)
            #self.log("fan low")
            self.setfanstate("low")
            # reset timestamp_high
            self.timestamp_high = 0


    #def humidity_level(self, entity, attribute, old, new, kwargs):
    def humidity_level(self):
        # humdelta unit of measurement is mg/m3
        # HASS has a sensor that receives the lowest absolute humidity in the past
        # two hours. Delta between current humidity and lowest is humdelta
        humdelta = float(self.get_state("sensor.humdelta"))
        #humdelta = float(self.get_state("input_number.humdelta_dummy"))

        if humdelta < 2:
            # fanstate low
            desiredState = "low"
        elif humdelta >= 2 and humdelta < 4:
            # fanstate medium
            desiredState = "medium"
        if humdelta >= 4:
            # fanstate high
            desiredState = "high"
        return desiredState

    def boilerstatus(self, entity, attribute, old, new, kwargs):
        # when hot water is reported, return "high"
        boilerstatus = self.get_state("sensor.wk_boilerstatus")
        #boilerstatus = self.get_state("input_number.boilerstatus_dummy")
        if boilerstatus == "HW": #  or boilerstatus == 2:
            return "high"
        else:
            return "low"


    def fanstatehighdelay(self, kwargs):
        boilerstatus = self.get_state("sensor.wk_boilerstatus")
        if boilerstatus == "HW":
            self.setfanstate("high")

    def setfanstate(self, desiredState):
        curState = self.get_state("input_select.fanstate")
        if desiredState != curState:
            self.set_state("input_select.fanstate", state=desiredState)
