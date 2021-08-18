
class StudyThreeBarsUtil:

    @staticmethod
    def standardDeviation(lst):
        avg = sum(lst) / len(lst)
        var = sum((x-avg)**2 for x in lst) / len(lst)
        std = var**0.5
        return std

    @staticmethod
    def trend_value(nums: list):
        summed_nums = sum(nums)
        multiplied_data = 0
        summed_index = 0
        squared_index = 0

        for index, num in enumerate(nums):
            index += 1
            multiplied_data += index * num
            summed_index += index
            squared_index += index**2

        numerator = (len(nums) * multiplied_data) - \
            (summed_nums * summed_index)
        denominator = (len(nums) * squared_index) - summed_index**2
        if denominator != 0:
            return numerator/denominator
        else:
            return 0

    @staticmethod
    def column(matrix, i):
        return [row[i] for row in matrix]
