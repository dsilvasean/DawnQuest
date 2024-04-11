from users.models import User

from core.models import Question

from Assessment.models import QuestionPaperFormatIndex, Assessment

class AssessmentGenerator():
    def __init__(self, format_id, user, chapters):
        self.format_id = format_id
        self.user = User.objects.get(id=user)
        self.tree = None
        self.chapters = chapters
        self.questions_queryset = None
        self.result = {}
        self.questions = []
        self.remove_old_questions = True

        self._populate_format_tree()
        self._populate_questions_queryset()


    def _populate_questions_queryset(self):
        if self.remove_old_questions:
            blacklisted_questions_queryset = Question.objects.filter(assessment__created_by=self.user, assessment__marks=20, assessment__subject_id=87)
            self.questions_queryset = Question.objects.filter(chapter__in=self.chapters).exclude(id__in=blacklisted_questions_queryset)
        else:
            self.questions_queryset = Question.objects.filter(chapter__in=self.chapters) 
            return
    
    def _populate_format_tree(self):
        self.tree = QuestionPaperFormatIndex.objects.get(id=self.format_id).format.dump_bulk()[0]
    
    def _post_process(self):
        assessment_instance = Assessment.objects.create(created_by=self.user, marks=20, raw_json=self.result, format_id_id=self.format_id, subject_id=87)
        assessment_instance.chapters.add(*self.chapters)
        assessment_instance.questions.add(*self.questions)
        assessment_instance.save()

    def generate_json(self):
        self.result = {"data_type":"questionaire",
                    "total_marks":self.tree['data']['marks']}
        for node in self.tree['children']:
            self._parse_node(node)

        meta = {"format_id":self.tree['data']['data'], "question_ids":self.questions}
        resp = {"result":self.result, "meta":meta}
        self._post_process()
        return resp


    def _parse_node(self,node, from_=None):
        # node is a main question  
        if node['data']['node_type'] == 2 and "_" not in node['data']['data']:
            self.result[f"{node['data']['data']}"] = {
            "has_subquestions":True if node['children'][0]['data']['node_type'] != 3 else False,
            "marks":node['data']['marks'],
            "data":[]
        }   
            from_ = node['data']['data']
            for node_ in node['children']:
                self._parse_node(node_,from_)
        
        # node is a sub question
        elif node['data']['node_type'] == 2 and "_" in node['data']['data']:
            self.result[f"{node['data']['data'].split('_')[0]}"]['data'].append({
            "data_type":"sub_question",
            "content":node['data']['data'].split('_')[-1],
            "marks":node['data']['marks'],
            "data":[]
        })
            from_ = node['data']['data']
            for node_ in node['children']:
                self._parse_node(node_, from_=from_,)
        
        # node is question
        elif node['data']['node_type'] == 3:
            total_marks = node['data']['marks']
            allowed_question_types = node['data']['question_type']
            accumulated_marks = 0
            _selected_questions = list()
            _questions = self.questions_queryset.filter(core_type__in=allowed_question_types).order_by("?")
            for question in _questions:
                marks = question.core_type.marks
                if accumulated_marks + marks <= total_marks:
                    _selected_questions.append(question)
                    accumulated_marks += marks
            
            while accumulated_marks > total_marks:
                excess_question = _selected_questions.pop()
                accumulated_marks -= excess_question.core_type.marks
            
            if from_ is not None and "_" not in from_:
                for question in _selected_questions:
                    self.questions.append(question.id)
                    data ={
                    "data_type":"question",
                    "content":question.question,
                    "question_type":question.core_type.name,
                    "marks":question.core_type.marks
                }
                    self.result[from_]['data'].append(data)
            
            elif from_ is not None and "_" in from_:
                q = self.result[from_.split("_")[0]]
                for sub in q['data']:
                    if sub['content'] == from_.split("_")[-1]:
                        for question in _selected_questions:
                            self.questions.append(question.id)
                            data ={
                            "data_type":"question",
                            "content":question.question,
                            "question_type":question.core_type.name,
                            "marks":question.core_type.marks
                        }
                            sub['data'].append(data)

        