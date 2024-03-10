
your_structure = {'data': {'node_type': 1, 'marks': 20, 'data': 'MH|01|06|20|01', 'question_type': []}, 'id': 4, 'children': [{'data': {'node_type': 2, 'marks': 4, 'data': 'Q5', 'question_type': []}, 'id': 13, 'children': [{'data': {'node_type': 3, 'marks': 4, 'data': 'Q5 Diagram – 4', 'question_type': [8]}, 'id': 18}]}, {'data': {'node_type': 2, 'marks': 6, 'data': 'Q4', 'question_type': []}, 'id': 12, 'children': [{'data': {'node_type': 3, 'marks': 6, 'data': 'Q4 Answer in brief – 6', 'question_type': [4]}, 'id': 17}]}, {'data': {'node_type': 2, 'marks': 6, 'data': 'Q3', 'question_type': []}, 'id': 11, 'children': [{'data': {'node_type': 2, 'marks': 2, 'data': 'Q3_B', 'question_type': []}, 'id': 20, 'children': [{'data': {'node_type': 3, 'marks': 2, 'data': 'Chart – 2', 'question_type': [4]}, 'id': 22}]}, {'data': {'node_type': 2, 'marks': 4, 'data': 'Q3_A', 'question_type': []}, 'id': 19, 'children': [{'data': {'node_type': 3, 'marks': 4, 'data': 'Short note – 4', 'question_type': [4]}, 'id': 21}]}]}, {'data': {'node_type': 2, 'marks': 2, 'data': 'Q2', 'question_type': []}, 'id': 10, 'children': [{'data': {'node_type': 3, 'marks': 2, 'data': 'Match the columns / One word answer / True or False / One line answer', 'question_type': [1, 5, 7, 3, 2]}, 'id': 15}]}, {'data': {'node_type': 2, 'marks': 2, 'data': 'Q1', 'question_type': []}, 'id': 9, 'children': [{'data': {'node_type': 3, 'marks': 2, 'data': 'FIB/MCQ', 'question_type': [1]}, 'id': 14}]}]}



def parse_tree(tree):
    result = {"data_type":"questionaire",
              "total_marks":tree['data']['marks']}
    for node in tree['children']:
        parse_node(node, result)

        
    return result

def parse_node(node , result, from_=None):
    # print(node)
    if node['data']['node_type'] == 2 and "_" not in node['data']['data']:
        result[f"{node['data']['data']}"] = {
            "has_subquestions":True if node['children'][0]['data']['node_type'] != 3 else False,
            "marks":node['data']['marks'],
            "data":[]
        }
        fr = node['data']['data'] 
        for node_ in node['children']:
            parse_node(node_, result, from_=fr)

    elif node['data']['node_type'] == 2 and "_" in node['data']['data']:
        result[f"{node['data']['data'].split('_')[0]}"]['data'].append({
            "data_type":"sub_question",
            "content":node['data']['data'].split('_')[-1],
            "marks":node['data']['marks'],
            "data":[]
        })
        fr = node['data']['data']
        for node_ in node['children']:
            parse_node(node_, result, from_=fr)

    elif node['data']['node_type'] == 3:
        print(node)
        if from_ is not None and "_" not in from_:
            result[from_]['data'].append({
                "data_type":"question",
                "content":"Question",
            })

        elif from_ is not None and "_" in from_:
            q = result[from_.split("_")[0]]
            for sub in q['data']:
                if sub['content'] == from_.split("_")[-1]:
                    sub['data'].append({
                        "data_type":"question_type"
                    })
            # q = result[from_.split("_")[0]]
            # for sub_qs in q:
                # print(sub_qs)
                # if sub_qs['content'] == from_.split("_")[-1]:
                #     sub_qs['data'].append({
                #         "data_type":"question_type"
                #     }) 
            # print(sub_qs)
    
    # print(result)

parse_tree(your_structure)
# print(parse_tree(your_structure))