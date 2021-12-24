import queue
class AddDataToCoTList:
    def __init__(self):
        pass

    #this function sends specified data to all pipes within a provided array
    def send(self, pipes, data, origin):
        for service, pipe in pipes.items():
            try:
                if service != origin:
                    #print('putting data in pipe')
                    pipe.put(data)
            except Exception as e:
                print(e)
                pass
        return 1

    #this function attempts to receive data from a specified pipe and then return the data

    def recv(self, pipe, timeout = None):
        try:
            data = pipe.get(timeout = timeout)
            return data
        except queue.Empty:
            return None
        except Exception as e:

            print(e)
