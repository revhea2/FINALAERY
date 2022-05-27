_VARIABLES = {

    "INTEREST": {
        "REALISTIC": {"STEM": 4, "GAS": 3, "HUMSS": 2, "ABM": 1},
        "INVESTIGATE": {"STEM": 4, "ABM": 3, "HUMSS": 2, "GAS": 1},
        "ARTISTIC": {"HUMSS": 4, "GAS": 3, "STEM": 2, "ABM": 1},
        "SOCIAL": {"HUMSS": 4, "GAS": 3, "STEM": 2, "ABM": 1},
        "ENTERPRISING": {"ABM": 4, "GAS": 3, "HUMSS": 2, "STEM": 1},
        "CONVENTIONAL": {"ABM": 4, "STEM": 3, "GAS": 2, "HUMSS": 1}
    },

    "LEARNING_STYLE": {
        "LINGUISTIC": {"HUMSS": 4, "ABM": 3, "GAS": 2, "STEM": 1},
        "LOGICAL": {"STEM": 4, "ABM": 3, "HUMSS": 2, "GAS": 1},
        "SPATIAL": {"ABM": 4, "STEM": 3, "HUMSS": 2, "GAS": 1},
        "BODILY": {"HUMSS": 4, "GAS": 3, "STEM": 2, "ABM": 1},
        "MUSICAL": {"GAS": 4, "HUMSS": 3, "STEM": 2, "ABM": 1},
        "INTERPERSONAL": {"ABM": 4, "HUMSS": 3, "GAS": 2, "STEM": 1},
        "INTRAPERSONAL": {"STEM": 4, "GAS": 3, "HUMSS": 2, "ABM": 1},
        "NATURALIST": {"GAS": 4, "HUMSS": 3, "ABM": 2, "STEM": 1}
    },

    "ACAD_ACHIEVEMENTS": {
        "MATH": {"STEM": 4, "ABM": 3, "GAS": 2, "HUMSS": 1},
        "ENGLISH": {"HUMSS": 4, "ABM": 3, "STEM": 2, "GAS": 1},
        "SCIENCE": {"STEM": 4, "GAS": 3, "HUMSS": 2, "ABM": 1},
        "SOCIAL_SCIENCE": {"HUMSS": 4, "ABM": 3, "GAS": 2, "STEM": 1}
    }

}


def checkDataDependability(data):
    featuresTotal = 0

    #  loop in each feature/category score
    #  and add score.
    for featureScore in range(14):
        featuresTotal += data[featureScore]

    #  if zero meaning there are no checks for learning
    #  style and interest else return nothing.
    if featuresTotal != 0:
        return None

    numberOfIdenticalGrades = 1
    isAllGradePassed = True

    # traverse on each grade
    for gradScoreIdx in range(14, len(data) - 1):

        # check if each grades is similar
        if data[gradScoreIdx] == data[gradScoreIdx + 1]:
            numberOfIdenticalGrades += 1

        # if current grade is below passing grade
        if data[gradScoreIdx] < 75:
            isAllGradePassed = False

    # incomplete grades or each grade didn't met the passing 
    # grade.
    if not isAllGradePassed:
        return "N/A"

    # If all grades are equal and thee value of learning style
    #  and interest is zero then return the gas strand.
    if numberOfIdenticalGrades == 4:
        return 'GAS'

    # we return nothing
    return None


#  https://www.statisticshowto.com/weighting-factor/
def WeightFactorAlgorithm(data):
    # store the weight result
    result = {"HUMSS": 0, "GAS": 0, "STEM": 0, "ABM": 0}

    # check first for special cases
    spRes = checkDataDependability(data)

    # if spRes is not none, meaning there is an answer returned by
    # the checkDataDependability() function then we return 
    # the value otherwise proceed to main algorithm.
    if (spRes != None):
        return spRes
    else:

        # pointer location of input data.
        data_counter_idx = 0

        # loop to 3 variables.
        for variable_id, variable_value in _VARIABLES.items():

            # store all categories to categories variable.
            categories = variable_value
            # stores in temp counter all processed weights in our
            # current variable.
            temp_counter = {"HUMSS": 0, "GAS": 0, "STEM": 0, "ABM": 0}

            # loop through all category in that variable.
            for _, category_value in categories.items():

                # get all strands from categories variable.
                strands = category_value
                for strand_name, strand_value in strands.items():

                    # get the score from the input data.
                    test_score = data[data_counter_idx]

                    # Check if the score is not zero.
                    if (test_score > 0):
                        # check if the current variable id is not the 
                        # acad achievements. We conditioned it because
                        # we need to edit the max range of the grade to 
                        # equally from other variables.
                        if (variable_id != "ACAD_ACHIEVEMENTS"):
                            # continiously add weights for each strand 
                            temp_counter[strand_name] += (strand_value * test_score)
                        else:
                            # continiously add weights for each strand 
                            temp_counter[strand_name] += (strand_value) * ((test_score / 10) - 2)

                # move the data pointer to the right
                data_counter_idx += 1

            # multiply on the variable distribution
            # then store the final result in our result list.
            for temp_counter_id, _ in temp_counter.items():
                result[temp_counter_id] += temp_counter[temp_counter_id]

    print("Weighting factor Result: ", result)

    # return the result
    return [result["STEM"], result["HUMSS"], result["ABM"], result["GAS"]]


if __name__ == "__main__":
    x = [3, 2, 3, 1, 4, 4, 4, 5, 5, 5, 6, 3, 5, 6, 86, 81, 84, 87]
    print(WeightFactorAlgorithm(x))
