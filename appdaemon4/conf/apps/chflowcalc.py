import appdaemon.plugins.hass.hassapi as hass
import datetime

class chflowcalc(hass.Hass):
    def initialize(self):
        
        
        if self.args["combined_flow"] != "":
            self.listen_state(self.inputhandler, self.args["temp_combined"])
        else:
            self.listen_state(self.inputhandler, self.args["temp_combined"])
            # self.listen_state(self.inputhandler, self.args["temp_2"])

    def inputhandler(self, entity, attribute, old, new, kwargs):
        temp_1 = float(self.get_state(self.args["temp_1"]))
        temp_2 = float(self.get_state(self.args["temp_2"]))
        temp_combined = float(self.get_state(self.args["temp_combined"]))

        if self.args["combined_flow"] == "":
            combined_flow = 100
        else:
            combined_flow = float(self.get_state(self.args["combined_flow"]))

        # 'fab*Tab = fa*Ta + fb*Tb
        # Fcom*Tcom = F1*T1+F2*T2
        # Fcom = F1+F2

        # Fcom*Tcom = F1*T1+(Fcom-F1)*T2
        # Fcom*Tcom = F1*T1+Fcom*T2-F1*T2
        # Fcom*Tcom - Fcom*T2 = F1*T1-F1*T2
        # Fcom*(Tcom - T2) = F1*(T1-T2)
        # Fcom*(Tcom - T2)/(T1-T2) = F1

        if combined_flow == 0:
            flow_1 = 0
            flow_2 = 0
        else:
            if temp_1 == temp_2:
                flow_1 = 50
                flow_2 = 50
            else:
                flow_1 = round(combined_flow * (temp_combined - temp_2)/(temp_1 - temp_2))
                flow_2 = combined_flow - flow_1
            

            if flow_1 < 0 or flow_1 > 100:
                flow_1 = 0
                flow_2 = 0

        if flow_1 != 0:
            error = 0.3
            i = 0
            temp_combined_error = [temp_combined-error,temp_combined+error]
            temp_1_error = [temp_1 - error , temp_1 + error]
            temp_2_error = [temp_2 - error , temp_2 + error]

            flow_1_error = []
            flow_2_error = []

            for tcomb in temp_combined_error:
                for t1 in temp_1_error:
                    for t2 in temp_2_error:
                        if t1 != t2:
                            flow_1_error.append(round(combined_flow * (tcomb - t2)/(t1 - t2)))
                            #flow_2_error.append(combined_flow - flow_1_error(i))
                            #i = i+1
                        else:
                            flow_1_error.append(combined_flow/2)

            #self.log(flow_1_error)
            maxerror = round(max(flow_1_error) - flow_1)
            minerror = round(min(flow_1_error) - flow_1)
            
            
            #self.log("room SP is {} degrees".format(roomsp))
            #self.log("{} (+{}/{})%".format(flow_1,maxerror,minerror))

            displaytopic_1 = "{} (+{}/{})".format(flow_1,maxerror,minerror)
            displaytopic_2 = "{} (+{}/{})".format(flow_2,maxerror,minerror)
        else:
            displaytopic_1 = flow_1
            displaytopic_2 = flow_2
        
        self.call_service("mqtt/publish", topic=self.args["flowtopic_1"], payload=flow_1, retain=True)
        self.call_service("mqtt/publish", topic=self.args["flowtopic_2"], payload=flow_2, retain=True)
        self.call_service("mqtt/publish", topic=self.args["displaytopic_1"], payload=displaytopic_1, retain=True)
        self.call_service("mqtt/publish", topic=self.args["displaytopic_2"], payload=displaytopic_2, retain=True)

