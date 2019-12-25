import appdaemon.plugins.hass.hassapi as hass
import requests
import datetime

from datetime import timedelta


class vakantie(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler_on, "input_boolean.vakantie", new="on")
        self.listen_state(self.inputhandler_off, "input_boolean.vakantie", new="off")

    def inputhandler_on(self, entity, attribute, old, new, kwargs):
        now = datetime.datetime.now()
        start = now.strftime("%Y-%m-%dT%H:%M:00")

        end = now + timedelta(days=32)
        end = end.strftime("%Y-%m-%dT%H:%M:00")

        self.log(start)
        self.log(end)

        

        # Inform through Telegram
        self.notify("Vakantiemodus ingeschakeld","telegram")
        # self.call_service('notify/telegram', message="Vakantiemodus ingeschakeld")
        
        # Switch thermostat to vacation mode
        headers = {'Content-type': 'application/json'}
        myurl = "http://192.168.0.9:8124"

        command1 = "/bridge/heatingCircuits/hc1/holidayMode/start"
        body1 = start

        command2 = "/bridge/heatingCircuits/hc1/holidayMode/end"
        body2 = end


        command3 = "/bridge/heatingCircuits/hc1/holidayMode/activated"
        body3 = "on"

        r1 = requests.post(myurl+command1, verify=False, json={"value": body1}, headers = headers)
        self.log(r1.status_code)
        self.log(r1.text)

        r2 = requests.post(myurl+command2, verify=False, json={"value": body2}, headers = headers)
        self.log(r2.status_code)
        self.log(r2.text)

        r3 = requests.post(myurl+command3, verify=False, json={"value": body3}, headers = headers)
        self.log(r3.status_code)
        self.log(r3.text)

    def inputhandler_off(self, entity, attribute, old, new, kwargs):
        self.call_service('notify/telegram', message="Vakantiemodus uitgeschakeld")
        
        # Switch off thermostat vacation mode
        headers = {'Content-type': 'application/json'}
        myurl = "http://192.168.0.9:8124"
        command = "/bridge/heatingCircuits/hc1/holidayMode/activated"
        body = "off"

        r2 = requests.post(myurl+command, verify=False, json={"value": body}, headers = headers)
        self.log(r2.status_code)
        self.log(r2.text)

