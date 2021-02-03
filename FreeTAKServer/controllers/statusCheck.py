import socket
from time import sleep, gmtime, strftime
import uuid
import smtplib
import ssl
import time


class statusCheck:
    def __init__(self):
        # !/usr/bin/env python3
        # needs python 3.x due to some different functions

        # Healthchecker for FTS TAK self.servers. May work with others, but not tested
        # Alan Barrow July 16, 2020 alan@pinztrek.com
        self.version = "1.0"

        # tune your params below, then execute. It will run until interupted.
        # prints "+" each time it checks a server.
        # Will only work with self.servers not using secure connections

        # --------------------------------------------------------------------------------------------------
        # Setup our test params

        # How long to sleep between checks in seconds
        self.sleeptime = 60 * 2

        # Setup Email params
        # multiple recips separated by comma and a space, format is pretty picky

        self.recip = []

        self.sender = ''

        # Your smtp server
        self.smtp_server = ''

        # Your smtp port. Should be 465 or similar SSL, the sendmail is setup to use SSL
        self.smtp_port = ''

        # The account email to authorize with. Sometimes need a + instead of @
        self.smtp_acct = ""

        # Password to send email
        self.smtp_password = ""

        self.smtp_trace_level = 0  # 1 is useful trace

        # List of self.servers to monitor
        self.servers = [
            ["server", "ip", "port"]
        ]

        # -----------------------------------------------------------------------------------------
        # Should not have to modify below here

        # Setup a UID
        self.my_uid = str(socket.getfqdn())
        self.my_uid = self.my_uid + "-" + str(uuid.uuid1())
        self.my_uid = bytes("healthchecker-" + self.my_uid, "UTF-8")

        # get a time, does not really matter
        self.xml_time = bytes(strftime("%Y-%m-%dT%H:%M:%SZ", gmtime()), "UTF-8")

        # XML strings for the healthcheck
        self.dataString = b'<?xml self.version="1.0" encoding="UTF-8" standalone="yes"?>\n<event self.version="2.0" uid="' + self.my_uid + b'" type="t-x-c-t" time="' + self.xml_time + b'" start="' + self.xml_time + b'" stale="' + self.xml_time + b'" how="h-g-i-g-o"><point lat="0.0" lon="0.0" hae="9999999.0" ce="9999999.0" le="9999999.0"/><detail><takv platform="healthcheck" os="24" self.version="1.0.0.0"/><contact/></detail></event>'

        self.connectionString = self.dataString

        # Uncomment to see the xml sent
        # print(self.dataString)

        # -------------------------------------------------------------------------
        # Make these global
        self.status = ""
        self.sock = ''

        # Get rid of any old messages, really should not be needed with unique UID's
    def flushit(self):
        self.sock.settimeout(1)

        # response = 'start some reading'
        # Flush any pending server responses
        while True:
            # print("Read attempt: " + str(i))
            try:
                response = self.sock.recv(2048)
                # print("flushit response is:")
                # print(response)
                pass

            except BaseException:
                # print("flushit read empty")
                # Flushed, now return
                break

        # return response

    def readit(self):
        self.sock.settimeout(1)

        response = ''
        # Flush any pending server responses
        # while True:
        for i in range(5):
            # print("Read attempt: " + str(i))
            try:
                response = self.sock.recv(2048)
                # print("readit response is:")
                # print(response)
                return response

            except Exception as e:
                # print("readit read empty")
                pass

        return response

    def closeit(self):
        # print("shutting down")
        self.sock.shutdown(1)
        time.sleep(0.1)
        self.sock.close()

    def notify(self, status):
        # Log event to the screen
        print("")  # since the progress dots do not have new line

        # uncomment to just print the event, not the email. (and comment out the email print)
        # print(strftime("%d/%m/%y %H:%M ", gmtime()) + self.status)
        # Add timestamp
        status = strftime("%d/%m/%y %H:%M ", gmtime()) + status

        smtp_subject = status
        smtp_body = status
        my_recips = ""
        for cnt in range(len(self.recip) - 1):
            my_recips = my_recips + self.recip[cnt] + ", "
        my_recips = my_recips + self.recip[-1]

        # Useful when debugging multiple debugging, ok to comment out
        print("Recip String: " + my_recips)

        # Prepare the message package
        message = "From: " + self.sender + "\r\n" \
                  + "To: " + my_recips + "\r\n" \
                  + "Subject: " + smtp_subject \
                  + "\r\n\r\n" + smtp_body \
 \
            # useful when debugging email
        print(message)

        # Blast the email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
            try:
                server.set_debuglevel(self.smtp_trace_level)
                server.login(self.smtp_acct, self.smtp_password)
                server.sendmail(self.sender, self.recip, message)
                server.quit()
                print("Mail sent")
            except Exception as e:
                print(e)
                print("Mail send failed")

    def start(self):
        print("------------------------------------------------------------------------------")
        print("FTS Healthchecker Version " + self.version)
        while True:
            # print("starting loop again")
            for server in range(0, len(self.servers)):

                # print("server # is " + str(server))

                # Setup our locals
                testserver = self.servers[server][0]
                testip = self.servers[server][1]
                testport = self.servers[server][2]
                # print(str(server+1) + " " + testserver + " IP: " + testip + ":" + str(testport))

                # Open the socket
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Longer timeout for busy self.servers
                self.sock.settimeout(10)

                # Now try to open
                try:
                    self.sock.connect((testip, testport))
                    # print("Connected: " + testip + ":" + str(testport))

                except socket.error as e:
                    # print(testserver + 'connection failed')
                    self.closeit()
                    self.notify(testserver + ": Connect failed socket error-" + str(e))
                    continue

                except BaseException:
                    # return 'connection failed'
                    # print(testserver + 'connection failed')
                    # No need to close, not open
                    # closeit()
                    self.notify(testserver + ": Connect failed")
                    continue

                # self.sock.send(b'')

                # Send Connect String to server
                # print("Now Connect string")
                try:
                    sent = self.sock.send(self.connectionString)
                except BaseException:
                    print(testserver + ": Connection send failed")
                    self.closeit()
                    self.notify(testserver + ": Connection send Failed")
                    continue

                # print("Connect response:")
                # Server sends active CoT's upon connect
                junk = self.flushit()  # Don't care about recent points
                # print(junk)

                # time.sleep(0.1)
                # flush the reads
                # junk=flushit()

                # print("Now send data string:")
                # print(self.dataString)
                sent = self.sock.send(self.dataString)

                # print("read the heartbeat response:")
                # Set Default response if it does not match
                # response = testserver + ": Healthcheck compare failed"
                response = ''

                # Do multiple checks in case server sends a valid CoT while testing
                for count in range(1, 20):
                    junk = self.readit()
                    # print("Heartbeat response " + str(count) + ":")
                    # print(junk)
                    if junk == self.dataString:
                        # print(testserver + ": OK")
                        # notify(testserver + ": OK")
                        response = testserver + ": OK"
                        # Exit the response check for loop
                        break
                    else:
                        response = testserver + ": Healthcheck compare failed"
                        # print(testserver + ": Healthcheck compare failed")
                        # pass
                # print("Cleanup and try next server")
                # Cleanup and notify failed check
                try:
                    self.closeit()
                except BaseException:
                    pass
                # Now send the response
                if response:
                    self.notify(response)

                # print("test")
                print("+", end="", flush=True)
                # print("Hello there!", end = '')
                # print(".")

            # print("+")
            # print("sleeping " + str(self.sleeptime))
            sleep(self.sleeptime)


if __name__ == "__main__":
    statusCheck().start()
