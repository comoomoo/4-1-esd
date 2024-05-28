import numpy as np
import os
import time
from lecture_time_validator import LectureTimeValidator
from shell_func import clear

class CourseAdminSystem:
    # insert_courses 메서드는 특정 과목들을 course_list에 추가하는 메서드이다.
    # 만약 중복되는 과목번호를 가진 과목이 있다면 해당 과목은 추가하지 않는다.
    def insert_courses(self):
        print('0 : 추가할 과목 불러오기, 1 : 직접 정보 입력')
        input_value = input('입력: ')
        if input_value == '0':
            courses = np.array([['120', 'AutomaticControl', 'Elective', '3', 'Mon#B1#Thu#B1', 'Woncheon#539'],
                                ['130', 'Multimedia', 'Elective', '3', 'Wed#B1#Fri#B1', 'Woncheon#540'],
                                ['140', 'ComputerArchitecture', 'Elective', '3', 'Mon#E1#Thu#E1', 'Woncheon#510'],
                                ['150', 'Probability', 'Elective', '3', 'Mon#D1#Wed#D1', 'Woncheon#228'],
                                ['160', 'ElectronicCircuit1', 'Required', '3', 'Wed#B1#Fri#B1', 'Woncheon#538']])
            for course in courses:
                course_number = course[0]
                if self.course_list.has_course(course_number) == False:
                    self.course_list.append_course(np.array([course]))
                    print('과목이 추가되었습니다.')
                else:
                    print('과목번호(',course_number,') 는 이미 개설된 과목입니다')
        elif input_value == '1':
            course=list(input('과목번호 과목명 전필여부 학점 시간 장소\n').split())
            if len(course)!=6: #과목정보 입력 형식과 맞지 않을 경우
                print('잘못된 입력입니다')
                return
            if self.course_list.has_course(course[0]) == True: #과목번호의 중복을 확인
                    print('이미 존재하는 과목번호 입니다')
                    return
            if course[0].isdigit() == False: #과목번호가 숫자인지 확인
                print('과목 번호 입력이 숫자가 아닙니다. 과목 번호는 숫자로 입력해야 합니다.')
                return
            if (course[2]=='Elective' or course[2]=='Required') == False: #전필여부가 형식에 맞게 입력되었는지 확인
                print('전필여부의 입력이 잘못되었습니다.')
                return
            if course[3].isdigit() == False: #학점이 숫자가 입력이 되었는지 확인
                print('학점 입력이 숫자가 아닙니다. 학점은 숫자로 입력해야 합니다.')
                return
            validator = LectureTimeValidator()
            if validator.is_valid(course[4]) == False: #수업시간의 입력이 형식에 맞는지 확인
                print("수업 시간은 다음과 같은 포맷으로 입력해야 합니다. 예) Mon#D1#Wed#D1\n")
                return
            classroom_number = course[5].split('#')
            if len(classroom_number) != 2 or (len(classroom_number) == 2 and classroom_number[1].isdigit() == False): #수업장소가 형식에 맞는 입력인지 확인
                print("수업 장소는 다음과 같은 포맷으로 입력해야 합니다. 예) Woncheon#538\n")
                return
            self.course_list.append_course(np.array([course])) #모든 조건 만족시 과목 추가
            print('과목이 추가되었습니다')
        else:
            print('잘못된 입력입니다')
    # delete_course 메서드는 사용자에게 삭제하려는 과목 번호를 입력받아 과목을 삭제하는 메서드이다.
    def delete_course(self):
        course_number = input('삭제하려는 과목번호를 입력해주세요: ')
        self.course_list.delete_course(course_number)
    # edit_course 메서드는 사용자에게 변경하려는 과목 번호를 입력받아 과목을 변경하는 메서드이다.
    def edit_course(self):
        course_number = input('변경하려는 과목번호를 입력해주세요: ')
        self.course_list.edit_course(course_number)
    # run 메서드는 CourseAdminSystem을 통해 관리자가 작업을 수행할 수 있도록 작업을 시작하는 메서드이다.
    # 해당 메서드를 실행함으로써 CLI 프로그램 사용자는 과목 추가, 삭제, 정보 변경을 할 수 있게 된다.
    def run(self):
        print('관리자로 로그인하셨습니다. 수행하고자 하는 작업을 입력해주세요.')
        while(True):
            admin_input = input('0- 과목 추가, 1- 과목 삭제, 2- 과목 정보 변경, 3- 개설 과목 조회, 4- 작업 종료. 입력하기: ').strip()
            if admin_input == '0':
                self.insert_courses()
                time.sleep(3)
                clear()
                #course_list.save_courses()
            elif admin_input == '1':
                self.delete_course()
                time.sleep(3)
                clear()
                #course_list.save_courses()
            elif admin_input == '2':
                self.edit_course()
                time.sleep(3)
                clear()
                #course_list.save_courses()
            elif admin_input == '3':
                self.course_list.show_courses()
            elif admin_input == '4':
                clear()
                break
            else:
                print('입력이 잘못되었습니다. 다시 입력해주세요')
    def __init__(self, course_list):
        self.course_list = course_list