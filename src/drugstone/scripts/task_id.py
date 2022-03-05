import random
import string


class TaskId:

    __ids = []

    @classmethod
    def get(cls, pre: str, length: int) -> str:
        chars = string.ascii_letters + string.digits
        t_id = pre + "-" + "".join(random.choice(chars) for _ in range(length))
        while t_id in cls.__ids:
            t_id = pre + "-" + "".join(random.choice(chars) for _ in range(length))
        cls.__ids.append(t_id)
        return t_id
