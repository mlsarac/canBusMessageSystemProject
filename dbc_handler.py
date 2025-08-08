import cantools

class DBCHandler:
    def __init__(self, dbc_file = "DBC_fixed_cleaned.dbc"):
        self.db = cantools.database.load_file(dbc_file)

    def get_all_messages(self):
        return [msg.name for msg in self.db.messages]

    def get_all_signals(self, msg_name):
        try:
            msg = self.db.get_message_by_name(msg_name)
            return [sig.name for sig in msg.signals]
        except KeyError:
            return []

    def get_message_by_name(self, msg_name):
        return self.db.get_message_by_name(msg_name)

    def get_signal_by_name(self, msg_name, sig_name):
        msg = self.db.get_message_by_name(msg_name)
        sig= msg.get_signal_by_name(sig_name)
        return sig



