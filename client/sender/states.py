
class State:
    """
    Sender states
    """

    IDLE = "idle"
    NOTIFY_SENT = "notify_sent"
    LISTEN = "listen"
    AWAIT_REPORT = "await_report"
    FIN = "fin"
