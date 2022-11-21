__unittest = True
class CustomAssertions:
    def assertKeyValuePairInDict(self, key: object, val: object, dictionary: object) -> object:
        """

        Args:
            key:
            val:
            dictionary:

        Returns:

        """
        def gen_dict_extract(key, var, val):
            if hasattr(var, 'items'):
                for k, v in var.items():
                    if k == key and v == val:
                       return True
                    if isinstance(v, dict):
                        for result in gen_dict_extract(key, v, val):
                            return result
                    elif isinstance(v, list):
                        for d in v:
                            if gen_dict_extract(key, d, val) == True:
                                return True
                            else:
                                for result in gen_dict_extract(key, d, val):
                                    return result
                    elif isinstance(v, bool):
                        return True
        assert gen_dict_extract(key=key, var=dictionary, val = val)
