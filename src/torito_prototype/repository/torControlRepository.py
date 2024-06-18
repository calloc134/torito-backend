from dbus import SystemBus, Interface
from stem import control
import socket
from time import sleep
from typing import Generator
import re


tagPhase = {
    'starting': 'Starting',
    'conn': 'Connecting to a relay',
    'conn_dir': 'Connecting to a relay directory',
    'conn_done_pt': "Connected to pluggable transport",
    'handshake_dir': 'Finishing handshake with directory server',
    'onehop_create': 'Establishing an encrypted directory connection',
    'requesting_status': 'Retrieving network status',
    'loading_status': 'Loading network status',
    'loading_keys': 'Loading authority certificates',
    'enough_dirinfo': 'Loaded enough directory info to build circuits',
    'ap_conn': 'Connecting to a relay to build circuits',
    'ap_conn_done': 'Connected to a relay to build circuits',
    'ap_conn_done_pt': 'Connected to pluggable transport to build circuits',
    'ap_handshake': 'Finishing handshake with a relay to build circuits',
    'ap_handshake_done': 'Handshake finished with a relay to build circuits',
    'requesting_descriptors': 'Requesting relay information',
    'loading_descriptors': 'Loading relay information',
    'conn_or': 'Connecting to the Tor network',
    'conn_done': "Connected to a relay",
    'handshake': "Handshaking with a relay",
    'handshake_or': 'Finishing handshake with first hop',
    'circuit_create': 'Establishing a Tor circuit',
    'done': 'Connected to the Tor network!'
}

class TorControlRepository: 
    deviceType: str
    torIp: str
    torPort: int
    manager: object

    def __init__(self, deviceType: str, torIp: str, torPort: int):
        self.deviceType = deviceType
        self.torIp = torIp
        self.torPort = torPort

        # dbusを初期化
        dbus = SystemBus()
        systemd = dbus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        self.manager = Interface(systemd, 'org.freedesktop.systemd1.Manager')

    # 購読のためのコールバックとして関数を受け取る
    def startTor(self) -> Generator[str, None, str]:

        # Linuxであればsystemctlを使ってtorを起動
        if self.deviceType == "Linux":
            try: 
                self.manager.StartUnit('tor.service', 'replace')
            except Exception as e:
                print(e)
                raise Exception(f"Failed to start tor: {e}")
        else: 
            print
            raise Exception(f"Unsupported device type: {self.deviceType}")
        
        # torが起動するまで待つ
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        count = 0
        while not sock.connect_ex((self.torIp, self.torPort)) == 0 and count < 10:
            sleep(1)
            count += 1

        tor_controller = control.Controller.from_port(port=9051)

        try:
            tor_controller.authenticate()
        except Exception as e:
            raise Exception(f"Failed to authenticate: {e}")
        
        # 購読を開始
        bootstrap_percent = 0
        previous_percent = 0

        while bootstrap_percent < 100:
            sleep(0.1)
            bootstrap_status = tor_controller.get_info("status/bootstrap-phase")
            bootstrap_percent = int(re.match('.* PROGRESS=([0-9]+).*', bootstrap_status).group(1))
            bootstrap_tag = re.search(r'TAG=(.*) +SUMMARY', bootstrap_status).group(1)
            if bootstrap_percent > previous_percent:
                previous_percent = bootstrap_percent

                if not bootstrap_tag in tagPhase:
                    print(f"Unknown tag: {bootstrap_tag}")
                    continue

                print(f"{tagPhase[bootstrap_tag]}: {bootstrap_percent}%")
                yield f"{tagPhase[bootstrap_tag]}: {bootstrap_percent}%"

        
