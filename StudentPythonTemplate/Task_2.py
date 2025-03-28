##########################################################################################
# Task 2 [6 points out of 30] Basic evaluation
# Evaluate your classifier. On your own, implement a method that will create a confusion matrix based on the provided
# classified data. Then implement methods that will return TPs, FPs and FNs based on the confusion matrix.
# From these, implement binary precision, recall and f-measure, and their macro counterparts.
# Finally, implement the multiclass version of accuracy.
# Remember to be mindful of edge cases (the approach for handling them is explained in lecture slides).
# The template contains a range of functions you must implement and use appropriately for this task.
# The template also uses a range of functions implemented by the module leader to support you in this task,
# particularly relating to reading images and csv files accompanying this portfolio.
# You can start working on this task immediately. Please consult at the very least Week 3 materials.
##########################################################################################

import Helper
import Dummy
import numpy
from Task_1 import classification_scheme

# This function computes the confusion matrix based on the provided data.
#
# INPUT: classified_data   : a numpy array containing paths to images, actual classes and predicted classes.
#                            Please refer to Task 1 for precise format description. Remember, this data contains
#                            header row!
# OUTPUT: confusion_matrix : a numpy array representing the confusion matrix computed based on the classified_data.
#                            The order of elements MUST be the same as in the classification scheme.
#                            The columns correspond to actual classes and rows to predicted classes.
#                            In other words, confusion_matrix[0] should be understood
#                            as the row of values predicted as Female, and [row[0] for row in confusion_matrix] as the
#                            column of values that were actually Female (independently of if the classified data
#                            contained Female entries or not).

def confusionMatrix(classified_data: numpy.typing.NDArray) -> numpy.typing.NDArray:
    # skipping the header row
    classified_data = classified_data[1:]
    
    # making the 5x5 matrix filled with 0s based on the number of classes seen in task 1
    num_classes = len(classification_scheme)
    confusion_matrix = numpy.zeros((num_classes, num_classes), dtype=int)
    
    # Filling the confusion matrix
    for row in classified_data:
        
        #Getting the actual and predicted classes 
        actual_class = row[1]  
        predicted_class = row[2]  
        
        #error prevention and converting the classes to indexes
        if actual_class in classification_scheme and predicted_class in classification_scheme:
            actual_index = classification_scheme.index(actual_class)
            predicted_index = classification_scheme.index(predicted_class)
            confusion_matrix[predicted_index, actual_index] += 1
    
    return confusion_matrix


# These functions compute per-class true positives and false positives/negatives based on the provided confusion matrix.
#
# INPUT: confusion_matrix : the numpy array representing the confusion matrix computed based on the classified_data.
#                           The order of elements is the same as  in the classification scheme.
#                           The columns correspond to actual classes and rows to predicted classes.
# OUTPUT: a list of ints representing appropriate true positive, false positive or false
#         negative values per a given class, in the same order as in the classification scheme. For example, tps[1]
#         corresponds to TPs for Male class.


def computeTPs(confusion_matrix: numpy.typing.NDArray) -> list[int]:
    # Have fun! Below is just a dummy for returns, feel free to edit
    tps = []
    #getting the diagonal values
    for i in range(len(confusion_matrix)):
        tp = confusion_matrix[i][i]
        tps.append(tp)
    return tps


def computeFPs(confusion_matrix: numpy.typing.NDArray) -> list[int]:
    # Have fun! Below is just a dummy for returns, feel free to edit
    fps = []
    #getting the sums of non-diagonal values in the rows
    for i in range(len(confusion_matrix)):
        fp = 0
        for j in range(len(confusion_matrix)):
            if i != j:
                fp += confusion_matrix[i][j]
        fps.append(fp)
    return fps


def computeFNs(confusion_matrix: numpy.typing.NDArray) -> list[int]:
    # Have fun! Below is just a dummy for returns, feel free to edit
    fns = []
    #getting the sums of non-diagonal values in the columns
    for i in range(len(confusion_matrix)):
        fn = 0
        for j in range(len(confusion_matrix)):
            if i != j:
                fn += confusion_matrix[j][i]
        fns.append(fn)
    return fns


# These functions compute the binary measures based on the provided values. Not all measures use all of the values.
#
# INPUT: tp, fp, fn : the values of true positives, false positive and negatives
# OUTPUT: appropriate evaluation measure created using the binary approach.

def computeBinaryPrecision(tp: int, fp: int, fn: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    precision = float(0)

    if tp + fp > 0:
        precision = float(tp) / float(tp + fp)
    return precision


def computeBinaryRecall(tp: int, fp: int, fn: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    recall = float(0)
    if tp + fn > 0:
        recall = float(tp) / float(tp + fn)
    return recall


def computeBinaryFMeasure(tp: int, fp: int, fn: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    f_measure = float(0)
    precision = computeBinaryPrecision(tp, fp, fn)
    recall = computeBinaryRecall(tp, fp, fn)
    if precision + recall > 0:
        f_measure = 2 * precision * recall / (precision + recall)
    return f_measure


# These functions compute the evaluation measures based on the provided values - macro precision, macro recall,
# macro f-measure, and accuracy (multiclass version). Not all measures use of all the values.
# You are expected to use appropriate binary counterparts when needed (binary recall for macro recall, binary precision
# for macro precision, binary f-measure for macro f-measure).
#
# INPUT: tps, fps, fns, data_size
#                       : the per-class true positives, false positive and negatives, and number of classified entries
#                         in the classified data (aka, don't count the header!)
# OUTPUT: appropriate evaluation measures created using the macro-average approach.

def computeMacroPrecision(tps: list[int], fps: list[int], fns: list[int], data_size: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    precision = float(0)

    total_classes = len(tps)
    if total_classes == 0:
        return precision
    
    total_precision = 0.0
    for i in range(total_classes):
        class_precision = 0.0
        if tps[i] + fps[i] > 0:
            class_precision += float(tps[i]) / float(tps[i] + fps[i])
        total_precision += class_precision

    precision = total_precision / total_classes
    return precision

    


def computeMacroRecall(tps: list[int], fps: list[int], fns: list[int], data_size: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    recall = float(0)
    
    total_classes = len(tps)
    if total_classes == 0:
        return recall
    
    total_recall = 0.0
    for i in range(total_classes):
        class_recall = 0.0
        if tps[i] + fns[i] > 0:
            class_recall = float(tps[i]) / float(tps[i] + fns[i])
        total_recall += class_recall

    recall = total_recall / total_classes
    return recall


def computeMacroFMeasure(tps: list[int], fps: list[int], fns: list[int], data_size: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    f_measure = float(0)
    
    total_classes = len(tps)
    if total_classes == 0:
        return f_measure
    
    total_f_measure = 0.0
    for i in range(total_classes):
        precision = 0.0
        if tps[i] + fps[i] + fns[i] > 0:
            precision = float(tps[i]) / float(tps[i] + fps[i])

        recall = 0.0
        if tps[i] + fns[i] > 0:
            recall = float(tps[i]) / float(tps[i] + fns[i])

        class_f_measure = 0.0
        if precision + recall > 0:
            class_f_measure = 2 * precision * recall / (precision + recall)

        total_f_measure += class_f_measure

    f_measure = total_f_measure / total_classes
    return f_measure


def computeAccuracy(tps: list[int], fps: list[int], fns: list[int], data_size: int) -> float:
    # Have fun! Below is just a dummy for returns, feel free to edit
    accuracy = float(0)
    total_tp = sum(tps)
    accuracy =float(total_tp) / float(data_size)
    return accuracy


# In this function you are expected to compute precision, recall, f-measure and accuracy of your classifier using
# the macro average approach.

# INPUT: classified_data   : a numpy array containing paths to images, actual classes and predicted classes.
#                            Please refer to Task 1 for precise format description.
#       confusion_func     : function to be invoked to compute the confusion matrix
#
# OUTPUT: computed measures
def evaluateKNN(classified_data: numpy.typing.NDArray, confusion_func=confusionMatrix) \
        -> tuple[float, float, float, float]:
    # Have fun! Below is just a dummy for returns, feel free to edit
    precision = float(0)
    recall = float(0)
    f_measure = float(0)
    accuracy = float(0)

    confusion_matrix = confusion_func(classified_data)

    tps = computeTPs(confusion_matrix)
    fps = computeFPs(confusion_matrix)
    fns = computeFNs(confusion_matrix)

    data_size = len(classified_data) - 1  

    precision = computeMacroPrecision(tps, fps, fns, data_size)
    recall = computeMacroRecall(tps, fps, fns, data_size)
    f_measure = computeMacroFMeasure(tps, fps, fns, data_size)
    accuracy = computeAccuracy(tps, fps, fns, data_size)
    
    return precision, recall, f_measure, accuracy


##########################################################################################
# You should not need to modify things below this line - it's mostly reading and writing #
# Be aware that error handling below is...limited.                                       #
##########################################################################################


# This function reads the necessary arguments (see parse_arguments function in Task_1_5),
# and based on them evaluates the kNN classifier.
def main():
    opts = Helper.parseArguments()
    if not opts:
        print("Missing input. Read the README file.")
        exit(1)
    print(f'Reading data from {opts["classified_data"]}')
    classified_data = Helper.readCSVFile(opts['classified_data'])
    if classified_data.size == 0:
        print("Classified data is empty, cannot run evaluation. Exiting Task 2.")
        return
    print('Evaluating kNN')
    result = evaluateKNN(classified_data)
    print('Result: precision {}; recall {}; f-measure {}; accuracy {}'.format(*result))


if __name__ == '__main__':
    main()
