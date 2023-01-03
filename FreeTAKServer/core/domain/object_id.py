import re
from digitalpy.core.main.object_factory import ObjectFactory
import uuid


class ObjectId:

    DELIMITER = ":"

    __dummy_id_pattern = "DigitalPy[A-Za-z0-9]{32}"
    __id_pattern = None
    __delimiter_pattern = None
    _num_pk_keys = {}
    __null_oid = None
    __fq_type = None

    def __init__(self, type, id=[], prefix=""):
        self.prefix = prefix
        self.persistence_facade = ObjectFactory.get_instance("persistencefacade")
        self.__fq_type = (
            lambda: self.persistence_facade.get_fully_qualified_type(type)
            if type != "NULL"
            else "NULL"
        )()
        if not isinstance(id, list):
            self.id = [id]
        else:
            self.id = id

        self.num_pks = ObjectId.get_number_of_pks(type)

        while len(self.id) < self.num_pks:
            self.id.append(self.get_dummy_id())

        self.str_val = self.__str__()

    def __str__(self):
        oid_str = self.__fq_type + ObjectId.DELIMITER + ObjectId.DELIMITER.join(self.id)
        if len(self.prefix.strip()) > 0:
            oid_str = self.prefix + ObjectId.DELIMITER + oid_str
        self.str_val = oid_str
        return self.str_val

    def get_id(self):
        return self.id

    def get_type(self):
        return self.__fq_type

    def contains_dummy_ids(self):
        for id in self.get_id():
            if ObjectId.is_dummy_id(id):
                return True
        return False

    @staticmethod
    def is_dummy_id(id):
        return len(id) == 36 and id.startswith("DigitalPy")

    @staticmethod
    def NULL_OID():
        if ObjectId.__null_oid == None:
            ObjectId.__null_oid = ObjectId("NULL")
        return ObjectId.__null_oid

    @staticmethod
    def get_number_of_pks(type):
        if type not in ObjectId._num_pk_keys:
            num_pks = 1
            persistence_facade = ObjectFactory.get_instance("persistencefacade")
            if persistence_facade.is_known_type(type):
                mapper = persistence_facade.get_mapper(type)
                num_pks = len(mapper.get_pk_names)
            ObjectId._num_pk_keys[type] = num_pks
        return ObjectId._num_pk_keys[type]

    @staticmethod
    def get_dummy_id():
        return "DigitalPy" + str(uuid.uuid4()).replace("-", "")

    @staticmethod
    def is_valid(oid):
        if ObjectId.parse(oid) == None:
            return False
        else:
            return True

    @staticmethod
    def parse(oid):
        if isinstance(oid, ObjectId):
            return oid
        return None
        # TODO: properly implement parsing oid string
        oid_parts = ObjectId.parse_oid_string(oid)
        if not oid_parts:
            return None

        type = oid_parts["type"]
        ids = oid_parts["id"]
        prefix = oid_parts["prefix"]

        if not ObjectFactory.get_instance("persistence_facade").is_known_type(type):
            return None

        num_pks = ObjectId.get_number_of_pks(type)
        if num_pks == None or num_pks != len(ids):
            return None

        return ObjectId(type, ids, prefix)

    @staticmethod
    def get_delimiter_pattern():
        if ObjectId.delimiter_pattern == None:
            ObjectId.delimiter_pattern = "/" + ObjectId.DELIMITER + "/"
        return ObjectId.delimiter_pattern

    @staticmethod
    def parse_oid_string(oid: str):
        if len(oid) == 0:
            return None
        oid_parts = re.split(ObjectId.get_delimiter_pattern(), oid)
        if len(oid_parts) < 2:
            return None
        if ObjectId.__id_pattern == None:
            ObjectId.__id_pattern = "/^[0-9]*$|^" + ObjectId.__dummy_id_pattern + "$/"

        ids = []
        next_part = oid_parts.pop()
        while next_part != None and re.split(ObjectId.__id_pattern, next_part) == 1:
            int_next_part = int(next_part)
            if next_part == str(int_next_part):
                ids.append(int_next_part)
            else:
                ids.append(next_part)
        ids.reverse()
        type = next_part

        prefix = ObjectId.DELIMITER + oid_parts

        return {"type": type, "id": ids, "prefix": prefix}
