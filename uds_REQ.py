

import can
class UDSRequest:
    def __init__(self, service_name, uds_data):
        self.service_name = service_name
        self.uds_data = uds_data
        self.dataList = uds_data[2:]


def build_uds_message(service: list, dataList: list):
    pci = (len(service) + len(dataList))
    final_message = [pci] + service + dataList
    return final_message




def tester_present_req():
    uds_msg = build_uds_message([0x3E] , [0x00])
    return UDSRequest("tester_present_REQ", uds_msg)



def read_data_by_identifier_req():
    uds_msg = build_uds_message([0x22], [0xF1,0x90])# [DID_High, DID_Low]
    return UDSRequest("read_data_by_identifier_REQ", uds_msg)



#
def ecu_reset_req(reset_type:list):
    uds_msg = build_uds_message([0x11], reset_type)
    return UDSRequest("ecu_reset_REQ", uds_msg)


#

def session_control_req(session_type: list):  # [0x01] veya [0x03]
    uds_msg = build_uds_message([0x10],session_type)
    return UDSRequest("session_control_REQ", uds_msg)



def clear_DTC_req(group_of_dtc: list):
    uds_msg = build_uds_message([0x14], group_of_dtc )
    return UDSRequest("clear_DTC_REQ", uds_msg)



def read_data_info_req(sub_function = [0x02], status_mask = [0xFF]):
    uds_msg = build_uds_message([0x19],sub_function + status_mask)
    return UDSRequest("read_data_info_REQ", uds_msg)



def uds_to_can(uds_msg:list):
    extended_data = uds_msg + ([0x00] * (8 - len(uds_msg)))
    can_message = can.Message(arbitration_id=0x7e0, data=extended_data, is_extended_id=False)
    return can_message




def main_request():
    bus = None
    try:
        bus = can.Bus(interface='pcan', channel='PCAN_USBBUS2', bitrate=500000, receive_own_messages=False)
        print("bus OK")
        message = uds_to_can(tester_present_req().uds_data)
        print("mesaj aaaaaaaaaaaaaaaaaaaa")
        bus.send(message)
        print(message)
        response_message = bus.recv(5)
        print("response mesajı: ")
        print(response_message)
    finally:
        if bus:
            bus.shutdown()

if __name__ == "__main__":
    main_request()




"""
bus = None
try:
    bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000, receive_own_messages=True)
    bus.reset()
    message = can.Message(arbitration_id=726, is_extended_id=False,
                          data=[0x03, 0x22, 0xF1, 0x90, 0x00, 0x00, 0x00, 0x00])
    bus.send(message)
    msg = bus.recv(timeout=1.0)
    print(msg)
finally:
    if bus:
        bus.shutdown()
"""

"""bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000)
message = can.Message(arbitration_id=726, data=[0x03, 0x22, 0xF1, 0x90])
bus.send(message)"""
