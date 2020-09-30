import appdaemon.plugins.hass.hassapi as hass
import datetime
# from math import ceil


class scheduletest(hass.Hass):
    def initialize(self):
        
        # schedule low temp
        weekend_sleeptime_switch_time = datetime.datetime.strptime(self.args['weekend_sleeptime_switch'],'%H:%M:%S').time()
        week_sleeptime_switch_time = datetime.datetime.strptime(self.args['week_sleeptime_switch'],'%H:%M:%S').time()


        
        self.log(weekend_sleeptime_switch_time)
        self.log(type(weekend_sleeptime_switch_time))

        self.run_daily(self.switch_to_low_temp_weekend, weekend_sleeptime_switch_time)
        self.run_daily(self.switch_to_low_temp_week, week_sleeptime_switch_time)

        # Schedule to hi temp
        weekend_afternoon_switch_time = datetime.datetime.strptime(self.args['weekend_afternoon_switch'],'%H:%M:%S').time()
        week_afternoon_switch_time = datetime.datetime.strptime(self.args['week_afternoon_switch'],'%H:%M:%S').time()
        
        self.run_daily(self.switch_to_hi_temp_weekend, weekend_afternoon_switch_time)
        self.run_daily(self.switch_to_hi_temp_week, week_afternoon_switch_time)

    def switch_to_low_temp_weekend(self, entity):
        self.log("pong")
        self.call_service('notify/telegram', message="switch_to_low_temp_weekend")
    def switch_to_low_temp_week(self, entity):
        self.log("pong")
        self.call_service('notify/telegram', message="switch_to_low_temp_week")
    def switch_to_hi_temp_weekend(self, entity):
        self.log("pong")
        self.call_service('notify/telegram', message="switch_to_hi_temp_weekend")
    def switch_to_hi_temp_week(self, entity):
        self.log("pong")
        self.call_service('notify/telegram', message="switch_to_hi_temp_week")