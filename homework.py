from typing import Dict, Sequence, Union
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Получить сообщение о тренировке."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    RUN_COEFF_MULTIPL: float = 18
    RUN_COEFF_SUBTRACT: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.RUN_COEFF_MULTIPL
                * self.get_mean_speed()
                - self.RUN_COEFF_SUBTRACT)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    SW_COEFF_MULTIPL_FOR_WEIGHT: float = 0.035
    SW_COEFF_MULTIPL: float = 0.029
    SW_COEFF_MULTIPL_FOR_MEAN_SPEED: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return (self.SW_COEFF_MULTIPL_FOR_WEIGHT
                * self.weight
                + ((self.get_mean_speed()
                   ** self.SW_COEFF_MULTIPL_FOR_MEAN_SPEED
                   // self.height))
                * self.SW_COEFF_MULTIPL
                * self.weight) * (self.duration * self.MIN_IN_HR)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    SWIM_COEFF_FOR_MEAN_SPEED: float = 1.1
    SWIM_COEFF_MULTIPL: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        return ((self.get_mean_speed() + self.SWIM_COEFF_FOR_MEAN_SPEED)
                * self.SWIM_COEFF_MULTIPL
                * self.weight)


def read_package(workout_type: str,
                 data: Sequence[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    packages: Dict[str, type[Training]] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking}
    if workout_type not in packages:
        raise KeyError(f'{workout_type} - неизвестный тип тренировки')

    return packages[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
