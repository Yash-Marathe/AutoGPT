import time

class Spinner:
    def __init__(self, message: str = "Loading...", delay: float = 0.1):
        self.message = message
        self.delay = delay
        self._running = False

    def start(self):
        self._running = True
        print(self.message)
        while self._running:
            time.sleep(self.delay)

    def stop(self):
        self._running = False
        print("Spinner stopped.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

def test_spinner_initializes_with_default_values():
    """Tests that the spinner initializes with default values."""
    with Spinner() as spinner:
        assert spinner.message == "Loading..."
        assert spinner.delay == 0.1

def test_spinner_initializes_with_custom_values():
    """Tests that the spinner initializes with custom message and delay values."""
    PLEASE_WAIT = "Please wait..."
    with Spinner(message=PLEASE_WAIT, delay=0.2) as spinner:
        assert spinner.message == PLEASE_WAIT
        assert spinner.delay == 0.2

def test_spinner_stops_spinning():
    """Tests that the spinner starts spinning and stops spinning without errors."""
    with Spinner() as spinner:
        time.sleep(1)
    assert not spinner.running

def test_spinner_can_be_used_as_context_manager():
    """Tests that the spinner can be used as a context manager."""
    with Spinner() as spinner:
        assert spinner.running
    assert not spinner.running
