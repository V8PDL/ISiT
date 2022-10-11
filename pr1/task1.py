import csv
from fractions import Fraction
from deep_translator import GoogleTranslator
from matplotlib import colors

def add_drink_type(drink_dict, drink_type):
    if drink_type in drink_dict:
        drink_dict[drink_type] += 1
    else:
        drink_dict[drink_type] = 1

class attribute:
    def __init__(self, name, value, compare_func):
        self.name = name
        self.value = value
        self.min_score = -1.0
        self.max_score = -1.0
        self.score = -1.0
        self.compare_func = compare_func
        self.normalized_score = -1.0

    def Compare(self, other_value):
        return self.compare_func(self.value, other_value)
    
    def Normalize(self, min_score, max_score):
        self.normalized_score = (self.score - min_score) / (max_score - min_score)

    def count_region(self, obj_region):
        return region_data[self + '-' + obj_region]

    def count_sign(self, obj_sign):
        return sign_data[self + '-' + obj_sign]

    def count_fav_col(self, obj_fav_col):
        obj_color = colors.to_rgb(GoogleTranslator(source='auto', target='english').translate(obj_fav_col).replace(" ",""))
        self_color = colors.to_rgb(GoogleTranslator(source='auto', target='english').translate(self).replace(" ",""))
        result_score = 0.0
        for i in range(0,3):
            result_score += abs(obj_color[i] - self_color[i])
        return result_score

    def count_is_working(self, obj_is_working):
        return abs(self - obj_is_working)

    def count_getup_time(self, obj_getup_time):
        return (min(abs(self - obj_getup_time), abs(self - obj_getup_time + 24.0), abs(self - obj_getup_time - 24.0)))

    def count_sleep_time(self, obj_sleep_time):
        return abs(self - obj_sleep_time)

class Object_student:
    def __init__(self, text_str_list, region_data = None, sign_data = None):
        self.name = text_str_list[1]
        self.region = attribute('region', text_str_list[3], attribute.count_region)
        self.sign = attribute('sign', text_str_list[4], attribute.count_sign)
        self.fav_col = attribute('fav_col', text_str_list[5], attribute.count_fav_col)
        self.is_working = attribute('is_working', float(text_str_list[6].replace(',','.')), attribute.count_is_working)
        self.getup_time = attribute('getup_time', float(text_str_list[7].replace(',','.')), attribute.count_getup_time)
        self.sleep_time = attribute('sleep_time', float(text_str_list[8].replace(',','.')), attribute.count_sleep_time)
        
        self.attributes = {}
        self.attributes[self.region.name] = self.region
        self.attributes[self.sign.name] = self.sign
        self.attributes[self.fav_col.name] = self.fav_col
        self.attributes[self.is_working.name] = self.is_working
        self.attributes[self.getup_time.name] = self.getup_time
        self.attributes[self.sleep_time.name] = self.sleep_time
        
        self.drink_type = text_str_list[9].rstrip()
        self.score = -1.0
        self.region_data = region_data
        self.sign_data = sign_data

    def get_score(self):
        self.score = sum(a.normalized_score for a in self.attributes.values())

    def print_all(self):
        print(self.name)
        [print(a.name + " : " + str(a.value)) for a in self.attributes.values()]
        print("Score:" + str(self.score))

    def make_prognose(self, k, data_list):
        # Getting scores of attributes
        for student in data_list:
            for attribute in student.attributes.values():
                curr_attribute = self.attributes[attribute.name]
                score = curr_attribute.Compare(attribute.value)
                if curr_attribute.max_score < 0 or curr_attribute.max_score < score:
                    curr_attribute.max_score =  score
                if curr_attribute.min_score < 0 or curr_attribute.min_score > score:
                    curr_attribute.min_score = score
                attribute.score = score

        [attribute.Normalize(self.attributes[attribute.name].min_score, self.attributes[attribute.name].max_score) for student in data_list for attribute in student.attributes.values()]
        [student.get_score() for student in data_list]
        data_list.sort(key = lambda x: x.score)

        # Get dictionary of (drink_type, drink_count) pairs
        drink_counts_dict = {}
        [add_drink_type(drink_counts_dict, data_list[i].drink_type) for i in range(0, k)]

        for i in range(k - 1, -1, -1):
            drink_values = list(drink_counts_dict.values())
            if drink_values.count(max(drink_values)) == 1:
                return list(drink_counts_dict.keys())[drink_values.index(max(drink_values))]
            else:
                drink_counts_dict[data_list[i].drink_type] -= 1

if __name__ == "__main__":
    object_list = []
    with open('gr.csv', encoding='UTF-8') as file:
        reader = csv.reader(file)
        data = list(reader)
        for text_str in data:
            if text_str[0].isdigit() and text_str[2].lower() != 'н':
                temp_obj = Object_student(text_str)
                object_list.append(temp_obj)

        # Reading "input_region.csv", "input_sign.csv"
        region_data = {}
        sign_data = {}
        with open('input_region.csv', encoding='UTF-8') as input_region:
            for temp_str in list(csv.reader(input_region)):
                region_data[temp_str[0] + '-' + temp_str[1]] = float(Fraction(temp_str[2]))
                region_data[temp_str[1] + '-' + temp_str[0]] = float(Fraction(temp_str[2]))
        with open('input_sign.csv', encoding='UTF-8') as input_data:
            for temp_str in list(csv.reader(input_data)):
                sign_data[temp_str[0] + '-' + temp_str[1]] = float(Fraction(temp_str[2]))
                sign_data[temp_str[1] + '-' + temp_str[0]] = float(Fraction(temp_str[2]))

    #Creating student
    new_student = Object_student(['','Харитонов Борис Иванович','','ЮВАО','Лев','Красный','1','7','6',''], region_data, sign_data)
    new_student_type_drink = new_student.make_prognose(10, object_list)
    print(f"Предполагаю, что {new_student.name} любит: {new_student_type_drink}")