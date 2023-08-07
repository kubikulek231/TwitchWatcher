import platform


class IsRPI4:
    @staticmethod
    def is_rpi4():
        return platform.machine() == 'armv7l'
