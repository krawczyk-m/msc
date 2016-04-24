
class State:
    """
    Sender states
    """

    INIT = "init"
    NOTIFY = "notify"
    AWAIT_CONFIRMATION = "await_confirmation"
    SEND = "send"
    AWAIT_REPORT = "await_report"
    CONFIRM_REPORT = "confirm_report"
