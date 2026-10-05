import json
import socket
import data_layer

HOST = "127.0.0.1" #Мой локальный хост
PORT = 8080
HEADER_SIZE_BYTES = 3
OPCODE_SIZE_BYTES = 1
LITTLE_ENDIAN = "little" #константа порядка байт
LOG_FILE = "journal.log" #имя файла, в который сервер обязан сохранять историю запросов


def log_request(opcode: int, payload: dict) -> None: #Открывает файл с логами и дозаписывает строку с кодом операции и переданными данными
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"Код: {opcode}, Данные: {payload}\n")


def process_request(opcode: int, data: dict) -> tuple[int, dict]: #Вызывает нужную функцию слоя данных по коду операции
    if opcode == 1:
        res = data_layer.create_account(data["uid"], data["ip"], data["timestamp"])
        
    elif opcode == 2:
        res = data_layer.get_all_accounts()
        
    elif opcode == 3:
        res = data_layer.get_account_by_id(data["uid"])
        
    elif opcode == 4:
        res = data_layer.update_account(data["uid"], data["ip"], data["timestamp"])
        
    elif opcode == 5:
        res = data_layer.create_message(data["uid"], data["argument"], data["account"])
        
    elif opcode == 6:
        res = data_layer.get_all_messages()
        
    elif opcode == 7:
        res = data_layer.get_message_by_id(data["uid"])
        
    elif opcode == 8:
        res = data_layer.update_message(data["uid"], data["argument"], data["account"])
        
    elif opcode == 9:
        res = data_layer.create_log(data["uid"], data["message"], data["status"])
        
    elif opcode == 10:
        res = data_layer.get_all_logs()
        
    elif opcode == 11:
        res = data_layer.get_log_by_id(data["uid"])
        
    elif opcode == 12:
        res = data_layer.update_log(data["uid"], data["message"], data["status"])
        
    elif opcode == 13:
        res = data_layer.select_recent_messages(data["now_timestamp"])
        
    else:
        return opcode, {"error": "Неизвестный код операции"}

    return opcode, {"result": res}


def run_server() -> None: #Запускает TCP RPC сервер
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        conn, _ = server.accept()
        handle_connection(conn)


def handle_connection(conn: socket.socket) -> None: #Обрабатывает подключение клиента
    try:
        header = conn.recv(HEADER_SIZE_BYTES + OPCODE_SIZE_BYTES)
        if not header:
            conn.close()
            return
        body_len = int.from_bytes(header[:HEADER_SIZE_BYTES], byteorder=LITTLE_ENDIAN)
        opcode = int.from_bytes(header[HEADER_SIZE_BYTES:], byteorder=LITTLE_ENDIAN)
        body_bytes = conn.recv(body_len)
        payload = json.loads(body_bytes.decode("utf-8"))

        log_request(opcode, payload)
        out_code, response_data = process_request(opcode, payload)

        res_bytes = json.dumps(response_data).encode("utf-8")
        res_len_bytes = len(res_bytes).to_bytes(HEADER_SIZE_BYTES, byteorder=LITTLE_ENDIAN)
        res_code_byte = out_code.to_bytes(OPCODE_SIZE_BYTES, byteorder=LITTLE_ENDIAN)

        conn.sendall(res_len_bytes + res_code_byte + res_bytes)
    finally:
        conn.close()


if __name__ == "__main__":
    run_server()
