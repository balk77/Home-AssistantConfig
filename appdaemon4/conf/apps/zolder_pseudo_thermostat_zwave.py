import appdaemon.plugins.hass.hassapi as hass
import datetime
# from math import ceil


class zolderpseudothermostat(hass.Hass):
    def initialize(self):

        self.block = False

        # Listen for changes in raw thermostat
        # self.handle = self.listen_state(self.main, self.args['thermostat_raw_sp'],trigger="raw")
        
        # Listen for changes in frontend thermostat
        # self.handle = self.listen_state(self.main, self.args['frontendsp'],trigger="frontend")
        
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
                    self.log("setting sp to: "+str(frontend_sp))
                    self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
                    self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
            else:
                if self.now_is_between(self.args['weekend_morning_switch'],self.args['weekend_afternoon_switch']):
                    self.log("setting sp to: "+str(frontend_sp))
                    self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
                    self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)

    def switch_to_low_temp_weekend(self, entity):
        workday = self.get_state("binary_sensor.workday_sensor")
        self.call_service("input_boolean/turn_off", entity_id=self.args["thermostaat_override"])
        

        if workday == "off":
            frontend_sp = self.get_state(self.args['temp_low_sp'])
            self.call_service("climate/set_temperature", entity_id=self.args['frontend_climate_device'], temperature=frontend_sp)
            self.call_service("input_number/set_value", entity_id=self.args['input_number_setpoint'], value=frontend_sp)
    
    def switch_to_low_temp_week(self, entity):
        workday = self.get_state("binary_sensor.workday_sensor")
        self.call_service("input_boolean/turn_off", entity_id=self.args["thermostaat_override"])
        

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