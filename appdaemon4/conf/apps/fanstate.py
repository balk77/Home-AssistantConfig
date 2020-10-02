import appdaemon.plugins.hass.hassapi as hass
from datetime import datetime, timezone, timedelta

class fanstate(hass.Hass):
    def initialize(self):

        # time = datetime.now()

        # Listen for state change of ventilation requirements
        # self.log("   ")

        self.listen_state(self.setspeed, "input_select.fanstate")
        self.listen_state(self.setselector, "sensor.itho_lastidindex")
        #self.listen_state(self.setoverride, "input_select.override_fan_timer")
        self.listen_state(self.setoverride, "input_boolean.itho_remote_override")
        self.run_every(self.checkstate, datetime.now(), 15*60)


    def setspeed(self, entity, attribute, old, new, kwargs):
        # self.log("   ")

        ## if Itho remote is used, override HASS automation for 10 minutes
        override = self.get_state("input_boolean.itho_remote_override")
        
        
        if override == "off":

            desiredState = self.get_state("input_select.fanstate")
            self.log("desiredState: "+desiredState)

            self.sendstate(desiredState=desiredState)

 

    def sendstate(self, desiredState):
        desiredState=desiredState
        newstate=""
        
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
        self.call_service("mqtt/publish", topic="hass/itho/cmd", payload=payload)

        if newstate == "1" or newstate == "0":
                self.call_service("input_number/set_value", entity_id="input_number.zolder_ventilatie", value=100)

    

    def setselector(self, entity, attribute, old, new, kwargs):
        # If LastID is Itho remote, execute the following block
        LastIDindex = float(self.get_state("sensor.itho_lastidindex"))

        if LastIDindex != 0:
            # Activate override for 10 minutes
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.itho_remote_override") 

            # get state as set by Itho remote
            curr_fanstate = self.get_state("sensor.itho_ventilatie")

            self.sendstate(desiredState=curr_fanstate)
            self.log("new remote state ="+curr_fanstate)
            


            if curr_fanstate:
                self.select_option("input_select.fanstate", desiredState)
            self.log(desiredState)

            # Disable override after 10 minutes
            self.run_in(self.setselector_delay, 600)
            curr_fanstate = None

    def setselector_delay(self, kwargs):
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.itho_remote_override")
        self.call_service("input_select/select_option", entity_id="input_select.override_fan_timer", option="Uit")
    
    # def override_delay(self, kwargs)
    #     self.call_service("input_boolean/turn_off", entity_id="input_boolean.itho_remote_override")

    def setoverride(self, entity, attribute, old, new, kwargs):
        automation_override = self.get_state("input_boolean.itho_remote_override")

        if automation_override == "on":
            self.run_in(self.setselector_delay, 900)
   

    
    def checkstate(self, kwargs):

        current_fanstate = self.get_state("sensor.itho_ventilatie")
        self.log("Current fan state: "+current_fanstate)
        # desiredState = self.get_state("input_select.fanstate")

        self.sendstate(desiredState=current_fanstate)