from PyQt5.QtWidgets import QApplication
from can_ui import CANMessageSenderUI
from dbc_handler import DBCHandler
from can_sender import CanSender

app = QApplication([])

ui = CANMessageSenderUI()
dbc = DBCHandler()
can = CanSender()


ui.msg_combo.addItems(dbc.get_all_messages())

def on_message_selected():

     #seçim yapılmadıysa
     if ui.msg_combo.currentText() == "Seçiniz":
          return

     ui.sig_combo.clear()
     msg = dbc.get_message_by_name(ui.msg_combo.currentText())

     if msg is None:
          ui.output_display.append("Message not found")
          return

     if not msg.signals:
          ui.output_display.append("This message has no signals defined.")
          return

     signal_names = [s.name for s in msg.signals]
     ui.sig_combo.clear()
     ui.sig_combo.addItems(signal_names)
     ui.sig_combo.setCurrentIndex(0)


     #seçinizle ilgili sorun var

ui.msg_combo.currentTextChanged.connect(on_message_selected)


def on_signal_selected():

     #burası seçilwn sinyale göre value tipi ne olmalı kısmı

     msg_name = ui.msg_combo.currentText()
     selected_signal_name = ui.sig_combo.currentText()

     # seçim yapılmadıysa
     if not msg_name or not selected_signal_name or ui.sig_combo.currentText() == "Select":
          return

     selected_signal = dbc.get_signal_by_name(msg_name, selected_signal_name)######
     signal_unit = selected_signal.unit
     ui.unit_label.setText(signal_unit)

     min_val = selected_signal.minimum
     max_val = selected_signal.maximum
     if min_val is not None and max_val is not None:
          ui.range_label.setText(f"Range: {min_val} to {max_val}")
     else:
          ui.range_label.setText("")

     # sinyal value'su seçilecek mi girilecek mi
     #sig.choices bir sözlüktür (dict), varsa True döner
     # seçilecek ise

     if(selected_signal.choices):
          ui.val_input.hide()
          ui.val_combo.show()

          value_list =[]

          for key, desc in selected_signal.choices.items():
               value_list.append(f"{key} - {desc}")
          ui.val_combo.clear()
          ui.val_combo.addItems(value_list)


          # type checking yapılacak

     # girilecek ise
     else:
          ui.val_combo.hide()
          ui.val_input.show()

         #type checking yapılacak

ui.sig_combo.currentTextChanged.connect(on_signal_selected)

def prepare_can_message():
     msg_name = ui.msg_combo.currentText()
     sig_name = ui.sig_combo.currentText()

     if msg_name == "Seçiniz" or sig_name == "Seçiniz":
          ui.output_display.append("Lütfen geçerli bir mesaj ve sinyal seçin.")
          return None,None,None


     msg = dbc.get_message_by_name(ui.msg_combo.currentText())
     sig = dbc.get_signal_by_name(ui.msg_combo.currentText(),ui.sig_combo.currentText())

     value = None

     if ui.val_input.isVisible():
          try:
               value = float(ui.val_input.text())

          except ValueError:
               ui.output_display.append("Girilen değer geçersiz ")
               return None,None,None

          if (sig.minimum is not None or sig.maximum is not None):
               if not (sig.minimum <= value <= sig.maximum):
                    ui.output_display.append(f"Value is not in range. Range : {sig.minimum},{sig.maximum}")


     elif ui.val_combo.isVisible():
          try:
               # seçeneklerin başındaki index
               value = int(ui.val_combo.currentText().split(" - ")[0])

          except (ValueError, IndexError) :
               ui.output_display.append("Seçim type hatası var ")
               return None,None,None

          if (sig.minimum is not None and sig.maximum is not None): # bu kısmı anlamadım ama seçeneklerdeki bazı sinyaller range dışı !!??? , o yüzden eklendi
               if not (sig.minimum <= value <= sig.maximum):
                    ui.output_display.append(f"Seçim geçersiz. Bu sinyal için aralık: {sig.minimum} - {sig.maximum}")
                    return None, None, None

     else:#değer girişi yapılmadıysa
          ui.output_display.append("input girisi yapılmadı ")
          return None,None,None
     return msg, sig, value

def on_view_clicked():
     msg, sig, value = prepare_can_message()

     if msg is None or sig is None or value is None:
          return

     else:
          try:
               hex_msg = hex(msg.frame_id) + (can.view_can_data(msg, sig, value)).hex()
               ui.output_display.append("Can message viewed . Message : " + hex_msg)

          except Exception as e:
               ui.output_display.append(f"Mesaj oluştururken hata oldu {str(e)}")


ui.view_btn.clicked.connect(on_view_clicked)

def on_send_bus_clicked():

     msg, sig, value = prepare_can_message()

     if msg is None or sig is None or value is None:
          return

     else:
          try:
               data = can.view_can_data(msg,sig,value)
               hex_message = hex(msg.frame_id) + (can.view_can_data(msg, sig, value)).hex()  #----------------------------------------------------------------
               ui.output_display.append("Message : " + hex_message) #isteğe göre silinebilir, bus'a gönderirken aynı zamanda mesajı basıyor ------------------
               is_extended = msg.is_extended_frame

               can.send_can_message(msg.frame_id, data, is_extended)  #**** try except eklenecek bus bağlanmasa da gönderildi mesajı basıyor
               ui.output_display.append("Can message send.")


          except Exception as e:
               ui.output_display.append(f"Mesaj gönderilirken hata oldu {str(e)}")


ui.send_btn.clicked.connect(on_send_bus_clicked)

ui.show()
app.exec_()




