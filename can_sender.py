import cantools
import can


class CanSender:
    def __init__(self):
        self.bus = None # açılır açılmaz bus'a bağlanmasın diye,başlangıçta view çalışabilir

    def connect_to_bus(self): # tek sefer bağlansın her mesajda tekrardan bağlanmasın diye bu fonksiyonu yazdım

        if self.bus is None:
            self.bus = can.interface.Bus(bustype='pcan', channel='PCAN_USBBUS2', bitrate=500000)

    def send_can_message(self, frame_id, data, is_extended):
        try:
            self.connect_to_bus()
            msg = can.Message(arbitration_id=frame_id, data=data, is_extended_id = is_extended)
            self.bus.send(msg)
            print("Mesaj gönderildi.")

        except can.CanError as e:
            print(f"Hata oluştu: {e}")


    def view_can_data(self, msg_def, signal, value):  #----> aynı zamanda data kısmını yapıyor seçilen sinyal dışındakiler sıfır
        signals = msg_def.signals
        signal_dict = {}
        for sig in signals:
            name = sig.name
            if name == signal.name:
                signal_dict[name] = value
            else:
                signal_dict[name] = 0

        hex_msg = msg_def.encode(signal_dict)

        return hex_msg