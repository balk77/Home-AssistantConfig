import appdaemon.plugins.hass.hassapi as hass
import datetime
import time

class sousvide(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, "input_boolean.sousvide_timer", new="on")

        self.listen_state(self.switch_on_boolean, "sensor.sous_vide_status", new="running")

        self.listen_state(self.cancel_sous_timer1, "sensor.sous_vide_status", old="running")

        self.listen_state(self.cancel_sous_timer2, "input_boolean.sousvide_timer", new="off")
        self.listen_state(self.cancel_sous_timer2, "input_boolean.sousvide_active", new="off")

    def switch_on_boolean(self, entity, attribute, old, new, kwargs):
        
        self.call_service("input_boolean/turn_on", entity_id="input_boolean.sousvide_active")

    def cancel_sous_timer1(self, entity, attribute, old, new, kwargs):
        
        # self.log("Canceling timer")
        # self.cancel_timer(self.timer_on)
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.sousvide_timer")
        self.call_service("input_boolean/turn_off", entity_id="input_boolean.sousvide_active")

    def cancel_sous_timer2(self, entity, attribute, old, new, kwargs):
        
        self.log("Canceling timer")
        self.cancel_timer(self.timer_on)
        

    def inputhandler(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()
        endtime = self.get_state("input_datetime.sousvidefinish")
        set_hour = self.get_state("input_datetime.sousvidefinish", attribute="hour")
        set_minute = self.get_state("input_datetime.sousvidefinish", attribute="minute")

        offset_hour = self.get_state("input_datetime.sousvidelengte", attribute="hour")
        offset_minute = self.get_state("input_datetime.sousvidelengte", attribute="minute")
        target_temp = self.get_state("input_number.sousvidetemp")
        # self.log(uur)
        
        if datetime.datetime(now.year,now.month,now.day,set_hour,set_minute) < datetime.datetime.now():
            self.log("morgen")
            daydelta = datetime.timedelta(days=1)
        else:
            self.log("vandaag")
            daydelta = datetime.timedelta(days=0)

        end_time = datetime.datetime(now.year,now.month,now.day,set_hour,set_minute) + daydelta
        start_time = end_time - datetime.timedelta(hours=offset_hour,minutes=offset_minute)

        self.log("Starttijd is {} ".format(start_time))
        self.log("Eindtijd is {} ".format(end_time))

        if start_time < datetime.datetime.now() + datetime.timedelta(seconds=5):
            # start de sous vide meteen
            # stel de eind tijd opnieuw in
            end_time = datetime.datetime.now() + datetime.timedelta(hours=offset_hour,minutes=offset_minute)
            self.call_service("mqtt/publish", topic="anova/command/temp", payload=target_temp)
            self.timer_on = self.run_in(self.initsousvide, 1, temperature=target_temp)
        else:
            self.call_service("mqtt/publish", topic="anova/command/temp", payload=target_temp)
            self.timer_on = self.run_at(self.initsousvide, start_time, temperature=target_temp)
        
        

            
    def initsousvide(self, temperature):
        temperature = temperature["temperature"]
        self.call_service("mqtt/publish", topic="anova/command/temp", payload=temperature)
        self.handle = self.run_in(self.startsousvide, 10, temperature=temperature)

    def startsousvide(self, temperature):
        #temperature = temperature["temperature"]
        target_temp = self.get_state("input_number.sousvidetemp")
        device_target_temp = self.get_state("sensor.sous_vide_target_temperature")
        # test if device target temperature is equal to desired target temperature
        if target_temp == device_target_temp:
            self.log("start Sous Vide met temperatuur {}".format(target_temp))
            self.call_service("input_boolean/turn_on", entity_id="input_boolean.sousvide_active")
        else:
            self.log("target_temp = {}".format(target_temp))
            self.log("device target_temp = {}".format(device_target_temp))
            self.handle = self.run_in(self.initsousvide, 10, temperature=target_temp)
