import serial
import sys
import time


print("""
████████████████████████████████████  
██                                ██  
██  ████  ████  ████  ████  ████  ████
██  ████  ████  ████  ████  ████  ████
██  ████  ████  ████  ████  ████  ████
██  ████  ████  ████  ████  ████  ████
██  ████  ████  ████  ████  ████  ████
██                                ██  
████████████████████████████████████  
PIL SEVIYE OLCER - SERHAT MERAL
""")


def get_serial_port():
    try:
        return int(input("Sayısal port kodunu giriniz Com? :"))
    except:
        print("lütfen sayısal kod giriniz com5 portunu kullanıyorsanız '5' yazınız")

def value_bar(value: int):
    value = int(value)
    sys.stdout.flush()
    # print(f"\rOyun {3 - x} saniye sonra başlıyor...", end=" ")
    print(f'\r{"█" * value}{"▒" * (100 - value)} {value}%', end=' ')


def value_bar_test():
    value_bar(0)
    time.sleep(10)
    for i in range(10, 68):
        value_bar(i)
        time.sleep(.10)


value_bar_test()


'''
port = get_serial_port()
ser = serial.Serial(port, 9600)  # 'COMX' kısmını kullanmak istediğiniz seri port ile değiştirin



while True:
    if ser.in_waiting > 0:
        data = ser.readline().decode('utf-8').rstrip()
        try:
            value_bar(int(data))
        except:
            print("VERİ OKUMA HATASI")
            break


'''


