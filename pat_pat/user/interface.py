from abc import abstractmethod
from pat_pat.role import Role, Action


class UserInterface:
    @abstractmethod
    def decision(self, my_role: Role, enemies_role: list[Role]) -> Action:
        pass

    @abstractmethod
    def get_user_name(self) -> str:
        pass
