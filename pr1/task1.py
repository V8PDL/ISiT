import csv
from fractions import Fraction
from deep_translator import GoogleTranslator
from matplotlib import colors

class attribute:
    def __init__(self, name, value, compare_func, weight = 1):
        self.name = name
        self.value = value
        self.min_score = -1.0
        self.max_score = -1.0
        self.score = -1.0
        self.compare_func = compare_func
        self.normalized_score = -1.0
        self.weight = weight

    def Compare(self, other_value):
        return self.weight * self.compare_func(self, other_value)
    
    def Normalize(self, min_score, max_score):
        self.normalized_score = (self.score - min_score) / (max_score - min_score)

    def count_region(self, obj_region):
        return region_data[self.value + '-' + obj_region]

    def count_sign(self, obj_sign):
        return sign_data[self.value + '-' + obj_sign]

    def count_fav_col(self, obj_fav_col):
        result_score = 0.0
        for i in range(0,3):
            result_score += abs(obj_fav_col[i] - self.value[i])
        return result_score

    def count_is_working(self, obj_is_working):
        return abs(self.value - obj_is_working)

    def count_getup_time(self, obj_getup_time):
        return (min(abs(self.value - obj_getup_time), abs(self.value - obj_getup_time + 24.0), abs(self.value - obj_getup_time - 24.0)))

    def count_sleep_time(self, obj_sleep_time):
        return abs(self.value - obj_sleep_time)

class Student:
    def __init__(self, text_str_list):
        self.name = text_str_list[1]
        self.attributes = {}
        self.attributes['region'] = attribute('region', text_str_list[3], attribute.count_region)
        self.attributes['sign'] = attribute('sign', text_str_list[4], attribute.count_sign)
        str_color = text_str_list[5]
        if str_color in colors_dict:
            color = colors_dict[str_color]
        else:
            color = colors.to_rgb(GoogleTranslator(source='auto', target='english').translate(str_color).replace(" ",""))
            colors_dict[str_color] = color
        self.attributes['fav_col'] = attribute('fav_col', color, attribute.count_fav_col)
        self.attributes['is_working'] = attribute('is_working', float(text_str_list[6].replace(',','.')), attribute.count_is_working)
        self.attributes['getup_time'] = attribute('getup_time', float(text_str_list[7].replace(',','.')), attribute.count_getup_time)
        self.attributes['sleep_time'] = attribute('sleep_time', float(text_str_list[8].replace(',','.')), attribute.count_sleep_time)
        
        self.drink_type = text_str_list[9].rstrip()
        self.score = -1.0

    def set_normalized_score(self):
        self.score = sum(a.normalized_score for a in self.attributes.values())

    def print_all(self):
        print(f"------------------------------------------------------------------------------\n{self.name}\nAttributes:")
        [print(f"{attribute.name}: {str(attribute.value)}; score: {str(attribute.score)}; normalized: {str(attribute.normalized_score)}") for attribute in self.attributes.values()]
        print("Total Score: " + str(self.score))

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

        # Getting all scores (normalized)
        [attribute.Normalize(self.attributes[attribute.name].min_score, self.attributes[attribute.name].max_score) for student in data_list for attribute in student.attributes.values()]
        [student.set_normalized_score() for student in data_list]
        data_list.sort(key = lambda x: x.score)

        # Get dictionary of (drink_type, drink_count) pairs
        drink_counts_dict = {}
        for i in range(0, k):
            if data_list[i].drink_type in drink_counts_dict:
                drink_counts_dict[data_list[i].drink_type] += 1
            else:
                drink_counts_dict[data_list[i].drink_type] = 1

        # Choose most popular variant
        for i in range(k - 1, -1, -1):
            drink_values = list(drink_counts_dict.values())
            if drink_values.count(max(drink_values)) == 1:
                return list(drink_counts_dict.keys())[drink_values.index(max(drink_values))]
            else:
                drink_counts_dict[data_list[i].drink_type] -= 1

if __name__ == "__main__":
    print("Fork of project by Ivanov A.G., Kachanov F.K., Efremov D.S., Gavrilyuk I. P.\nMade by Efremov D.S., Gavrilyuk I. P.\n")
    dataset = []
    colors_dict = {}
    with open('gr.csv', encoding='UTF-8') as file:
        [dataset.append(Student(line)) for line in list(csv.reader(file)) if line[0].isdigit() and line[2].lower() != 'н']

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
    new_student = Student(['','Харитонов Борис Иванович','','ЮВАО','Весы','Красный','0','1','1',''])
    new_student_type_drink = new_student.make_prognose(10, dataset)
    [student.print_all() for student in dataset]
    print('------------------------------------------------------------------------------\n')
    print(f"Предполагаю, что {new_student.name} любит: {new_student_type_drink}")