from googleapiclient.discovery import build
import pandas as pd
import re

def entry_point(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    intent_name = request_json["queryResult"]["intent"]["displayName"]
    if intent_name == "course-title":
        output = get_course_title(request_json)
        return {"fulfillmentText": output}

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# google sheet ID for each document
ug_courses_sheetId = "1tZsYptvGCa6qEF4kRlTSVyDsdhcOyAeyUmDA29QTrhE"
course_lecturers_sheetId = "1KdW-nySPmITUHsGIicx4Km25y8SqPAxp-YavFTkRqFA"
lecturer_info_sheetId = "1TxbKaWYp8SjBkrTk2BUD-grNBrPR1aza4VBBAcn4ppc"

sheet_range = "Sheet1"
# credential = ServiceAccountCredentials.from_json_keyfile_name("compeng_sheets.json", scopes=scope)

service = build('sheets', 'v4')
sheet = service.spreadsheets()


def read_ug_courses():
    """
    reads "ug_courses" google sheet and returns a data frame
    :return: pandas dataframe
    """
    result = sheet.values().get(spreadsheetId=ug_courses_sheetId, range=sheet_range).execute()
    values = result.get("values", [])
    if not values:
        print("No data Found")
        raise ValueError("No Data Found")
    df_ug_courses = pd.DataFrame(values[1:], columns=values[0][:-1])
    return df_ug_courses


def read_course_lecturers():
    """
    reads "course_lecturers" google sheet and returns it as a dataframe
    :return:
    """
    result = sheet.values().get(spreadsheetId=course_lecturers_sheetId, range=sheet_range).execute()
    values = result.get("values", [])
    if not values:
        print("No data Found")
        raise ValueError("No Data Found")
    else:
        df_course_lecturers = pd.DataFrame(values[1:], columns=values[0])
        return df_course_lecturers


def read_lecturer_info():
    """
    reads "lecturer_info" google sheets and returns it as a pandas dataframe
    :return:
    """
    result = sheet.values().get(spreadsheetId=lecturer_info_sheetId, range=sheet_range).execute()
    values = result.get("values", [])
    if not values:
        print("No data Found")
        raise ValueError("No Data Found")
    else:
        print(values)
        df_lecturer_info = pd.DataFrame(values[1:], columns=values[0])
        return df_lecturer_info


def get_course_title(request_json):
    """
    searches a provided course and returns its course title
    :param request_json: a json containing parameters from the Webhook request
    :return:
    """
    parameters = request_json["queryResult"]["parameters"]
    
    courses_parameter = parameters.get("courses", None)

    if courses_parameter is None:
        print("No courses specified")
    elif isinstance(courses_parameter, str):
        courses_parameter = [courses_parameter]
    else:
        pass
    
    # remove spaces in each course and capitalize it
    course_codes = [re.sub("\s", "", course_code).upper() for course_code in courses_parameter]
    
    # get the data fram of all courses 
    df_ug_courses = read_ug_courses()
    
    # course titles that match the input courses
    course_titles_series = df_ug_courses[df_ug_courses.course_code.isin(course_codes)]["title"]
    
    # check if the course outline is not empty
    if not course_titles_series.empty:
        course_titles_list = list(course_titles_series.values)
        print(course_titles_list)
        course_outlines = " ".join(course_titles_list)
        return course_outlines
    else:
        message = "{} was not found. Try another searching another course".format(course_codes)
        return message