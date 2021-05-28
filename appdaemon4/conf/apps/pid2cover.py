import appdaemon.plugins.hass.hassapi as hass

class pid2cover(hass.Hass):
    def initialize(self):
        self.listen_state(self.inputhandler, "input_number.radiator_dide_position")
        self.status = "on"
        
        self.listen_state(self.startup, "binary_sensor.status_radiator_dide", old="off", new="on")
        
        self.listen_state(self.startup, "input_boolean.reset_radiator_dide", old="off", new="on")
        
        # self.run_in(self.startup, 1)
        # self.startup(1,1,1,1,1)

    def inputhandler(self, entity, attribute, old, new, kwargs):
        current_cover_position = float(self.get_state("cover.radiator_dide", attribute="current_position"))
        required_cover_position = float(self.get_state("input_number.radiator_dide_position"))
        cover_state = self.get_state("cover.radiator_dide" )
        # self.log(current_cover_position)
        # self.log(required_cover_position)
        # self.log(cover_state)

        if current_cover_position != required_cover_position and (cover_state == "open" or cover_state == "closed") and self.status == "on":
            # self.log("changing state to")
            # self.log(required_cover_position)
            self.call_service("cover/set_cover_position", entity_id="cover.radiator_dide", position=required_cover_position)

    def startup(self, entity, attribute, old, new, kwargs):
        self.status = "off"
        # self.log("opening valve")
        self.run_in(self.callservice, 2, position=100)
        # self.log("closing valve")
        self.run_in(self.callservice, 20, position=0)
        
        self.call_service("input_number/set_value", entity_id="input_number.dide_radiator_intgegraal", value=99999)
        self.call_service("input_number/set_value", entity_id="input_number.dide_radiator_intgegraal", value=600)
        self.status = "on"
        # self.log("bootup reset")



    
    def callservice(self, args):
        # self.log(args['position'])
        # self.log(args)
        self.call_service("cover/set_cover_position", entity_id="cover.radiator_dide", position=args['position'])

