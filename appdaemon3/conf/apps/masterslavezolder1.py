import appdaemon.plugins.hass.hassapi as hass
from math import ceil
import datetime
import time

# https://www.raspberrypi.org/forums/viewtopic.php?t=92973
# https://www.raspberrypi.org/forums/viewtopic.php?t=92973#p649179

class masterslavezolder(hass.Hass):

    


    #def __init__(self, p_gain, i_gain, d_gain, now):
        

    def initialize(self):

        self.last_error = 0.0
        #self.last_time = datetime.datetime.now()
        self.last_time = time.time()


        self.p_gain = 0.75
        self.i_gain = 0.01
        self.d_gain = 0.001

        self.i_error = 0.0

        #self.listen_state(self.inputhandler, "sensor.thermostaat_tempsetpoint_raw")
        #self.handle = self.listen_event(self.inputhandler_event, 'MQTT_MESSAGE', namespace = 'mqtt', topic = self.args["roomsp"])
        self.handle = self.listen_event(self.inputhandler_event, 'MQTT_MESSAGE', namespace = 'mqtt', topic = "x/y/z")
        #self.listen_state(self.inputhandler_state, self.args["ventipv"])
        #self.listen_state(self.inputhandler_state, self.args["thermpv"])
        #self.listen_state(self.inputhandler_state, self.args["roomsp"])

    def inputhandler_state(self, entity, attribute, old, new, kwargs):
        self.main()

    def inputhandler_event(self, event_name, data, kwargs):
        self.main()

    def main(self):

        #time_now = datetime.datetime.now()
        time_now = time.time()


        #temp_pid = PID(PID_TEMP_P_GAIN, PID_TEMP_I_GAIN, PID_TEMP_D_GAIN, time_now)

        

        ventipv = float(self.get_state(self.args["ventipv"]))
        thermpv = float(self.get_state(self.args["thermpv"]))
        roomsp = float(self.get_state(self.args["roomsp"]))
        thermsp = float(self.get_state(self.args["thermsp2"]))

        # roomsp = 14
        # ventipv = 13.1

        [p_out, i_out, d_out] = self.Compute(ventipv, roomsp, time_now)

        #self.log([p_out, i_out, d_out])
        minsp = 13
        temp_out = minsp + ceil(2*(p_out + i_out + d_out))/2
        
        

        
        #self.log(thermpv)
        self.log("room SP is {} degrees".format(roomsp))
        self.log("room PV is {} degrees".format(ventipv))
        self.log("therm SP is {} degrees".format(thermsp))
        
        #self.log(ventipv)

        # if ventipv > roomsp:
        #     newsp_ = roomsp - (ventipv - thermpv)
        #     if newsp_ < roomsp:
        #         self.log("adjust sp")
        #         newsp = ceil(2*newsp_)/2
        #         self.log(newsp)

        # if 'newsp' in locals() and newsp >= 13:
        #     self.log("Adjust Therm SP, new SP = ")
        #     self.log(newsp)
        # else:
        #     newsp = roomsp
        #     self.log("Therm SP equal to Room SP")

        if temp_out <= 13:
            temp_out = 13
        elif temp_out > 18:
            temp_out = 18

        self.log("New thermostat SP is {}".format(temp_out))
        
        #self.call_service("mqtt/publish", topic=self.args["thermsp"], payload=newsp)
        #self.fire_event("heaty_set_temp", room_name="zolder", v=str(newsp), reschedule_delay=1)
    
    def Compute(self, input, target, now):
        dt = (now - self.last_time)
        #self.log(dt)

        #---------------------------------------------------------------------------
        # Error is what the PID alogithm acts upon to derive the output
        #---------------------------------------------------------------------------
        error = target - input

        #---------------------------------------------------------------------------
        # The proportional term takes the distance between current input and target
        # and uses this proportially (based on Kp) to control the ESC pulse width
        #---------------------------------------------------------------------------
        p_error = error

        #---------------------------------------------------------------------------
        # The integral term sums the errors across many compute calls to allow for
        # external factors like wind speed and friction
        #---------------------------------------------------------------------------
        self.i_error += (error + self.last_error) * dt
        i_error = self.i_error

        #---------------------------------------------------------------------------
        # The differential term accounts for the fact that as error approaches 0,
        # the output needs to be reduced proportionally to ensure factors such as
        # momentum do not cause overshoot.
        #---------------------------------------------------------------------------
        d_error = (error - self.last_error) / dt

        #---------------------------------------------------------------------------
        # The overall output is the sum of the (P)roportional, (I)ntegral and (D)iffertial terms
        #---------------------------------------------------------------------------
        p_output = self.p_gain * p_error
        i_output = self.i_gain * i_error
        d_output = self.d_gain * d_error

        #---------------------------------------------------------------------------
        # Store off last input for the next differential calculation and time for next integral calculation
        #---------------------------------------------------------------------------
        self.last_error = error
        self.last_time = now

        #---------------------------------------------------------------------------
        # Return the output, which has been tuned to be the increment / decrement in ESC PWM
        #---------------------------------------------------------------------------
        return p_output, i_output, d_output