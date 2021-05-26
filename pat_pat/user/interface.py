from abc import abstractmethod

from pygame import Surface

from pat_pat.role import Role, Action


class UserInterface:
    @abstractmethod
    def decision(self, my_role: Role, enemies_role: list[tuple[str, Role]]) -> Action:
        pass

    @abstractmethod
    def get_user_name(self) -> str:
        pass

    @abstractmethod
    def get_role_id(self, roles_pics: list[list[Surface]]) -> int:
        pass
