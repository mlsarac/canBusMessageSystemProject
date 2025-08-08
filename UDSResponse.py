from UDSRequest import UDSRequest 
import can
class UDSResponse:
    def __init__(self, original_request: UDSRequest, response_data):
        self.original_request = original_request
        self.response_data = response_data
        self.is_positive = True


def reconstruct_request_from_can(request_message: can.Message):
    request_uds = extract_uds_from_can(request_message)
    service_id = request_uds[1]
    service_name = determine_service_name(service_id)
    return UDSRequest(service_name, request_uds)


def determine_service_name(service_id: int):
    service_map = {
        0x3E: "tester_present_REQ",
        0x22: "read_data_by_identifier_REQ",
        0x11: "ecu_reset_REQ",
        0x10: "session_control_REQ",
        0x14: "clear_DTC_REQ",
        0x02: "read_data_info_REQ"
    }
    return service_map.get(service_id, "unknown_service")


def extract_uds_from_can(request_message: can.Message):
    pci = request_message.data[0]
    return request_message.data[0:pci + 1]


def build_uds_message(service: list, dataList: list):
    pci = (len(service) + len(dataList))
    final_message = [pci] + service + dataList
    return final_message


def uds_to_can(uds_msg: list):
    extended_data = uds_msg + ([0x00] * (8 - len(uds_msg)))
    can_message = can.Message(arbitration_id=0x7E8, data=extended_data, is_extended_id=False)
    return can_message


def read_data_by_identifier_resp(request: UDSRequest):
    if request.service_name != "read_data_by_identifier_REQ":
        raise ValueError("Yanlış message tipi!")
    else:
        data = [0x01, 0x02, 0x03, 0x04]
        uds_msg = build_uds_message([0x62], request.dataList + data)
        return UDSResponse("read_data_by_identifier_RESP", uds_msg)


# 333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333

def ecu_reset_resp(request: UDSRequest):
    if request.service_name != "ecu_reset_REQ":
        raise ValueError("Yanlış message tipi!")
    else:
        uds_msg = build_uds_message([0x51], request.dataList)
        return UDSResponse("ecu_reset_RESP", uds_msg)


def session_control_resp(request: UDSRequest):
    if request.service_name != "session_control_REQ":
        raise ValueError("Yanlış message tipi!")
    else:
        timing_params = [0x00, 0x32, 0x01, 0xF4]
        uds_msg = build_uds_message([0x50, request.dataList] + timing_params)
        return UDSResponse("session_control_RESP", uds_msg)


def clear_DTC_resp(request: UDSRequest):
    if request.service_name != "clear_DTC_REQ":
        raise ValueError("Yanlış message tipi!")
    else:
        uds_msg = build_uds_message([0x54], request.dataList)
        return UDSResponse("clear_DTC_RESP", uds_msg)


def read_data_info_resp(request: UDSRequest):
    P0171_dtc = [0x00, 0x17, 0x1A] + [0x08]  # ciddi arıza
    P0300_dtc = [0x00, 0x30, 0x0B] + [0x04]  # hafif arıza
    response_data = [0x02, 0xFF] + P0171_dtc + P0300_dtc
    uds_msg = build_uds_message([0x59], response_data)
    return UDSResponse("read_data_info_RESP", uds_msg)


def tester_present_resp(request: UDSRequest):
    if request.service_name != "tester_present_REQ":
        raise ValueError("Yanlış mesaj tipi!")
    else:
        uds_msg = build_uds_message([0x7E], request.dataList)
        return UDSResponse("tester_present_RESP", uds_msg)


def main_response():
    try:
        bus = bus = can.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=500000, receive_own_messages=False)
        print("bus calisiyor")
        print("Listening on PCAN_USBBUS1...")
        can_message = bus.recv(10)
        if can_message:
            print("MESAJ ALINDI : ")

        else:
            print("mesaj alınamadı")

        uds_request = reconstruct_request_from_can(can_message)

        response_data = None

        if uds_request.service_name == "tester_present_REQ":
            response_data = [0x02, 0x7E, 0x00]

        elif uds_request.service_name == "read_data_by_identifier_REQ":
            response_data = []

        elif uds_request.service_name == "ecu_reset_REQ":
            response_data = [0x02, 0x51, uds_request.uds_data[2]]

        elif uds_request.service_name == "session_control_REQ":
            response_data = [0x02, 0x50, uds_request.uds_data[2]]

        elif uds_request.service_name == "clear_DTC_REQ":
            response_data = [0x01, 0x54]

        elif uds_request.service_name == "read_data_info_REQ":
            response_data = []
        else:
            print("hata bas")

        uds_response = UDSResponse(uds_request, response_data)
        uds_response_data = uds_response.response_data
        response_message = uds_to_can(uds_response_data)

        bus.send(response_message)
        print(response_message)

    finally:
        if bus:
            bus.shutdown()

    pass


main_response()
