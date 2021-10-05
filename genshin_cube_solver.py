class Cube():
    def __init__(self, flag_const:bool=False, flag_hat:bool=False, flag_exist:bool=True, direction:int=1) -> None:
        self._flag_const = flag_const
        self._flag_hat = flag_hat
        self._flag_exist = flag_exist
        self._direction = direction

    def __add__(self, other) -> int:
        return self.get_weight() + other.get_weight()

    def __radd__(self, other) -> int:
        return self.get_weight() + other

    def rotate(self, cubes:list, cube_index:int) -> None:
        if self._flag_const:
            cubes[cube_index + 1].rotate(cubes, cube_index + 1)
            return
        cube_index = 0 if cube_index > 8 else cube_index

        self._direction += 1

        if not self._flag_exist:
            if self._direction > 8:
                self._direction = 1
                cubes[cube_index + 1].rotate(cubes, cube_index + 1)
            return

        if self._direction > 4:
            self._direction = 1
            if cube_index == 8:
                cubes[0].rotate(cubes, 0)
            else:
                cubes[cube_index + 1].rotate(cubes, cube_index + 1)

    def get_weight(self) -> int:
        if not self._flag_exist:
            return 9
        return int(self._flag_hat) * 4 + self._direction

    def get_direction(self) -> int:
        return self._direction

    def get_states(self) -> None:
        print(f'<{self}>: c:{self._flag_const}, h:{self._flag_hat}, e:{self._flag_exist}, dir:{self._direction}')

class Field():
    from math import sqrt
    def __init__(self, userStateMatrix:list, userDirMatrix:list) -> None:
        self._userStateMatrix = self._def_states(userStateMatrix)
        self._userDirMatrix = userDirMatrix
        self._field:list = self._initialize_field()
        #[cube.get_states() for cube in self._field]
        self._matrix_one_size = int(self.sqrt(len(self._field)))

    def _def_states(self, userStateMatrix) -> list:
        states = {'const':0, 'consth':1, 'dynamic':2, 'dynamich':3, 'nothing':4}
        return [states.get(el) for el in userStateMatrix]

    def _initialize_field(self) -> list:
        return [Cube(
                True if states == 0 or states == 1 else False,
                True if states == 1 or states == 3 else False,
                False if states == 4 else True,
                direction) for states, direction in zip(self._userStateMatrix, self._userDirMatrix)]

    def _check(self) -> bool:
        fsum = sum([cube for cube in self._field[:self._matrix_one_size]])

        for k in range(self._matrix_one_size):
            temp = sum([cube for cube in self._field[k*self._matrix_one_size:k*self._matrix_one_size+self._matrix_one_size]])
            if temp != fsum:
                return False

        for k in range(self._matrix_one_size):
            temp = sum([cube for cube in self._field[k::self._matrix_one_size]])
            if temp != fsum:
                return False

        dig1 = sum([cube for cube in self._field[0::self._matrix_one_size+1]])
        if dig1 != fsum:
            return False

        dig1 = sum([cube for cube in self._field[2:-1:self._matrix_one_size-1]])
        if dig1 != fsum:
            return False

        return True

    def _get_weights(self) -> list:
        return [cube.get_weight() for cube in self._field]

    def _get_directions(self) -> list:
        return [cube.get_direction() for cube in self._field]

    def solve(self) -> None:
        while True:
            if self._check():
                print(f'Weights: {self._get_weights()}\nDirections: {self._get_directions()}')
                break
            self._field[0].rotate(self._field, 0)
            

def main() -> None:
    # Examples:
    # userStateMatrix = ['dynamic', 'consth', 'dynamich', 
    #                    'nothing', 'consth', 'const',
    #                    'dynamic', 'const', 'dynamich']
    # userDirMatrix = [1, 3, 1,
    #                  1, 1, 1,
    #                  1, 3, 1]

    # userStateMatrix = ['dynamic', 'dynamic', 'dynamic', 
    #                    'dynamic', 'dynamic', 'dynamic',
    #                    'dynamic', 'nothing', 'dynamic']
    # userDirMatrix = [2, 1, 2,
    #                  3, 3, 3,
    #                  4, 1, 4]

    userStateMatrix = ['dynamic', 'const', 'consth', 
                       'nothing', 'dynamich', 'const',
                       'const', 'dynamich', 'dynamich']
    userDirMatrix = [1, 3, 4,
                     1, 1, 1,
                     2, 3, 1]

    Field(userStateMatrix, userDirMatrix).solve()


if __name__ == '__main__':
    main()