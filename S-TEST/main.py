import sys
import socket
import requests
import json
from PyQt5 import QtWidgets

class PacketSenderApp(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self.aramayi_baslat()

    def aramayi_baslat(self):
        self.setWindowTitle('N-TEST')

        with open("styles.css", "r") as f:
            self.setStyleSheet(f.read())

        self.paket_gonder_tab = QtWidgets.QWidget()
        self.paket_gonder_layout = QtWidgets.QVBoxLayout()

        self.ip_label = QtWidgets.QLabel('IP Adresi:', self)
        self.paket_gonder_layout.addWidget(self.ip_label)
        self.ip_input = QtWidgets.QLineEdit()
        self.paket_gonder_layout.addWidget(self.ip_input)

        self.port_label = QtWidgets.QLabel('Port:')
        self.paket_gonder_layout.addWidget(self.port_label)
        self.port_input = QtWidgets.QLineEdit()
        self.paket_gonder_layout.addWidget(self.port_input)

        self.paket_turu_label = QtWidgets.QLabel('Paket Türü:')
        self.paket_gonder_layout.addWidget(self.paket_turu_label)
        self.paket_turu_combo = QtWidgets.QComboBox()
        self.paket_turu_combo.addItems(['TCP', 'UDP', 'HTTP'])
        self.paket_gonder_layout.addWidget(self.paket_turu_combo)

        self.http_yontemi_label = QtWidgets.QLabel('HTTP Yöntemi:')
        self.paket_gonder_layout.addWidget(self.http_yontemi_label)
        self.http_yontemi_combo = QtWidgets.QComboBox()
        self.http_yontemi_combo.addItems(['GET', 'POST'])
        self.paket_gonder_layout.addWidget(self.http_yontemi_combo)

        self.user_agent_label = QtWidgets.QLabel('User-Agent Seç:', self)
        self.paket_gonder_layout.addWidget(self.user_agent_label)
        self.user_agent_combo = QtWidgets.QComboBox()
        self.paket_gonder_layout.addWidget(self.user_agent_combo)

        self.zaman_asimi_label = QtWidgets.QLabel('Zaman Aşımı:')
        self.paket_gonder_layout.addWidget(self.zaman_asimi_label)
        self.zaman_asimi_input = QtWidgets.QLineEdit()
        self.paket_gonder_layout.addWidget(self.zaman_asimi_input)

        self.paket_icerigi_label = QtWidgets.QLabel('Paket İçeriği:')
        self.paket_gonder_layout.addWidget(self.paket_icerigi_label)
        self.paket_icerigi_input = QtWidgets.QTextEdit()
        self.paket_icerigi_input.setMinimumHeight(100)
        self.paket_gonder_layout.addWidget(self.paket_icerigi_input)

        self.yanit_label = QtWidgets.QLabel('Alınan Yanıt:')
        self.paket_gonder_layout.addWidget(self.yanit_label)
        self.yanit_output = QtWidgets.QTextEdit()
        self.yanit_output.setReadOnly(True)
        self.yanit_output.setMinimumHeight(100)
        self.paket_gonder_layout.addWidget(self.yanit_output)

        self.gonder_button = QtWidgets.QPushButton('Gönder')
        self.gonder_button.clicked.connect(self.paket_gonder)
        self.paket_gonder_layout.addWidget(self.gonder_button)

        self.paket_gonder_tab.setLayout(self.paket_gonder_layout)

        self.api_sorgu_tab = QtWidgets.QWidget()
        self.api_sorgu_layout = QtWidgets.QVBoxLayout()

        self.api_label = QtWidgets.QLabel('API URL:')
        self.api_sorgu_layout.addWidget(self.api_label)
        self.api_input = QtWidgets.QLineEdit()
        self.api_sorgu_layout.addWidget(self.api_input)

        self.user_agent_label_api = QtWidgets.QLabel('User-Agent Seç:', self)
        self.api_sorgu_layout.addWidget(self.user_agent_label_api)
        self.user_agent_combo_api = QtWidgets.QComboBox()
        self.api_sorgu_layout.addWidget(self.user_agent_combo_api)

        self.api_yanit_label = QtWidgets.QLabel('Yanıt:')
        self.api_sorgu_layout.addWidget(self.api_yanit_label)
        self.api_yanit_output = QtWidgets.QTextEdit()
        self.api_yanit_output.setReadOnly(True)
        self.api_yanit_output.setMinimumHeight(100)
        self.api_sorgu_layout.addWidget(self.api_yanit_output)

        self.sorgu_gonder_button = QtWidgets.QPushButton('Sorgu Gönder')
        self.sorgu_gonder_button.clicked.connect(self.api_sorgu_gonder)
        self.api_sorgu_layout.addWidget(self.sorgu_gonder_button)

        self.api_sorgu_tab.setLayout(self.api_sorgu_layout)

        self.addTab(self.paket_gonder_tab, 'Paket Gönder')
        self.addTab(self.api_sorgu_tab, 'API Sorgu')

        self.setGeometry(100, 100, 400, 600)
        self.show()

        self.user_agentlari_yukle()

    def user_agentlari_yukle(self):
        try:
            with open("agent.txt", "r") as f:
                agents = f.readlines()
            for agent in agents:
                self.user_agent_combo.addItem(agent.strip())
                self.user_agent_combo_api.addItem(agent.strip())
        except FileNotFoundError:
            print("agent.txt dosyası bulunamadı.")

    def paket_gonder(self):
        ip = self.ip_input.text()
        paket_turu = self.paket_turu_combo.currentText()
        http_yontemi = self.http_yontemi_combo.currentText()
        zaman_asimi = self.zaman_asimi_input.text()
        user_agent = self.user_agent_combo.currentText()

        if not ip:
            self.yanit_output.setPlainText("Hata: IP adresi boş olamaz.")
            return

        if not zaman_asimi:
            self.yanit_output.setPlainText("Hata: Zaman aşımı boş olamaz.")
            return

        try:
            zaman_asimi = int(zaman_asimi)
            port = int(self.port_input.text()) if self.port_input.text() else None

            if paket_turu == 'TCP':
                self.tcp_gonder(ip, port, self.paket_icerigi_input.toPlainText(), zaman_asimi)
            elif paket_turu == 'UDP':
                self.udp_gonder(ip, port, self.paket_icerigi_input.toPlainText(), zaman_asimi)
            elif paket_turu == 'HTTP':
                if http_yontemi == 'GET':
                    self.http_get_gonder(ip, zaman_asimi, user_agent)
                elif http_yontemi == 'POST':
                    self.http_post_gonder(ip, zaman_asimi, user_agent)

        except ValueError as e:
            self.yanit_output.setPlainText(f"Hata: {str(e)}")
        except Exception as e:
            self.yanit_output.setPlainText(f"Hata: {str(e)}")

    def http_get_gonder(self, ip, zaman_asimi, user_agent):
        url = f'http://{ip}'
        headers = {'User-Agent': user_agent}
        try:
            response = requests.get(url, headers=headers, timeout=zaman_asimi)
            response.raise_for_status()
            self.yanit_output.setPlainText(response.text)
        except requests.exceptions.RequestException as e:
            self.yanit_output.setPlainText(f"Hata: {str(e)}")

    def http_post_gonder(self, ip, zaman_asimi, user_agent):
        url = f'http://{ip}'
        data = self.paket_icerigi_input.toPlainText()
        headers = {'User-Agent': user_agent}
        try:
            response = requests.post(url, data=data, headers=headers, timeout=zaman_asimi)
            response.raise_for_status()
            self.yanit_output.setPlainText(response.text)
        except requests.exceptions.RequestException as e:
            self.yanit_output.setPlainText(f"Hata: {str(e)}")

    def api_sorgu_gonder(self):
        url = self.api_input.text()
        user_agent = self.user_agent_combo_api.currentText()

        if not url:
            self.api_yanit_output.setPlainText("Hata: URL boş olamaz.")
            return

        headers = {'User-Agent': user_agent}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            json_response = json.loads(response.text)
            pretty_response = json.dumps(json_response, indent=4)
            self.api_yanit_output.setPlainText(pretty_response)
        except requests.exceptions.RequestException as e:
            self.api_yanit_output.setPlainText(f"Hata: {str(e)}")
        except json.JSONDecodeError:
            self.api_yanit_output.setPlainText("Hata: Geçersiz JSON yanıtı.")

    def tcp_gonder(self, ip, port, content, zaman_asimi):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(zaman_asimi)
        try:
            sock.connect((ip, port))
            sock.sendall(content.encode())
            response = sock.recv(4096).decode()
            self.yanit_output.setPlainText(response)
        finally:
            sock.close()

    def udp_gonder(self, ip, port, content, zaman_asimi):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(zaman_asimi)
        try:
            sock.sendto(content.encode(), (ip, port))
            response, _ = sock.recvfrom(4096)
            self.yanit_output.setPlainText(response.decode())
        finally:
            sock.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = PacketSenderApp()
    sys.exit(app.exec_())
