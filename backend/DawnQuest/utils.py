from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from core.models import CoreQuestionType, Question

def send_response(result=True, message="", error=None, data=None):
    if not result:
        status_code = status.HTTP_400_BAD_REQUEST
        response = {
            'success': 'False',
            'status code': status_code,
            'message': message,
        }
        if error is not None:
            response.__setitem__("error", error)
    else:
        status_code = status.HTTP_200_OK
        response = {
            'success': 'True',
            'status code': status_code,
            'message': message,
        }
        if data is not None:
            response.__setitem__("data", data)

    return Response(response, status=status_code)

# Parse Question Paper format

questions_queryset = None
def parse_tree(tree, chapters=[]):
    print(tree)
    global questions_queryset 
    questions_queryset = Question.objects.filter(chapter__in=chapters)
    questions = []
    result = {"data_type":"questionaire",
              "total_marks":tree['data']['marks']}
    for node in tree['children']:
        parse_node(node, result, questions_=questions)
    meta = {"format_id":tree['data']['data'], "question_ids": questions }
    ret = {"result":result, "meta":meta}
    return ret


def parse_node(node , result, from_=None, questions_=[]):
    global questions_queryset
    if node['data']['node_type'] == 2 and "_" not in node['data']['data']:
        result[f"{node['data']['data']}"] = {
            "has_subquestions":True if node['children'][0]['data']['node_type'] != 3 else False,
            "marks":node['data']['marks'],
            "data":[]
        }
        fr = node['data']['data'] 
        for node_ in node['children']:
            parse_node(node_, result, from_=fr, questions_=questions_)

    elif node['data']['node_type'] == 2 and "_" in node['data']['data']:
        result[f"{node['data']['data'].split('_')[0]}"]['data'].append({
            "data_type":"sub_question",
            "content":node['data']['data'].split('_')[-1],
            "marks":node['data']['marks'],
            "data":[]
        })
        fr = node['data']['data']
        for node_ in node['children']:
            parse_node(node_, result, from_=fr, questions_= questions_)

    elif node['data']['node_type'] == 3:
        # 
        total_marks = node['data']['marks']
        allowed_question_types = node['data']['question_type']
        selected_questions = list()
        # print(questions_queryset)
        
        print(allowed_question_types)
        questions = questions_queryset.filter(core_type__in=allowed_question_types).order_by("?")
        accumulated_marks = 0
        for question in questions:
            marks = question.core_type.marks
            if accumulated_marks + marks <= total_marks:
                selected_questions.append(question)
                accumulated_marks += marks

        while accumulated_marks > total_marks:
            excess_question = selected_questions.pop()
            accumulated_marks -= excess_question.core_type.marks



        print("heyy", selected_questions)

        data ={
            "data_type":"question",
            "content":"Question",
            # "question_type":CoreQuestionType.objects.filter(id__in=node['data']['question_type'])
        }

        
        if from_ is not None and "_" not in from_:
            for question in selected_questions:
                questions_.append(question.id)
                data ={
                "data_type":"question",
                "content":question.question,
                "question_type":question.core_type.name,
                "marks":question.core_type.marks
            }
            # data['marks'] = total_marks
            # for types in node['data']['question_type']:

                result[from_]['data'].append(data)
        # 
          

        elif from_ is not None and "_" in from_:
            q = result[from_.split("_")[0]]
            for sub in q['data']:
                if sub['content'] == from_.split("_")[-1]:
                    # print(sub)
                    for question in selected_questions:
                        questions_.append(question.id)
                        data ={
                        "data_type":"question",
                        "content":question.question,
                        "question_type":question.core_type.name,
                        "marks":question.core_type.marks
                    }
                        sub['data'].append(data)
    


