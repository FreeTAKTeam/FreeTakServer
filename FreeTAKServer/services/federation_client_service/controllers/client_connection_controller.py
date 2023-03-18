class ClientConnectionController():
    def __init__(self, selector, federates, db, logger) -> None:
        self.selector = selector
        self.federates = federates
        self.db = db
        self.logger = logger

    def disconnect_client(self, id: str) -> None:
        try:
            self.logger.info("disconnecting client")
            try:
                federate = self.federates[id]
            except Exception as e:
                self.logger.warning("federate array has no item with uid " + str(id) + " federates array is len " + str(
                    len(self.federates)))
                return None
            try:
                federate.conn.close()
                self.selector.unregister(federate.conn)
                del (self.federates[federate.uid])
            except Exception as e:
                self.logger.warning("exception thrown disconnecting client " + str(e))

            try:
                self.db.remove_ActiveFederation(f'id == "{federate.uid}"')
            except Exception as e:
                self.logger.warning("exception thrown removing outgoing federation from DB " + str(e))
            return None
        except Exception as e:
            self.logger.warning("exception thrown accessing client for disconnecting client " + str(e))
