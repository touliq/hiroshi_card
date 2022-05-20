import requests
import time
PP_ADDRESS = "http://172.19.74.33"
def test1():
    PP_CHANNELS = ["gyrX","gyrY","gyrZ"]
  #  PP_CHANNELS = ["pressure"]
    PP_CHANNELS_COUNT = len(PP_CHANNELS)

    M_CONTROLS = [70]
    M_CHANNEL = 0

    starturl = PP_ADDRESS + "/control?cmd=start"
    requests.get(starturl)

    while True:
        url = PP_ADDRESS + "/get?" + ("&".join(PP_CHANNELS))
        data = requests.get(url=url).json()
        for i, control in enumerate(M_CONTROLS):
           # print(data["buffer"])
            value = data["buffer"][PP_CHANNELS[i]]["buffer"][0]
            # valueY = data["buffer"][PP_CHANNELS[i]]["buffer"][0]
            # valueZ = data["buffer"][PP_CHANNELS[i]]["buffer"][0]

            print (i, value )
        
            time.sleep(0.2)
def test2():
    starturl = PP_ADDRESS + "/control?cmd=start"
    requests.get(starturl)
    while True:
        pass


test1();
