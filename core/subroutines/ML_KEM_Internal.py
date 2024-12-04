from core.subroutines.KPke import KPke


class ML_KEM_Internal:
    def __init__(self, kpke: KPke):
        self.kpke = kpke
        self.shared_secret = None

    def get_Keys(self):
        return self.shared_secret
