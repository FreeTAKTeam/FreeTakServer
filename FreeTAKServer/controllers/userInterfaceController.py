class userInterfaceController:
    def __init__(self):
        self.commandDict = {
            "1": "checkAliveProcesses",
            "2": "getSocketInformation"
        }

    def userInput(self):
        command = str(input('FTS $ '))
        commandFunction = getattr(self, self.commandDict[command])
        commandFunctionOutput = commandFunction()

    def checkAliveProcesses(self):
        pass
