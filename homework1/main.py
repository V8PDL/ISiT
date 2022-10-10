import random
import time

file1_str_amount = 1000
file2_str_amount = 1000000

iteration_tries = 5

def create_files():
    file1 = open('file1.txt','w')
    for i in range(1,file1_str_amount):
        file1.write(str(random.randint(1,file2_str_amount))+'\n')
    file1.close()
    file2 = open('file2.txt', 'w')
    for i in range(1,file2_str_amount):
        #file2.write(str(i)+'\n')
        file2.write(str(random.randint(1,file2_str_amount))+'\n')
    file2.close()

if __name__ == "__main__":
    create_files()
    file1 = open('file1.txt', 'r')
    file2 = open('file2.txt', 'r')
    file3_one_for = open('file3_one_for.txt', 'w')
    file3_double_for = open('file3_double_for.txt', 'w')
    file3_generator = open('file3_generator.txt', 'w')
    mass_1 = file1.readlines()
    mass_2 = file2.readlines()
    result_1 = []
    result_2 = []
    result_3 = []


    # print("Начинаем 1-ю операцию...")
    # timer_start_double_for = time.perf_counter()

    # for str_1 in mass_1:
    #     for str_2 in mass_2:
    #         if (str_1 == str_2):
    #             result_1.append(str_1)
    #
    # timer_end_double_for = time.perf_counter()
    # file3_one_for.writelines(result_1)
    # print(f"Обработка данных (double for) заняла {timer_end_double_for - timer_start_double_for:0.4f} секунд")


    print("Начинаем 2-ю операцию...")
    timer_start_one_for = time.perf_counter()

    for str_1 in mass_1:
        if (str_1 in mass_2):
            result_2.append(str_1)

    timer_end_one_for = time.perf_counter()
    file3_double_for.writelines(result_2)
    print(f"Обработка данных (one for) заняла {timer_end_one_for - timer_start_one_for:0.4f} секунд")


    print("Начинаем 3-ю операцию...")
    timer_start_generator = time.perf_counter()

    result_3 = [str_1 for str_1 in mass_1 if str_1 in mass_2]

    timer_end_generator = time.perf_counter()
    file3_generator.writelines(result_3)
    print(f"Обработка данных (generator) заняла {timer_end_generator - timer_start_generator:0.4f} секунд")
