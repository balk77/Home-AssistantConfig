import appdaemon.plugins.hass.hassapi as hass


class zwavecheck(hass.Hass):

    def initialize(self):
        
        check = 0
        arr = self.list_services()
        for x in range(len(arr)): 
            if arr[x]["domain"] == "zwave" and arr[x]["service"] == "set_config_parameter":
                self.log("Available: " + arr[x]["domain"] + " " + arr[x]["service"])
                check = 1
        

        if check == 1:
            # self.log("success")
            self.notify("Zwave ready @ AppDaemon start.",name="telegram")
        else:
            # self.log("fout")
            self.notify("Zwave not ready @ AppDaemon start.",name="telegram")

        self.listen_state(self.badkamertest, "input_boolean.badkamertest", old = "off", new = "on")
    
    def badkamertest(self, entity, attribute, old, new, kwargs):
        arr = self.list_services()
        for x in range(len(arr)): 
            if arr[x]["domain"] == "zwave" and arr[x]["service"] == "set_config_parameter":
                self.log(arr[x]["domain"])
                self.log(arr[x]["service"])

    
