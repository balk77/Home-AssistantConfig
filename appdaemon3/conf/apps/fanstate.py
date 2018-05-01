import appdaemon.plugins.hass.hassapi as hass

class fanstate(hass.Hass):
    def initialize(self):
        # Listen for state change of ventilation requirements
        # self.log("   ")

        self.listen_state(self.setspeed, "input_select.fanstate")
        self.listen_state(self.setselector, "sensor.itho_lastidindex")


    def setspeed(self, entity, attribute, old, new, kwargs):
        self.log("   ")

        ## if Itho remote is used, override HASS automation for 10 minutes
        override = self.get_state("input_boolean.itho_remote_override")
        desiredState = self.get_state("input_select.fanstate")
        if override == "off":
            if desiredState == "full":
                newstate =  "4"
            elif desiredState == "high":
                newstate =  "3"
            elif desiredState == "medium":
                newstate =  "2"
            elif desiredState == "low":
                newstate =  "1"
            elif desiredState == "standby":
                newstate =  "0"
            elif desiredState == "high (10 min)":
                newstate =  "13"
            elif desiredState == "high (20 min)":
                newstate =  "23"
            elif desiredState == "high (30 min)":
                newstate =  "33"

            payload = "State,"+newstate
            self.log(payload)
            # Change the topic to your liking
            self.call_service("mqtt/publish", topic="/hass/itho/cmd", payload=payload)

            if desiredState == "1" or desiredState == "0":
                self.set_value("input_number.zolder_ventilatie", 100)

    def setselector(self, entity, attribute, old, new, kwargs):
        # If LastID is Itho remote, execute the following block
        LastIDindex = float(self.get_state("sensor.itho_lastidindex"))

        if LastIDindex != 0:
            # Activate override for 10 minutes
            status = self.set_state("input_boolean.itho_remote_override", state="on")

            # get state as set by Itho remote
            curr_fanstate = self.get_state("sensor.itho_ventilatie")
            self.log("new remote state =")
            self.log(curr_fanstate)

            if curr_fanstate == "0":
                desiredState = "standby"
            elif curr_fanstate == "1":
                desiredState = "low"
            elif curr_fanstate == "2":
                desiredState = "medium"
            elif curr_fanstate == "3":
                desiredState = "high"
            elif curr_fanstate == "4":
                desiredState = "full"
            elif curr_fanstate == "13":
                desiredState = "high (10 min)"
            elif curr_fanstate == "23":
                desiredState = "high (20 min)"
            elif curr_fanstate == "33":
                desiredState = "high (30 min)"


            if curr_fanstate:
                self.select_option("input_select.fanstate", desiredState)
            self.log(desiredState)

            # Disable override after 10 minutes
            self.run_in(self.setselector_delay, 600)
            curr_fanstate = None

    def setselector_delay(self, kwargs):
        status = self.set_state("input_boolean.itho_remote_override", state="off")
