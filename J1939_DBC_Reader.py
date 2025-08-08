import cantools

db = cantools.database.load_file("DBC_fixed_cleaned.dbc")

def main():
    message_name =input("Mesaj adını girin: ")
    msg_def = db.get_message_by_name(message_name)

    signal_dict = {}
    for signal in msg_def.signals:
        signal_dict[signal.name] = 0

    print("Bu mesajdaki sinyaller: ")
    for name in signal_dict.keys():
        print(f"  🔸 {name}")

    signal_name = input("Sinyal adını girin: ")

    signal_value = float(input("Sinyal değerini girin: "))

    signal_dict[signal_name] = signal_value

    encode_data = msg_def.encode(signal_dict)
    print(encode_data)

main()


