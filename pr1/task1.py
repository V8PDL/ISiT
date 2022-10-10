import csv
from fractions import Fraction
from deep_translator import GoogleTranslator
from matplotlib import colors
from operator import attrgetter

class Simple_class:
    def __init__(self, _score, _drink_type):
        self.score = _score
        self.drink_type = _drink_type

class Object_student:
    def __init__(self, text_str_list):
        self.name = text_str_list[1]
        self.region = text_str_list[3]
        self.sign = text_str_list[4]
        self.fav_col = text_str_list[5]
        self.is_working = float(text_str_list[6].replace(',','.'))
        self.getup_time = float(text_str_list[7].replace(',','.'))
        self.sleep_time = float(text_str_list[8].replace(',','.'))
        self.drink_type = text_str_list[9].rstrip()

    def print_all(self):
        print(self.name, self.region, self.sign, self.fav_col, self.is_working, self.getup_time, self.sleep_time, self.drink_type)

    def count_region(self, all_obj_region_data, obj_region):
        return all_obj_region_data[self.region+'-'+obj_region]

    def count_sign(self, all_obj_sign_data, obj_sign):
        return all_obj_sign_data[self.sign+'-'+obj_sign]

    def count_fav_col(self,obj_fav_col):
        obj_color = colors.to_rgb(GoogleTranslator(source='auto', target='english').translate(obj_fav_col).replace(" ",""))
        self_color = colors.to_rgb(GoogleTranslator(source='auto', target='english').translate(self.fav_col).replace(" ",""))
        result_score = 0.0
        for i in range(0,3):
            result_score += abs(obj_color[i] - self_color[i])
        return result_score/3

    def count_is_working(self, obj_is_working):
        return abs(self.is_working - obj_is_working)

    def count_getup_time(self, all_obj_getup_difference, obj_getup_time):
        return abs(self.getup_time - obj_getup_time)/all_obj_getup_difference

    def count_sleep_time(self, all_obj_sleep_difference, obj_sleep_time):
        return (min(abs(self.sleep_time - obj_sleep_time), abs(self.sleep_time - obj_sleep_time + 24.0), abs(self.sleep_time - obj_sleep_time - 24.0)))/all_obj_sleep_difference

    def make_prognose(self, k, data_list):
        region_data = {}
        sign_data = {}
        min_sleep_time = -1.0
        max_sleep_time = 0
        min_getup_time = -1.0
        max_getup_time = 0
        #Reading "input_region.csv", "input_sign.csv"
        with open('input_region.csv', encoding='UTF-8') as input_region:
            for temp_str in list(csv.reader(input_region)):
                region_data[temp_str[0] + '-' + temp_str[1]] = float(Fraction(temp_str[2]))
                region_data[temp_str[1] + '-' + temp_str[0]] = float(Fraction(temp_str[2]))
        with open('input_sign.csv', encoding='UTF-8') as input_data:
            for temp_str in list(csv.reader(input_data)):
                sign_data[temp_str[0] + '-' + temp_str[1]] = float(Fraction(temp_str[2]))
                sign_data[temp_str[1] + '-' + temp_str[0]] = float(Fraction(temp_str[2]))
        #Getting min and max values for sleep_time and getup_time. Counting difference
        to_count_min_and_max_data_list = data_list.copy()
        to_count_min_and_max_data_list.append(self)
        for obj_data in to_count_min_and_max_data_list:
            if(obj_data.sleep_time < min_sleep_time or min_sleep_time == -1.0):
                min_sleep_time = obj_data.sleep_time
            if(obj_data.sleep_time > max_sleep_time):
                max_sleep_time = obj_data.sleep_time
            if(obj_data.getup_time < min_getup_time or min_getup_time == -1.0):
                min_getup_time = obj_data.getup_time
            if(obj_data.getup_time > max_getup_time):
                max_getup_time = obj_data.getup_time
        sleep_time_difference = abs(max_sleep_time - min_sleep_time)
        getup_difference = min(abs(max_getup_time - min_getup_time), abs(max_getup_time - min_getup_time + 24.0), abs(max_getup_time - min_getup_time - 24.0))
        print(min_sleep_time,max_sleep_time,sleep_time_difference)
        print(min_getup_time,max_getup_time,getup_difference)
        #Looking for the most similar data
        all_data_score_drink_list = []
        for obj_data in data_list:
            obj_data_score = self.count_region(region_data, obj_data.region) + self.count_sign(sign_data,obj_data.sign) + self.count_fav_col(obj_data.fav_col) + self.count_is_working(obj_data.is_working) + self.count_getup_time(getup_difference, obj_data.getup_time) + self.count_sleep_time(sleep_time_difference, obj_data.sleep_time)
            obj_data.print_all()
            print(obj_data_score)
            local_simple_object = Simple_class(obj_data_score, obj_data.drink_type)
            all_data_score_drink_list.append(local_simple_object)
        all_data_score_drink_list.sort(key=attrgetter('score'))
        do_while = True
        while(do_while and k != 0):
            result_dict = {}
            for i in range (0,k):
                if(all_data_score_drink_list[i].drink_type in list(result_dict.keys())):
                    result_dict[all_data_score_drink_list[i].drink_type] += 1
                else:
                    result_dict[all_data_score_drink_list[i].drink_type] = 1
            print(result_dict)
            if(list(result_dict.values()).count(max(list(result_dict.values()))) == 1):
                do_while = False
                result = list(result_dict.keys())[list(result_dict.values()).index(max(list(result_dict.values())))]
            else:
                k-=1
        return result

if __name__ == "__main__":
    object_list = []
    with open('gr.csv', encoding='UTF-8') as file:
        reader = csv.reader(file)
        data = list(reader)
        for text_str in data:
            if text_str[0].isdigit() and text_str[2].lower() != 'н':
                temp_obj = Object_student(text_str)
                object_list.append(temp_obj)
    #Creating student
    new_student = Object_student(['','Харитонов Борис Иванович','','МО','Лев','Красный','1','7','9',''])
    new_student_type_drink = new_student.make_prognose(10, object_list)
    print(f"Предполагаю, что {new_student.name} любит: {new_student_type_drink}")