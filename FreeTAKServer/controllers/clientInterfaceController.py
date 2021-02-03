class ClientInterfaceController:
    def __init__(self):
        self.commandDict = {
            'help': self.helpCommand
        }

    def commandInput(self):
        command = str(input('FTS $ '))
        output = self.commandDict[command]()
        print(output)

    def helpCommand(self):
        output = "this is currently just astetic"
        return output


ClientInterfaceController().commandInput()
