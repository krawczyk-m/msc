
class State:
    """
    Sender states
    """

    IDLE = "idle"
    AWAIT_NOTIFY = "await_notify"
    LISTEN = "listen"
    AWAIT_REPORT_ACK = "await_report_ack"
    FIN = "fin"
