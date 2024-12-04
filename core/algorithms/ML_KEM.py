from core.subroutines.ML_KEM_Internal import ML_KEM_Internal


class ML_KEM:
    def __init__(self, ml_kem_internal: ML_KEM_Internal):
        self.ml_kem_internal = ml_kem_internal
        self.encapsulation_key = None
        self.decapsulation_key = None
        self.c = None
        self.shared_secret = None

    def key_gen(self):
        return self.encapsulation_key, self.decapsulation_key

    def encapsulation(self, encapsulation_key):
        return self.c, self.shared_secret

    def decapsulation(self, decapsulation_key, c):
        return self.shared_secret
