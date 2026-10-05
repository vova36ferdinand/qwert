import json
import socket

HEADER_SIZE_BYTES = 3
OPCODE_SIZE_BYTES = 1
LITTLE_ENDIAN = "little"


class RPCClient: #Клиент для выполнения удаленных вызовов процедур по TCP

    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None: #Инициализирует адрес сервера
        self.host = host
        self.port = port

    def _send_request(self, opcode: int, payload: dict) -> dict: #Отправляет запрос серверу по бинарному протоколу
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.host, self.port))

        body_bytes = json.dumps(payload).encode("utf-8")
        len_bytes = len(body_bytes).to_bytes(HEADER_SIZE_BYTES, byteorder=LITTLE_ENDIAN)
        code_byte = opcode.to_bytes(OPCODE_SIZE_BYTES, byteorder=LITTLE_ENDIAN)

        client.sendall(len_bytes + code_byte + body_bytes)

        header = client.recv(HEADER_SIZE_BYTES + OPCODE_SIZE_BYTES)
        res_len = int.from_bytes(header[:HEADER_SIZE_BYTES], byteorder=LITTLE_ENDIAN)
        res_bytes = client.recv(res_len)
        client.close()

        data = json.loads(res_bytes.decode("utf-8"))
        return data.get("result")
#Это все функции что в файле data_layer.py их мы вызываем

    def create_account(self, uid: int, ip: str, timestamp: float) -> tuple:
        return self._send_request(1, {"uid": uid, "ip": ip, "timestamp": timestamp})

    def get_all_accounts(self) -> list:
        return self._send_request(2, {})

    def get_account_by_id(self, uid: int) -> tuple | None:
        return self._send_request(3, {"uid": uid})

    def update_account(self, uid: int, ip: str, timestamp: float) -> tuple | None:
        return self._send_request(4, {"uid": uid, "ip": ip, "timestamp": timestamp})

    def create_message(self, uid: int, argument: str, account: int) -> tuple:
        return self._send_request(5, {"uid": uid, "argument": argument, "account": account})

    def get_all_messages(self) -> list:
        return self._send_request(6, {})

    def get_message_by_id(self, uid: int) -> tuple | None:
        return self._send_request(7, {"uid": uid})

    def update_message(self, uid: int, argument: str, account: int) -> tuple | None:
        return self._send_request(8, {"uid": uid, "argument": argument, "account": account})

    def create_log(self, uid: int, message: int, status: str) -> tuple:
        return self._send_request(9, {"uid": uid, "message": message, "status": status})

    def get_all_logs(self) -> list:
        return self._send_request(10, {})

    def get_log_by_id(self, uid: int) -> tuple | None:
        return self._send_request(11, {"uid": uid})

    def update_log(self, uid: int, message: int, status: str) -> tuple | None:
        return self._send_request(12, {"uid": uid, "message": message, "status": status})

    def select_recent_messages(self, now_timestamp: float) -> list:
        return self._send_request(13, {"now_timestamp": now_timestamp})
