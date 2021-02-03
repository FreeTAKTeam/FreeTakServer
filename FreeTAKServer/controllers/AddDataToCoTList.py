

class AddDataToCoTList:
    def __init__(self):
        pass

    # this function sends specified data to all pipes within a provided array
    def send(self, pipes, data):
        for pipe in pipes:
            try:
                pipe.send(data)
            except Exception as e:
                print(e)
                pass
        return 1

    # this function attempts to receive data from a specified pipe and then return the data
    def recv(self, pipe):
        try:
            out = pipe.poll(timeout=0.1)
            if out:
                data = pipe.recv()
                return data
            else:
                return 0
        except Exception as e:
            print(e)
