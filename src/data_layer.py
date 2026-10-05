TIME_LIMIT_MINUTES = 8
SECONDS_IN_MINUTE = 60

ACCOUNTS = []
MESSAGES = []
LOGS = []


def create_account(uid: int, ip: str, ts: float) -> list:#Создаю аккаунт
    for acc in ACCOUNTS:
        if acc[0] == uid:
            acc[1] = ip
            acc[2] = ts
            return acc
    new_account = [uid, ip, ts]
    ACCOUNTS.append(new_account)
    return new_account

def get_all_accounts() -> list[tuple]: #Даёт список всех аккаунтов
    return ACCOUNTS


def get_account_by_id(uid: int) -> tuple | None: #Находит запись аккаунта по uID
    for account in ACCOUNTS:
        if account[0] == uid:
            return account
    return None


def update_account(uid: int, ip: str, timestamp: float) -> tuple | None: #Обновляем запись аккаунта по uID
    for index, account in enumerate(ACCOUNTS):
        if account[0] == uid:
            updated = (uid, ip, timestamp)
            ACCOUNTS[index] = updated
            return updated
    return None

def create_message(msg_id: int, text: str, account: int) -> list:
    """Создает сообщение или обновляет существующее по msg_id."""
    for msg in MESSAGES: # или messages
        if msg[0] == msg_id:
            msg[1] = text
            msg[2] = account
            return msg
    new_msg = [msg_id, text, account]
    MESSAGES.append(new_msg)
    return new_msg


def get_all_messages() -> list[tuple]: #Даёт список всех сообщений
    return MESSAGES


def get_message_by_id(uid: int) -> tuple | None: #Ищет сообщение по его ID
    for message in MESSAGES:
        if message[0] == uid:
            return message
    return None


def update_message(uid: int, argument: str, account: int) -> tuple | None: #Редактирует сообщение
    for index, message in enumerate(MESSAGES):
        if message[0] == uid:
            updated = (uid, argument, account)
            MESSAGES[index] = updated
            return updated
    return None


def create_log(log_id: int, info: str, status: int) -> list:
    """Создает лог или обновляет существующий по log_id."""
    for log in LOGS: # или logs
        if log[0] == log_id:
            log[1] = info
            log[2] = status
            return log
    new_log = [log_id, info, status]
    LOGS.append(new_log)
    return new_log

def get_all_logs() -> list[tuple]: #Даёт список всех логов
    return LOGS


def get_log_by_id(uid: int) -> tuple | None: #Находит запись лога по ID
    for log_entry in LOGS:
        if log_entry[0] == uid:
            return log_entry
    return None


def update_log(uid: int, message: int, status: str) -> tuple | None: #Обновляет данные лога по ID
    for index, log_entry in enumerate(LOGS):
        if log_entry[0] == uid:
            updated = (uid, message, status)
            LOGS[index] = updated
            return updated
    return None


def select_recent_messages(now_timestamp: float,) -> list[tuple]: #ыполняет выборку по формуле реляционной алгебры
    threshold = now_timestamp - (TIME_LIMIT_MINUTES * SECONDS_IN_MINUTE)
    result = []
    for msg in MESSAGES:
        account_id = msg[2]
        account = get_account_by_id(account_id)
        if account is not None and account[2] >= threshold:
            result.append((account[1], msg[1]))
    return result

