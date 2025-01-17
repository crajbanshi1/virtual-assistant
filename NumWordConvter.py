class NumWordConvter:

    __num2words = {
        1: "One",
        2: "Two",
        3: "Three",
        4: "Four",
        5: "Five",
        6: "Six",
        7: "Seven",
        8: "Eight",
        9: "Nine",
        0: "Zero",
    }

    __tenNumbers = {
        10: "Ten",
        11: "Eleven",
        12: "Twelve",
        13: "Thirteen",
        14: "Fourteen",
        15: "Fifteen",
        16: "Sixteen",
        17: "Seventeen",
        18: "Eighteen",
        19: "Nineteen",
        20: "Twenty",
        30: "Thirty",
        40: "Forty",
        50: "Fifty",
        60: "Sixty",
        70: "Seventy",
        80: "Eighty",
        90: "Ninety",
    }

    __amerinaSystem = {
        2: "Hundred",
        3: "Thousand",
        6: "Million",
        9: "Billion",
        12: "Trillion",
        15: "Quadrillion",
        18: "Quintillion",
        21: "Sextillion",
        24: "Septillion",
        27: "Octillion",
        30: "Nonillion",
        33: "Decillion",
    }

    __amerinaSystem = dict(
        sorted(__amerinaSystem.items(), key=lambda item: item[0], reverse=True)
    )

    __indianSystem = {
        2: "Sata",
        3: "Sahasra",
        5: "Lakh",
        7: "Crore",
        12: "śaṅku",
        17: "mahāśaṅku",
        22: "vr̥nda",
        27: "mahāvr̥nda",
        32: "padma",
        37: "mahāpadma",
        42: "kharva",
        47: "mahākharva",
        52: "samudra",
        57: "ogha",
        62: "mahaugha",
    }

    def __init__(self):
        self.__indianSystem = dict(
            sorted(self.__indianSystem.items(), key=lambda item: item[0], reverse=True)
        )

    def __higher_n2w(self, n, pow, numSystem):
        div = 10**pow
        fpart = ""
        if int((n - n % div) / div) > 0:
            fpart = self.__n2w(int((n - n % div) / div)) + " " + numSystem[pow]
        return fpart + " " + self.__n2w(n % div)

    def __n2w(self, n):
        try:
            numSystem = self.__amerinaSystem
            num_length = len(str(n))

            if n == 0:
                return ""
            elif num_length == 1:
                return self.__num2words[n]
            elif num_length == 2:
                ex = ""
                if n % 10 != 0:
                    ex = self.__num2words[n % 10]
                return self.__tenNumbers[n - n % 10] + ex
            else:
                for key, words in numSystem.items():
                    if num_length >= key + 1:
                        return self.__higher_n2w(n, key, numSystem)
        except KeyError:
            print("Number out of range")
            return str(n)

    def n2w(self, n):
        n = str(n).replace(",", "")
        dec = str(n).split(".")
        string = self.__n2w(int(dec[0]))

        if len(dec) >= 2:
            string += " point"
            for i in dec[1]:
                string += " " + self.__n2w(int(i))
        return string

    def __getWord(self, pre, wo):
        n = 0
        s = wo.replace(pre, "")
        for key, nums in self.__tenNumbers.items():
            if nums.lower() == pre:
                n += key
        for key, nums in self.__num2words.items():
            if s == nums.lower():
                n += key
        return n

    def __w2n(self, string):
        try:
            numSystem = self.__amerinaSystem
            words = string.split(" ")
            num = []
            tens = []

            for word in words:
                if word.isnumeric():
                    word = self.n2w(int(word))

                for key, nums in self.__tenNumbers.items():
                    if word.lower().startswith(nums.lower()):
                        n = self.__getWord(nums.lower(), word.lower())
                        tens.append(n)

                for key, nums in self.__num2words.items():
                    nums.lower(), word.lower()
                    if word.lower() == nums.lower():
                        tens.append(key)

                for key, illion in numSystem.items():
                    if word.lower() == illion.lower():
                        thiszeros = 10**key
                        if len(num) > 0 and num[len(num) - 1] < thiszeros:
                            p = num.pop()
                            num.append(p * thiszeros)

                        num.append(thiszeros)

            res = tens.pop()
            tens = list(reversed(tens))
            for n in num:
                t = tens.pop()
                res = res + (n * t)
            return res

        except KeyError:
            print("Number out of range")
            return str(n)

    def w2n(self, string):
        dec = string.split("point")
        number = self.__w2n(dec[0])
        pointnum = ""
        if len(dec) >= 2:
            decparts = dec[1].strip().split(" ")
            for i in decparts:
                pointnum += str(self.__w2n(i))
            number += int(pointnum) / 10 ** len(pointnum)
        return number


nwConvter = NumWordConvter()


def number2word(number):
    return nwConvter.n2w(number)


def word2number(string):
    return nwConvter.w2n(string)


if __name__ == "__main__":
    try:
        number = 845079077.987
        print("input", number)
        query = number2word(number)
        print(query)
        # query = "8 Hundred 45 Million 79 Thousand 77"

        number = word2number(str(query))
        print("output", number)

    except Exception as ex:
        print(ex)
