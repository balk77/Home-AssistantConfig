import appdaemon.plugins.hass.hassapi as hass


class ZolderTemperatuurVentilatie(hass.Hass):
    def initialize(self):
        # Listen for state change of ventilation requirements
        self.listen_state(self.input_parse2, "input_number.zolder_ventilatie")
        # DesiredPercentage = self.get_state("input_number.zolder_ventilatie")
        self.log("lalala1")

    def input_parse2(self, entity, attribute, old, new, kwargs):
        # get Desired Percentage from Home assistant
        DesiredPercentage = float(self.get_state("input_number.zolder_ventilatie"))
        # get old Desired Percentage from Home assistant
        PreviousDesiredPercentage = float(self.get_state("input_number.zolder_ventilatie_old"))

        # self.log(DesiredPercentage)
        # self.log(PreviousDesiredPercentage)

        # Disable input from user interface and show message "Valve is moving" instead

        self.call_service("group/set_visibility", entity_id="group.zolder_ventilatie", visible="False")
        self.call_service("group/set_visibility", entity_id="group.zolder_ventilatie_moving", visible="True")

        # Set time (seconds) for the valve to move from open to close, or close to open
        time_to_open = 29
        if DesiredPercentage == 100:
            # valve needs to open fully, for instance during HASS startup
            direction = "open"
            PulseTime_sec = time_to_open
        elif DesiredPercentage == 0:
            # valve needs to close
            direction = "close"
            PulseTime_sec = time_to_open
        elif DesiredPercentage > PreviousDesiredPercentage:
            # valve needs to open from old position to new position
            direction = "open"
            PulseTime_sec = (DesiredPercentage - PreviousDesiredPercentage) * (time_to_open / 100)
        elif DesiredPercentage < PreviousDesiredPercentage:
            # valve needs to close from old position to new position
            direction = "close"
            PulseTime_sec = (PreviousDesiredPercentage - DesiredPercentage) * (time_to_open / 100)
        else:
            # valve needs stay in position
            direction = "stay"
            PulseTime_sec = 0  # seconds

        # self.log(PulseTime_sec)
        # self.log(direction)

        # Translate seconds into Tasmota PulseTime codes. See also
        # https://github.com/arendst/Sonoff-Tasmota/wiki/Commands#main
        # first 11 seconds are in tenths of a second
        # remainder is in seconds

        if PulseTime_sec <= 11:
            PulseTime_sec = round(PulseTime_sec, 1)
            PulseTime = 1+PulseTime_sec*10
        elif PulseTime_sec > 11:
            PulseTime_sec = round(PulseTime_sec, 0)
            PulseTime = round(100 + PulseTime_sec, 0)
        # self.log("PulseTime: ")
        # self.log(PulseTime_sec)

        # Actual commands to valve, via MQTT

        if direction == "open":
            # stop valve closing
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/Power1", payload="off")
            # send required move time
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/PulseTime2", payload=PulseTime)
            # initiate movement for $PulseTime seconds
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/Power2", payload="on")
        elif direction == "close":
            # stop valve opening
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/Power2", payload="off")
            # send required move time
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/PulseTime1", payload=PulseTime)
            # initiate movement for $PulseTime seconds
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/Power1", payload="on")
        elif direction == "stay":
            # stop valve closing and opening
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/Power1", payload="off")
            self.call_service("mqtt/publish", topic="/zolder/ventilatie/sonoff/cmnd/Power2", payload="off")
        # write DesiredPercentage value to Home Assistant for next time
        self.set_value("input_number.zolder_ventilatie_old", DesiredPercentage)

        # Enable UI input after valve has stopped moving
        self.run_in(self.turn_on_handler, PulseTime_sec)

    def turn_on_handler(self, kwargs):
        self.call_service("group/set_visibility", entity_id="group.zolder_ventilatie", visible="True")
        self.call_service("group/set_visibility", entity_id="group.zolder_ventilatie_moving", visible="False")
