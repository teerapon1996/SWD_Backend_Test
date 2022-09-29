
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from apis.models import SchoolStructure, Schools, Classes, Personnel, Subjects, StudentSubjectsScore
import json
from django.http import HttpResponse


class StudentSubjectsScoreAPIView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        """
        [Backend API and Data Validations Skill Test]

        description: create API Endpoint for insert score data of each student by following rules.

        rules:      - Score must be number, equal or greater than 0 and equal or less than 100.
                    - Credit must be integer, greater than 0 and equal or less than 3.
                    - Payload data must be contained `first_name`, `last_name`, `subject_title` and `score`.
                        - `first_name` in payload must be string (if not return bad request status).
                        - `last_name` in payload must be string (if not return bad request status).
                        - `subject_title` in payload must be string (if not return bad request status).
                        - `score` in payload must be number (if not return bad request status).

                    - Student's score of each subject must be unique (it's mean 1 student only have 1 row of score
                            of each subject).
                    - If student's score of each subject already existed, It will update new score
                            (Don't created it).
                    - If Update, Credit must not be changed.
                    - If Data Payload not complete return clearly message with bad request status.
                    - If Subject's Name or Student's Name not found in Database return clearly message with bad request status.
                    - If Success return student's details, subject's title, credit and score context with created status.

        remark:     - `score` is subject's score of each student.
                    - `credit` is subject's credit.
                    - student's first name, lastname and subject's title can find in DATABASE (you can create more
                            for test add new score).

        """

        subjects_context = [{"id": 1, "title": "Math"}, {"id": 2, "title": "Physics"}, {"id": 3, "title": "Chemistry"},
                            {"id": 4, "title": "Algorithm"}, {"id": 5, "title": "Coding"}]

        credits_context = [{"id": 6, "credit": 1, "subject_id_list_that_using_this_credit": [3]},
                           {"id": 7, "credit": 2, "subject_id_list_that_using_this_credit": [2, 4]},
                           {"id": 9, "credit": 3, "subject_id_list_that_using_this_credit": [1, 5]}]

        credits_mapping = [{"subject_id": 1, "credit_id": 9}, {"subject_id": 2, "credit_id": 7},
                           {"subject_id": 3, "credit_id": 6}, {"subject_id": 4, "credit_id": 7},
                           {"subject_id": 5, "credit_id": 9}]

        student_first_name = request.data.get("first_name", None)
        student_last_name = request.data.get("last_name", None)
        subjects_title = request.data.get("subject_title", None)
        score = request.data.get("score", None)

        # # Filter Objects Example
        # DataModel.objects.filter(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        # # Create Objects Example
        # DataModel.objects.create(filed_1=value_1, filed_2=value_2, filed_2=value_3)

        return Response(status=status.HTTP_201_CREATED)


class StudentSubjectsScoreDetailsAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Backend API and Data Calculation Skill Test]

        description: get student details, subject's details, subject's credit, their score of each subject,
                    their grade of each subject and their grade point average by student's ID.

        pattern:     Data pattern in 'context_data' variable below.

        remark:     - `grade` will be A  if 80 <= score <= 100
                                      B+ if 75 <= score < 80
                                      B  if 70 <= score < 75
                                      C+ if 65 <= score < 70
                                      C  if 60 <= score < 65
                                      D+ if 55 <= score < 60
                                      D  if 50 <= score < 55
                                      F  if score < 50

        """
        try :
            student_id = kwargs.get("id", None)
            #DataModel.objects.filter(filed_1=value_1, filed_2=value_2, filed_2=value_3)
        
            st_id = Personnel.objects.get(pk=student_id)
            # sc = Classes.objects.get(pk=int(st_id.school_class))
            st_detail = StudentSubjectsScore.objects.filter(student__pk = student_id)
            fullname = str(st_id.first_name) +" "+ str(st_id.last_name)
            student_dict = {
                        "id": str(st_id.id),
                        "full_name": fullname,
                        "school": st_id.school_class.school.title
                        }
            example_context_data = {"student":student_dict,"subject_detail":[],"grade_point_average": ""}
            list_st_subj_score = []
            for qrs in st_detail :
                # QuerySet save to list
                list_st_subj_score.append(qrs)
            sum_score = 0
            count_subject = 0
            for obj in list_st_subj_score :
                score = int(obj.score)
                
                if score >= 80:
                    grade = "A"
                elif score >= 75:
                    grade = "B+"
                elif score >= 70:
                    grade = "B"
                elif score >= 65:
                    grade = "C+"
                elif score >= 60:
                    grade = "C"
                elif score >= 55:
                    grade = "D+"
                elif score >= 50 :
                    grade = "D"
                else:
                    grade = "F"
                
                sum_score = sum_score+score
                count_subject +=1
                dict_subj = {
                            "subject": str(obj.subjects) ,
                            "credit": str(obj.credit),
                            "score": str(obj.score),
                            "grade": str(grade),
                }
                example_context_data["subject_detail"].append(dict_subj)
            avg_score = float(sum_score/count_subject)
            example_context_data["grade_point_average"] = avg_score
            return Response(example_context_data)

        except Exception :
            status = {"status":"Failed"}
            return Response(status)
            

class PersonnelDetailsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        [Basic Skill and Observational Skill Test]

        description: get personnel details by school's name.

        data pattern:  {order}. school: {school's title}, role: {personnel type in string}, class: {class's order}, name: {first name} {last name}.

        result pattern : in `data_pattern` variable below.

        example:    1. school: Rose Garden School, role: Head of the room, class: 1, name: Reed Richards.
                    2. school: Rose Garden School, role: Student, class: 1, name: Blackagar Boltagon.

        rules:      - Personnel's name and School's title must be capitalize.
                    - Personnel's details order must be ordered by their role, their class order and their name.

        """
        try :
            school_title = kwargs.get("school_title", None)
            # print(school_title)
            personnel = Personnel.objects.filter(school_class__school__title="Rose Garden School")
            your_result = []
            for index,obj in enumerate(personnel) :
                # print(i.first_name,)
                if obj.personnel_type == 0 :
                    role = "class_teacher"
                elif obj.personnel_type == 1 :
                    role = "head_of_the_room"
                else :
                    role = "student"
                str_school = f'{index+1}. school: {str(obj.school_class.school)}, role: {role} class: {obj.school_class.class_order}, name: {obj.first_name} {obj.last_name}'
                your_result.append(str_school)
            return Response(your_result)

        except Exception :
            status = {"status":"Failed"}
            return Response(status)

class SchoolHierarchyAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get personnel list in hierarchy order by school's title, class and personnel's name.

        pattern: in `data_pattern` variable below.

        """
        try :
            all_school = []
            ########## Query Dorm Palace School ##############
            dorm_all_class = []
            person_class1_dorm = Personnel.objects.filter(school_class__school__title="Dorm Palace School",school_class__class_order=1)
            person_class2_dorm = Personnel.objects.filter(school_class__school__title="Dorm Palace School",school_class__class_order=2)
            person_class3_dorm = Personnel.objects.filter(school_class__school__title="Dorm Palace School",school_class__class_order=3)
            person_class4_dorm = Personnel.objects.filter(school_class__school__title="Dorm Palace School",school_class__class_order=4)
            person_class5_dorm = Personnel.objects.filter(school_class__school__title="Dorm Palace School",school_class__class_order=5)
            dorm_all_class.extend([person_class1_dorm,person_class2_dorm,person_class3_dorm,person_class4_dorm,person_class5_dorm])
            teachers = Personnel.objects.filter(personnel_type=0,school_class__school__title="Dorm Palace School")
            data_dorm = {"school":"Dorm Palace School",
                            "class 1" : {},
                            "class 2" : {},
                            "class 3" : {},
                            "class 4" : {},
                            "class 5" : {},
            }
            for index,unit_class in  enumerate(dorm_all_class):
                list_class = []
                list_teacher = []
                for teacher in teachers :
                    teacher_fullname = f'{teacher.first_name} {teacher.last_name}'
                    list_teacher.append("Teacher : "+ teacher_fullname)
                for personnel in unit_class :
                    # Get head of the room and student 
                    if personnel.personnel_type == 1 :
                        role = "head_of_the_room"
                        dict_pers = {f"{role}":f"{personnel.first_name} {personnel.last_name}"}
                        list_class.append(dict_pers)
                        data_dorm[f"class {index+1}"] = {f'{list_teacher[index]}: {list_class}'}
                    elif personnel.personnel_type == 2 :
                        role = "student"   
                        dict_pers = {f"{role}":f"{personnel.first_name} {personnel.last_name}"}
                        list_class.append(dict_pers)
                        data_dorm[f"class {index+1}"] = {f'{list_teacher[index]}: {list_class}'}
                    else :
                        pass
            all_school.append(data_dorm)    

            ########## Query Rose Garden School ##############
            rose_all_class = []

            person_class1_rose = Personnel.objects.filter(school_class__school__title="Rose Garden School",school_class__class_order=1)
            person_class2_rose = Personnel.objects.filter(school_class__school__title="Rose Garden School",school_class__class_order=2)
            person_class3_rose = Personnel.objects.filter(school_class__school__title="Rose Garden School",school_class__class_order=3)
            person_class4_rose = Personnel.objects.filter(school_class__school__title="Rose Garden School",school_class__class_order=4)
            person_class5_rose = Personnel.objects.filter(school_class__school__title="Rose Garden School",school_class__class_order=5)
            rose_all_class.extend([person_class1_rose,person_class2_rose,person_class3_rose,person_class4_rose,person_class5_rose])
            teachers = Personnel.objects.filter(personnel_type=0,school_class__school__title="Rose Garden School")
            data_rose = {"school":"Rose Garden School",
                            "class 1" : {},
                            "class 2" : {},
                            "class 3" : {},
                            "class 4" : {},
                            "class 5" : {},
            }
            for index,unit_class in  enumerate(rose_all_class):
                list_class = []
                list_teacher = []
                for teacher in teachers :
                    teacher_fullname = f'{teacher.first_name} {teacher.last_name}'
                    list_teacher.append("Teacher : "+ teacher_fullname)
                for personnel in unit_class :
                    # Get head of the room and student 
                    if personnel.personnel_type == 1 :
                        role = "head_of_the_room"
                        dict_pers = {f"{role}":f"{personnel.first_name} {personnel.last_name}"}
                        list_class.append(dict_pers)
                        data_rose[f"class {index+1}"] = {f'{list_teacher[index]}: {list_class}'}
                    elif personnel.personnel_type == 2 :
                        role = "student"   
                        dict_pers = {f"{role}":f"{personnel.first_name} {personnel.last_name}"}
                        list_class.append(dict_pers)
                        data_rose[f"class {index+1}"] = {f'{list_teacher[index]}: {list_class}'}
                    else :
                        pass
            all_school.append(data_rose)

            ########## Query Prepare Udom School ##############
            prepare_all_class = []

            person_class1_prepare = Personnel.objects.filter(school_class__school__title="Prepare Udom School",school_class__class_order=1)
            person_class2_prepare = Personnel.objects.filter(school_class__school__title="Prepare Udom School",school_class__class_order=2)
            person_class3_prepare = Personnel.objects.filter(school_class__school__title="Prepare Udom School",school_class__class_order=3)
            person_class4_prepare = Personnel.objects.filter(school_class__school__title="Prepare Udom School",school_class__class_order=4)
            person_class5_prepare = Personnel.objects.filter(school_class__school__title="Prepare Udom School",school_class__class_order=5)
            prepare_all_class.extend([person_class1_prepare,person_class2_prepare,person_class3_prepare,person_class4_prepare,person_class5_prepare])
            teachers = Personnel.objects.filter(personnel_type=0,school_class__school__title="Prepare Udom School")
            data_prepare = {"school":"Prepare Udom School",
                            "class 1" : {},
                            "class 2" : {},
                            "class 3" : {},
                            "class 4" : {},
                            "class 5" : {},
            }
            for index,unit_class in  enumerate(prepare_all_class):
                list_class = []
                list_teacher = []
                for teacher in teachers :
                    teacher_fullname = f'{teacher.first_name} {teacher.last_name}'
                    list_teacher.append("Teacher : "+ teacher_fullname)
                for personnel in unit_class :
                    # Get head of the room and student 
                    if personnel.personnel_type == 1 :
                        role = "head_of_the_room"
                        dict_pers = {f"{role}":f"{personnel.first_name} {personnel.last_name}"}
                        list_class.append(dict_pers)
                        data_prepare[f"class {index+1}"] = {f'{list_teacher[index]}: {list_class}'}
                    elif personnel.personnel_type == 2 :
                        role = "student"   
                        dict_pers = {f"{role}":f"{personnel.first_name} {personnel.last_name}"}
                        list_class.append(dict_pers)
                        data_prepare[f"class {index+1}"] = {f'{list_teacher[index]}: {list_class}'}
                    else :
                        pass
            all_school.append(data_prepare)
            return Response(all_school)

        except Exception :
            status = {"status":"Failed"}
            return Response(status)

class SchoolStructureAPIView(APIView):

    @staticmethod
    def get(request, *args, **kwargs):
        """
        [Logical Test]

        description: get School's structure list in hierarchy.

        pattern: in `data_pattern` variable below.

        """

        data_pattern = [
            {
                "title": "มัธยมต้น",
                "sub": [
                    {
                        "title": "ม.1",
                        "sub": [
                            {
                                "title": "ห้อง 1/1"
                            },
                            {
                                "title": "ห้อง 1/2"
                            },
                            {
                                "title": "ห้อง 1/3"
                            },
                            {
                                "title": "ห้อง 1/4"
                            },
                            {
                                "title": "ห้อง 1/5"
                            },
                            {
                                "title": "ห้อง 1/6"
                            },
                            {
                                "title": "ห้อง 1/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.2",
                        "sub": [
                            {
                                "title": "ห้อง 2/1"
                            },
                            {
                                "title": "ห้อง 2/2"
                            },
                            {
                                "title": "ห้อง 2/3"
                            },
                            {
                                "title": "ห้อง 2/4"
                            },
                            {
                                "title": "ห้อง 2/5"
                            },
                            {
                                "title": "ห้อง 2/6"
                            },
                            {
                                "title": "ห้อง 2/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.3",
                        "sub": [
                            {
                                "title": "ห้อง 3/1"
                            },
                            {
                                "title": "ห้อง 3/2"
                            },
                            {
                                "title": "ห้อง 3/3"
                            },
                            {
                                "title": "ห้อง 3/4"
                            },
                            {
                                "title": "ห้อง 3/5"
                            },
                            {
                                "title": "ห้อง 3/6"
                            },
                            {
                                "title": "ห้อง 3/7"
                            }
                        ]
                    }
                ]
            },
            {
                "title": "มัธยมปลาย",
                "sub": [
                    {
                        "title": "ม.4",
                        "sub": [
                            {
                                "title": "ห้อง 4/1"
                            },
                            {
                                "title": "ห้อง 4/2"
                            },
                            {
                                "title": "ห้อง 4/3"
                            },
                            {
                                "title": "ห้อง 4/4"
                            },
                            {
                                "title": "ห้อง 4/5"
                            },
                            {
                                "title": "ห้อง 4/6"
                            },
                            {
                                "title": "ห้อง 4/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.5",
                        "sub": [
                            {
                                "title": "ห้อง 5/1"
                            },
                            {
                                "title": "ห้อง 5/2"
                            },
                            {
                                "title": "ห้อง 5/3"
                            },
                            {
                                "title": "ห้อง 5/4"
                            },
                            {
                                "title": "ห้อง 5/5"
                            },
                            {
                                "title": "ห้อง 5/6"
                            },
                            {
                                "title": "ห้อง 5/7"
                            }
                        ]
                    },
                    {
                        "title": "ม.6",
                        "sub": [
                            {
                                "title": "ห้อง 6/1"
                            },
                            {
                                "title": "ห้อง 6/2"
                            },
                            {
                                "title": "ห้อง 6/3"
                            },
                            {
                                "title": "ห้อง 6/4"
                            },
                            {
                                "title": "ห้อง 6/5"
                            },
                            {
                                "title": "ห้อง 6/6"
                            },
                            {
                                "title": "ห้อง 6/7"
                            }
                        ]
                    }
                ]
            }
        ]

        your_result = []

        return HttpResponse(your_result, status=status.HTTP_200_OK)
        