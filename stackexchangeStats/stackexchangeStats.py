import datetime
import requests
import collections
import json
import json2html
from json2html import *
import argparse


def getArguments():
    """

    Gets the 2 dates in YYYY-MM-DD-HH-MM-SS format and the output format (html or json).

    :return: the 2 dates and the output format
    :rtype: str, str, str
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("stats")
    parser.add_argument("--since", help="Enter the first date in YYYY-MM-DD-HH-MM-SS format", required=True)
    parser.add_argument("--until", help="Enter the second date in YYYY-MM-DD-HH-MM-SS format", required=True)
    parser.add_argument("--output-format", help="Enter the output format (html or json)", choices=['html', 'json'], default=json)
    args = parser.parse_args()
    since = args.since
    until = args.until
    format = args.output_format
    return since, until, format


def getDates(firstDate, secondDate):
    """
    :param firstDate: a date in str format
    :type firstDate: str
    :param secondDate:
    :type secondDate: str
    :return: the 2 Unix time number from the input dates
    :rtype: int, int
    """

    firstDate = getDate(firstDate)
    firstUnixTime = convertToUnixTime(firstDate)
    secondDate = getDate(secondDate)
    secondUnixTime = convertToUnixTime(secondDate)
    return firstUnixTime, secondUnixTime


def getDate(askDate):
    """
    :param askDate: a date in str type in the YYYY-MM-DD-HH-MM-SS format, e.g. 2016-06-02-10-00-00
    :type askDate: str
    :return: the date in the datetime.datetime type
    :rtype: datetime.datetime
    """

    year, month, day, hour, minutes, seconds = map(int, askDate.split('-'))
    date = datetime.datetime(year, month, day, hour, minutes, seconds)
    return date


def convertToUnixTime(date):
    """
    :param date: a date in datetime.datetime type
    :type date: datetime.datetime
    :return: the Unix time of the input date
    :rtype: int
    """

    UnixTime = int((date - datetime.datetime(1970, 1, 1)).total_seconds())
    return UnixTime


def getAnswersFromSpecificPage(pageNum, firstUnixTime, secondUnixTime):
    """
    :param pageNum: the number of the page of the api for the answers
    :type pageNum: str
    :param firstUnixTime: the first Unix time
    :type firstUnixTime: str
    :param secondUnixTime: the second Unix time
    :type secondUnixTime: str
    :return: all the answers in the specific page number, between the two Unix time numbers in a json format
    :rtype: dict
    """

    page = requests.get("https://api.stackexchange.com/2.2/answers?page="+pageNum+"&pagesize=100&fromdate="+firstUnixTime+"&todate="+secondUnixTime+"&order=desc&sort=creation&site=stackoverflow&filter=!8Ifzx5dk2FlHlZ_vFIcbI")
    return page.json()


def getTotalAcceptedAnswers(answer, totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers):
    """

    Increases the number of the total accepted answers by 1, and the total score of the accepted answers by the
    answer's score, if the answer is accepted.

    :param answer: an answer dictionary
    :type answer: dict
    :param totalAcceptedAnswers: the number of the total accepted answers
    :type totalAcceptedAnswers: int
    :param totalScoreOfTotalAcceptedAnswers: the sum of the scores of the accepted answers
    :type totalScoreOfTotalAcceptedAnswers: int
    :return: the number of the total accepted answers and the total score of the accepted answers
    :rtype: int, int
    """

    if answer['is_accepted']:
        totalAcceptedAnswers += 1
        totalScoreOfTotalAcceptedAnswers += answer['score']
        return totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers
    else:
        return totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers


def getTopTenAnswers(answer, topTenAnswers):
    """

    Checks if the answer's score belongs to the top 10 answers. If yes, it adds it in the list depending on its score.

    :param answer: an answer dictionary
    :type answer: dict
    :param topTenAnswers: a list of 10 tuples of the format (answer id, score of the answer), that has the top 10 answers
    :type topTenAnswers: list
    :return: the updated list of the top ten answers
    :rtype: list
    """

    if answer['score'] >= topTenAnswers[9][1]:
        tupleInQuestion = (answer['answer_id'], answer['score'])
        topTenAnswers.insert(9, tupleInQuestion)
        topTenAnswers.pop()
        for times in reversed(range(9)):
            if answer['score'] >= topTenAnswers[times][1]:
                topTenAnswers[times], topTenAnswers[times + 1] = topTenAnswers[times + 1], topTenAnswers[times]
            else:
                break
    return topTenAnswers


def getTopTenAnswersWithCommentsCount(topTenAnswers):
    """
    :param topTenAnswers: the final list of the top 10 answers depending on their score
    :type topTenAnswers: list
    :return: an ordered dictionary of the top 10 answers with the answer_id and their number of comments
    :rtype: collections.OrderedDict
    """

    topTenAnswersWithCommentsCount = collections.OrderedDict()
    for j, k in topTenAnswers:
        totalComments = getComments(str(j))['total']
        topTenAnswersWithCommentsCount[""+str(j)+""] = totalComments
    return topTenAnswersWithCommentsCount


def getComments(answerId):
    """
    :param answerId: the number of the answer id
    :type answerId: str
    :return: the total number of comments for the specific answer id in a json format
    :rtype: dict
    """
    comments = requests.get("https://api.stackexchange.com/2.2/answers/"+answerId+"/comments??order=desc&sort=creation&site=stackoverflow&filter=!GeDDagMb(mX3)")
    return comments.json()


def printOutput(totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers, totalAnswers, questionsSet, topTenAnswersWithCommentsCount, outputFormat):
    """
    :return: Prints the output (in html or json format)
    :rtype:
    """

    finalResults = collections.OrderedDict()
    finalResults.update({"total_accepted_answers": totalAcceptedAnswers})
    finalResults.update({"accepted_answers_average_score": round(totalScoreOfTotalAcceptedAnswers/float(totalAcceptedAnswers), 1)})
    finalResults.update({"average_answers_per_question": round(totalAnswers/float(len(questionsSet)), 1)})
    finalResults.update({"top_ten_answers_comment_count": topTenAnswersWithCommentsCount})
    if outputFormat == 'html':
        print json2html.convert(json=finalResults)
    else:
        print json.dumps(finalResults, indent=4)
    return


if __name__ == '__main__':
    firstDate, secondDate, outputFormat = getArguments()
    firstUnixTime, secondUnixTime = getDates(firstDate, secondDate)
    firstAnswers = getAnswersFromSpecificPage(str(1), str(firstUnixTime), str(secondUnixTime))
    totalAnswers = firstAnswers['total']
    totalPages = totalAnswers/100 + (0 if totalAnswers % 100 == 0 else 1)
    totalAcceptedAnswers = 0
    totalScoreOfTotalAcceptedAnswers = 0
    topTenAnswers = zip([0] * 10, [0] * 10)
    questionsSet = set()
    for pageNumber in range(1, totalPages + 1):
        answers = getAnswersFromSpecificPage(str(pageNumber), str(firstUnixTime), str(secondUnixTime))
        answersItems = answers['items']
        for answer in answersItems:
            totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers = getTotalAcceptedAnswers(answer, totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers)
            topTenAnswers = getTopTenAnswers(answer, topTenAnswers)
            questionsSet.add(answer['question_id'])
    topTenAnswersWithCommentsCount = getTopTenAnswersWithCommentsCount(topTenAnswers)
    printOutput(totalAcceptedAnswers, totalScoreOfTotalAcceptedAnswers, totalAnswers, questionsSet, topTenAnswersWithCommentsCount, outputFormat)