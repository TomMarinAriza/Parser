from rich import print

_errors_detected = 0


def error(message, lineno=None):
    global _errors_detected
    if lineno is not None:
        print(f"{lineno}: [red]{message}[/red]")
    else:
        print(f"[red]{message}[/red]")
    _errors_detected += 1


def errors_detected():
    return _errors_detected


def clear_errors():
    global _errors_detected
    _errors_detected = 0