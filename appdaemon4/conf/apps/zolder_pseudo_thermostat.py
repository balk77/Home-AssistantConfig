import appdaemon.plugins.hass.hassapi as hass
import datetime
# from math import ceil


class zolderpseudothermostat(hass.Hass):
    def initialize(self):

        self.block = False

        # Listen for changes in raw thermostat
        # self.handle = self.listen_state(self.main, self.args['thermostat_raw_sp'],trigger="raw")
        
        # Listen for changes in frontend thermostat
        self.handle = self.listen_state(self.main, self.args['frontendsp'],trigger="frontend")
        
        # Listen for motion @ zolder
        self.handle = self.listen_state(self.zolder_motion, "input_boolean.zolder_beweging")
        
        # schedule low temp
        weekend_sleeptime_switch_time = datetime.datetime.strptime(self.args['weekend_sleeptime_switch'],'%H:%M:%S').time()
        week_sleeptime_switch_time = datetime.datetime.strptime(self.args['week_sleeptime_switch'],'%H:%M:%S').time()

        self.run_daily(self.switch_to_low_temp_weekend, weekend_sleeptime_switch_time)
        self.run_daily(self.switch_to_low_temp_week, week_sleeptime_switch_time)

        # Schedule to hi temp
        weekend_afternoon_switch_time = datetime.datetime.strptime(self.args['weekend_afternoon_switch'],'%H:%M:%S').time()
        week_afternoon_switch_time = datetime.datetime.strptime(self.args['week_afternoon_switch'],'%H:%M:%S').time()
        
        self.run_daily(self.switch_to_hi_temp_weekend, weekend_afternoon_switch_time)
        self.run_daily(self.switch_to_hi_temp_week, week_afternoon_switch_time)

    def main(self, entity, attribute, old, new, kwargs):
        self.log(self.block)
        trigger = kwargs['trigger']

        frontend_climate_device = self.args['frontend_climate_device']
        raw_climate_device = self.args['raw_climate_device']
        frontend_sp = float(self.get_state(frontend_climate_device, attribute="temperature"))
        raw_sp = float(self.get_state(raw_climate_device, attribute="temperature"))

        if self.block == False:
            self.block = True
            if trigger == "raw":
                
                self.log("(raw2fe) received_raw_sp: "+str(raw_sp))
                self.log("(raw2fe) frontend_sp: "+str(frontend_sp))

                # Test if received set point is equal to hass set point
                # if so: it means that SP change is initiated by home assistant
                # in that case: do nothing
                if frontend_sp == raw_sp or self.args["thermostaat_override"] == "on":
                    self.log("do nothing")
                else:
                    # self.call_service("mqtt/publish", topic=self.args["settopic"], payload=frontend_sp)
                    
                    self.log("(raw2fe) set "+self.args['frontend_climate_device']+" to "+str(raw_sp))
                    self.call_service("input_boolean/turn_on", entity_id=self.args["thermostaat_override"])
                    self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=raw_sp)
                    self.log("(raw2fe) thermostaat_override ON")
                    
                    self.run_in(self.restore_temperature, self.args["timeout"],restore_temp=frontend_sp)

            elif trigger == "frontend":
                # self.log(data)
                thermostaat_override = self.get_state(self.args["thermostaat_override"])
                
                self.log("(frontend_to_raw) Frontend SP: "+str(frontend_sp))
                self.log("(frontend_to_raw) raw sp: "+str(raw_sp))
                self.log("(frontend_to_raw) thermostaat_override: "+thermostaat_override)
                if frontend_sp != raw_sp and thermostaat_override == "off":
                    self.handle = self.call_service("climate/set_temperature", entity_id=self.args['raw_climate_device'], temperature=frontend_sp)
            self.run_in(self.unblock,10)
                    
    def unblock(self, kwargs):
        self.block = False
        # self.log(self.block)

                       
    def restore_temperature(self, kwargs):
        self.log("(restore_temperature) restore_temperature: "+str(kwargs["restore_temp"]))
        # self.call_service("mqtt/publish", topic=self.args["settopic"], payload=kwargs["restore_temp"])
        self.call_service("input_boolean/turn_off", entity_id=self.args["thermostaat_override"])
        self.log("(restore_temperature) thermostaat_override OFF")

        workday = self.get_state("binary_sensor.workday_sensor")
        zolder_beweging = self.get_state("input_boolean.zolder_beweging")
        temp_high_sp = self.get_state(self.args['temp_high_sp'])
        temp_low_sp = self.get_state(self.args['temp_low_sp'])

        if zolder_beweging == "on":
            afternoon_sp = temp_high_sp
        else:
            afternoon_sp = temp_low_sp

        if workday == "on":
            if self.now_is_between(self.args['week_morning_switch'],self.args['week_afternoon_switch']):
                self.log("restore to: "+str(afternoon_sp))
                self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=afternoon_sp)
                self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=afternoon_sp)
            elif self.now_is_between(self.args['week_afternoon_switch'],self.args['week_morning_switch']):
                self.log("restore to: "+str(temp_low_sp))
                self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=temp_low_sp)
                self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=temp_low_sp)
        else:
            if self.now_is_between(self.args['weekend_morning_switch'],self.args['weekend_afternoon_switch']):
                self.log("restore to: "+str(afternoon_sp))
                self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=afternoon_sp)
                self.call_service("climate/set_temperature", entity_id=self.args['raw_climate_device'], temperature=afternoon_sp)
                self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=afternoon_sp)
            elif self.now_is_between(self.args['weekend_afternoon_switch'],self.args['weekend_morning_switch']):
                self.log("restore to: "+str(temp_low_sp))
                self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=temp_low_sp)
                self.call_service("climate/set_temperature", entity_id=self.args['raw_climate_device'], temperature=temp_low_sp)
                self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=temp_low_sp)


    def zolder_motion(self, entity, attribute, old, new, kwargs):
        # self.log("zolder motion")
        workday = self.get_state("binary_sensor.workday_sensor")
        zolder_beweging = self.get_state("input_boolean.zolder_beweging")

        # self.log("zolderbeweging = "+zolder_beweging)

        override = self.get_state(self.args["thermostaat_override"])

        if override == "off":
            temp_high_sp = self.get_state(self.args['temp_high_sp'])
            temp_low_sp = self.get_state(self.args['temp_low_sp'])
            if zolder_beweging == "on":
                frontend_sp = temp_high_sp
            else:
                frontend_sp = temp_low_sp
            
            # self.log("frontend_sp = "+str(frontend_sp))

            if workday == "on":
                if self.now_is_between(self.args['week_morning_switch'],self.args['week_afternoon_switch']):
                    # self.log("setting sp to: "+str(frontend_sp))
                    self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
                    self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
            else:
                if self.now_is_between(self.args['weekend_morning_switch'],self.args['weekend_afternoon_switch']):
                    # self.log("setting sp to: "+str(frontend_sp))
                    self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
                    self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)

    def switch_to_low_temp_weekend(self, entity):
        workday = self.get_state("binary_sensor.workday_sensor")

        if workday == "off":
            frontend_sp = self.get_state(self.args['temp_low_sp'])
            self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
            self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
    
    def switch_to_low_temp_week(self, entity):
        workday = self.get_state("binary_sensor.workday_sensor")

        if workday == "on":
            frontend_sp = self.get_state(self.args['temp_low_sp'])
            self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
            self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)

    def switch_to_hi_temp_weekend(self, entity):
        workday = self.get_state("binary_sensor.workday_sensor")

        if workday == "off":
            frontend_sp = self.get_state(self.args['temp_high_sp'])
            self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
            self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
    
    def switch_to_hi_temp_week(self, entity):
        workday = self.get_state("binary_sensor.workday_sensor")

        if workday == "on":
            frontend_sp = self.get_state(self.args['temp_high_sp'])
            self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
            self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)



## parkinglot

        # today = datetime.date.today()


        # weekend_morning_switch_time = datetime.datetime.strptime(self.args['weekend_morning_switch'],'%H:%M').time()
        # weekend_afternoon_switch_time = datetime.datetime.strptime(self.args['weekend_afternoon_switch'],'%H:%M').time()
        
        # week_morning_switch_time = datetime.datetime.strptime(self.args['week_morning_switch'],'%H:%M').time()
        # week_afternoon_switch_time = datetime.datetime.strptime(self.args['week_afternoon_switch'],'%H:%M').time()

        # now_time = datetime.datetime.now().time()


        
        # self.log(weekend_morning_switch_time.strftime("%H:%M"))
        # self.log(now_time)

        # if workday == "on":
            # vroege ochtend
            # morning_switch_time = datetime.datetime.strptime(self.args['week_morning_switch'],'%H:%M:%S').time()
            # afternoon_switch_time = datetime.datetime.strptime(self.args['week_afternoon_switch'],'%H:%M:%S').time()
            
            # if self.now_is_between(self.args['week_morning_switch'],self.args['week_afternoon_switch']):
            # morning_switch_time < now_time < afternoon_switch_time:
                # self.log("middag")
                # self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
                # self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
            
            
        # else:
            # morning_switch_time = datetime.datetime.strptime(self.args['weekend_morning_switch'],'%H:%M:%S').time()
            # afternoon_switch_time = datetime.datetime.strptime(self.args['weekend_afternoon_switch'],'%H:%M:%S').time()

            # if self.now_is_between(self.args['weekend_morning_switch'],self.args['weekend_afternoon_switch']):
            # morning_switch_time < now_time < afternoon_switch_time:
                # self.log("middag")
                # self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
                # self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)


            # if weekend_morning_switch_time < now_time < weekend_afternoon_switch_time:
            #     self.log("middag")
            #     self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
            #     self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
        
        # if morning_switch_time < now_time < afternoon_switch_time:
        #         # self.log("middag")
        #         self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
        #         self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
            
        # self.log(weekend_morning_switch)
        
        # datetime.datetime.strptime('18:30','%H:%M')