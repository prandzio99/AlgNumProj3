INCODE_MATRIX = [[10, -3, -2, -1],
                 [3, 10, -3, -2],
                 [2, 3, 10, -3],
                 [1, 2, 3, 10]]

INCODE_F_VECTOR = [31, -17, 49, -19]

# globalne zmienne do sprawdzania (ro)zbieżności metody
divergence_counter = 0
last_diff_check = 999999
check_iteration = 1


def get_sq_matrix(n):
    """
    funkcja zwraca macierz o rozmiarze NxN utworzoną
    z danych wprowadzanych przez użytkownika

    :param n: integer
    :return: list[n][n]
    """
    matrix = []
    print("Wprowadź współczynniki układu równań: ")
    for i in range(1, n+1):
        row = []
        for j in range(1, n+1):
            prompt = "a" + str(i) + str(j) + ": "
            row.append(int(input(prompt)))
        matrix.append(row)
    return matrix


def get_start_vector(n):
    """
    funkcja zwraca wektor wstepnego przybliżenia utworzony
    z podanych przez użytkownika danych

    :param n: int
    :return: list[n]
    """
    vector = []
    print("Wprowadź wektor wstępnych przybliżeń rozwiązania: ")
    for i in range(1, n+1):
        prompt = "x" + str(i) + ": "
        vector.append(int(input(prompt)))
    return vector


def get_f_vector(n):
    """
    funkcja zwraca wektor f utworzony z podanych przez użytkownika danych

    :param n: int
    :return: list[n]
    """
    vector = []
    print("Wprowadź wektor f: ")
    for i in range(1, n + 1):
        prompt = "f" + str(i) + ": "
        vector.append(int(input(prompt)))
    return vector


def define_size():
    """
    funkcja zwraca podany przez użytkownika rozmiar macierzy

    :return: n
    """
    return int(input("Zdefiniuj rozmiar macierzy (NxN): "))


def make_choice():
    """
    funkcja pozwala użytkownikowi wybrać czy chce skorzystać
    z macierzy wpisanej do programu, czy podać nową samemu

    :return: boolean
    """
    print("Czy chcesz użyć własnej macierzy? (T/N)")
    ans = ""
    while ans not in ["t", "n"]:
        ans = input().lower()
    return "t" in ans


def display(vector, precision):
    """
    funkcja wyświetla wyniki działania programu

    :param vector: list[n][n]
    :param precision: float
    :return: None
    """
    print(f"Przybliżenie rozwiązania układu z precyzją = {precision}")
    for i in range(len(vector)):
        print(f"x{i+1} = {round(vector[i], 5)}")


def divergence_check(prev, curr):
    """
    funkcja sprawdza czy metoda jest rozbieżna dla podanego układu równań

    :param prev:
    :param curr:
    :return:
    """
    global last_diff_check
    global divergence_counter
    global check_iteration
    divergence_list = []
    for i in range(len(curr)):
        divergence_list.append(abs(prev[i] - curr[i]))
    current_max_divergence = max(divergence_list)
    print("p", check_iteration, " = ", round(current_max_divergence, 10), sep="")
    check_iteration += 1
    if current_max_divergence <= last_diff_check:
        last_diff_check = current_max_divergence
        divergence_counter = 0
    else:
        last_diff_check = current_max_divergence
        divergence_counter += 1
    if divergence_counter >= 5:
        print("Metoda jest rozbieżna dla podanego układu równań")
        exit()


def check_precision(prev, curr, acc):
    """
    funkcja sprawdza czy kolejna iteracja osiągnęła wymagane przybliżenie

    :param prev: list[n]
    :param curr: list[n]
    :param acc: float
    :return: boolean
    """
    divergence_check(prev, curr)
    results = []
    for i in range(len(curr)):
        results.append(abs(prev[i] - curr[i]) > acc)
    for element in results:
        if element:
            return True
    else:
        return False


def gauss_seidl(matrix, f_vector, x_vector, precision):
    """
    funkcja przybliża z zadaną dokładnością rozwiązanie układu
    równań na podstawie macierzy współczynników,
    wektora f oraz wektora wstępnych przybliżeń rozwiązania

    :param matrix: list[n][n]
    :param f_vector: list[n]
    :param x_vector: list[n]
    :param precision: float
    :return: list[n]
    """
    counter = 1
    previous_vector = x_vector.copy()
    try:
        for i in range(len(x_vector)):
            if i == 0:
                frac_top = -sum([matrix[i][j] * x_vector[j] for j in range(i + 1, len(x_vector))]) + f_vector[i]
                x_vector[i] = frac_top / matrix[i][i]
            else:
                right_side = -sum([matrix[i][j] * x_vector[j] for j in range(0, i)])
                left_side = -sum([matrix[i][j] * x_vector[j] for j in range(i + 1, len(x_vector))]) + f_vector[i]
                x_vector[i] = (right_side - left_side) / matrix[i][i]
        while check_precision(previous_vector, x_vector, precision):
            previous_vector = x_vector.copy()
            for i in range(len(x_vector)):
                if i == 0:
                    frac_top = -sum([matrix[i][j] * x_vector[j] for j in range(i+1, len(x_vector))]) + f_vector[i]
                    x_vector[i] = frac_top / matrix[i][i]
                else:
                    right_side = -sum([matrix[i][j] * x_vector[j] for j in range(0, i)])
                    left_side = -sum([matrix[i][j] * x_vector[j] for j in range(i+1, len(x_vector))]) + f_vector[i]
                    x_vector[i] = (right_side - left_side)/matrix[i][i]
            counter += 1
    except ZeroDivisionError:
        print("Macierz zawiera zera na przekątnej, uruchom program jeszcze raz zamieniając kolejność wierszy.")
        exit()
    print("Wykonano iteracji:", counter)
    return x_vector


def main():
    print("Program używa metody Gaussa-Seidla do przybliżenia rozwiązania układu równań z zadaną dokładnością.")
    if make_choice():
        matrix_size = define_size()
        matrix = get_sq_matrix(matrix_size)
        f_vector = get_f_vector(matrix_size)
        x_vector = get_start_vector(matrix_size)
    else:
        matrix = INCODE_MATRIX.copy()
        f_vector = INCODE_F_VECTOR.copy()
        x_vector = get_start_vector(len(matrix))
    precision = float(input("Zadaj dokładność: "))
    approximation = gauss_seidl(matrix, f_vector, x_vector, precision)
    display(approximation, precision)


if __name__ == '__main__':
    main()
