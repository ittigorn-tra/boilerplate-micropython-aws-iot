import network


class Wlan:
    def __init__(self, ssid: str, pwd: str) -> None:
        self._ssid = ssid
        self._pwd = pwd
        self._client = network.WLAN(network.STA_IF)
        self._client.active(True)

    def is_connected(self):
        return self._client.isconnected()

    def get_ifconfig(self):
        return self._client.ifconfig()

    def connect(self):

        if not self.is_connected():
            print('connecting to network...')
            self._client.connect(self._ssid, self._pwd)
            while not self.is_connected():
                pass

        print('network config:', self.get_ifconfig())


# # how to use
# wlan = Wlan(ssid='xxx', psk='xxx')
# wlan.connect()
