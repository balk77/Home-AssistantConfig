import appdaemon.plugins.hass.hassapi as hass

class TelegramBotEventListener(hass.Hass):
    """Event listener for Telegram bot events."""

    def initialize(self):
        """Listen to Telegram Bot events of interest."""
        self.listen_event(self.receive_telegram_text, 'telegram_text')
        self.listen_event(self.receive_telegram_callback, 'telegram_callback')
        self.listen_event(self.receive_telegram_command, 'telegram_command')

    def receive_telegram_command(self, event_id, payload_event, *args):
        # command: "/thecommand"
        # args: "<any other text following the command>"
        # from_first: "<first name of the sender>"
        # from_last: "<last name of the sender>"
        # user_id: "<id of the sender>"
        # chat_id: "<origin chat id>"
        # chat: "<chat info>"
        command = payload_event['command']
        # self.log("lala")
        

        user_id = payload_event['user_id']
        if command == "/ventilatie":
            self.ventilatie(payload_event = payload_event)



    def ventilatie(self, payload_event, *args):
        self.log(payload_event['user_id'])
        user_id = payload_event['user_id']
        self.call_service('telegram_bot/send_message',
                          title='*Dumb automation*',
                          target=user_id,
                          message=msg,
                          disable_notification=True,
                          inline_keyboard=keyboard)


    def receive_telegram_text2(self, event_id, payload_event, *args):
        """Text repeater."""
        assert event_id == 'telegram_text'
        user_id = payload_event['user_id']
        msg = 'You said: ``` %s ```' % payload_event['text']
        keyboard = [[("Edit message", "/edit_msg"),
                     ("Don't", "/do_nothing")],
                    [("Remove this button", "/remove button")]]
        self.call_service('telegram_bot/send_message',
                          title='*Dumb automation*',
                          target=user_id,
                          message=msg,
                          disable_notification=True,
                          inline_keyboard=keyboard)

    def receive_telegram_text(self, event_id, payload_event, *args):

        assert event_id == 'telegram_text'
        self.log(payload_event['chat_id'])

        self.log(payload_event['text'])
        if payload_event['text'] == '/vakantie':  # Only Answer to callback query
            self.call_service('telegram_bot/answer_callback_query',
                              message='pang pang pang',
                              callback_query_id=callback_id)
        #msg = 'You said: ``` %s ```' % payload_event['text']
        
        if payload_event['text'] == "":
            self.log("ja")
        else:
            self.main_menu(payload_event = payload_event)
            
            

    def main_menu(self, payload_event, *args):
        
        user_id = payload_event['user_id']

        msg = "Roep status op"
        keyboard = [[("Vakantie", "/vakantie"),
                        ("Verlichting", "/verlichting")],
                        [("Ventilatie", "/ventilatie")]]
        self.call_service('telegram_bot/send_message',
                        title='*Hoofdmenu*',
                        target=user_id,
                        message=msg,
                        disable_notification=True,
                        inline_keyboard=keyboard)
    def send_message(self, payload_event, **kwargs):
        user_id = payload_event['user_id']
        self.log(kwargs['msg'])
        try:
            self.call_service('telegram_bot/edit_message',
                                chat_id=user_id,
                                message_id="last",
                                title="*"+kwargs['title']+"*",
                                message=kwargs['msg'])
                            
        except:
            try:
                self.call_service('telegram_bot/edit_message',
                                chat_id=user_id,
                                message_id="last",
                                message=kwargs['msg'])
            except:
                self.log("error")
                                              

    def receive_telegram_callback(self, event_id, payload_event, *args):

        """Event listener for Telegram callback queries."""
        assert event_id == 'telegram_callback'
        data_callback = payload_event['data']
        callback_id = payload_event['id']
        user_id = payload_event['user_id']
        # keyboard = ["Edit message:/edit_msg, Don't:/do_nothing",
        #             "Remove this button:/remove button"]
        keyboard = [[("Edit message", "/edit_msg"),
                     ("Don't", "/do_nothing")],
                    [("Remove this button", "/remove button")]]

        if data_callback == '/edit_msg':  # Message editor:
            # Answer callback query
            self.call_service('telegram_bot/answer_callback_query',
                              message='Editing the message!',
                              callback_query_id=callback_id,
                              show_alert=True)

            # Edit the message origin of the callback query
            msg_id = payload_event['message']['message_id']
            user = payload_event['from_first']
            title = '*Message edit*'
            msg = 'Callback received from %s. Message id: %s. Data: ``` %s ```'
            self.call_service('telegram_bot/edit_message',
                              chat_id=user_id,
                              message_id=msg_id,
                              title=title,
                              message=msg % (user, msg_id, data_callback),
                              inline_keyboard=keyboard)

        elif data_callback == '/remove button':  # Keyboard editor:
            # Answer callback query
            self.call_service('telegram_bot/answer_callback_query',
                              message='Callback received for editing the '
                                      'inline keyboard!',
                              callback_query_id=callback_id)

            # Edit the keyboard
            new_keyboard = keyboard[:1]
            self.call_service('telegram_bot/edit_replymarkup',
                              chat_id=user_id,
                              message_id='last',
                              inline_keyboard=new_keyboard)

        elif data_callback == '/do_nothing':  # Only Answer to callback query
            self.call_service('telegram_bot/answer_callback_query',
                              message='OK, you said no!',
                              callback_query_id=callback_id)
        elif data_callback == "/vakantie_set":
            self.toggle("input_boolean.vakantie")
            modus = self.get_state("input_boolean.vakantie")
            if modus == "on":
                modus = "aan"
            else:
                modus = "uit"
            msg = "Vakantiemodus is nu " + modus
            self.call_service('telegram_bot/send_message',
                              title='*Vakantiemodus*',
                              target=user_id,
                              message=msg,
                              disable_notification=True)
            self.main_menu(payload_event = payload_event)
        elif data_callback == "/vakantie":
            user_id = payload_event['user_id']
            modus = self.get_state("input_boolean.vakantie")


            if modus == "on":
                modus2 = "uit"
            else:
                modus2 = "aan"

            msg = 'Vakantiemodus: ``` %s ```' % modus

            # self.log(modus2)
            keyboard = [[("Zet " + modus2, "/vakantie_set")]]

            self.call_service('telegram_bot/send_message',
                              title='*Vakantiemodus*',
                              target=user_id,
                              message=msg,
                              disable_notification=True,
                              inline_keyboard=keyboard)
        elif data_callback == "/ventilatie":
            modus = self.get_state("input_select.fanstate")
            msg = 'Vemtilatiemodus: ``` %s ```' % modus
            keyboard = [
                        [
                            ("Low", "/ventilatie_set_low"),("Medium", "/ventilatie_set_medium")
                        ],
                        [
                            ("High", "/ventilatie_set_high"),("Full", "/ventilatie_set_full")
                        ]]

            self.call_service('telegram_bot/send_message',
                              title='*Ventilatiemodus*',
                              target=user_id,
                              message=msg,
                              disable_notification=True,
                              inline_keyboard=keyboard)
            #self.send_message(payload_event = payload_event, msg="jaja", title="jojo")                                          
        elif data_callback == "/ventilatie_set_low":
            self.set_state("input_select.fanstate", state="low")
            self.main_menu(payload_event = payload_event)
        elif data_callback == "/ventilatie_set_medium":
            self.set_state("input_select.fanstate", state="medium")
            self.main_menu(payload_event = payload_event)
        elif data_callback == "/ventilatie_set_high":
            self.set_state("input_select.fanstate", state="high")
            self.main_menu(payload_event = payload_event)
        elif data_callback == "/ventilatie_set_full":
            self.set_state("input_select.fanstate", state="full")
            self.main_menu(payload_event = payload_event)
