import numpy as np
import os
import time
from shell_func import clear

class CourseRegistrationSystem:
    # run 메서드는 CourseRegistrationSystem을 통해 수강자가 작업을 수행할 수 있도록 작업을 시작하는 메서드이다.
    # 해당 메서드를 실행함으로써 CLI 프로그램 사용자는 과목 조회, 신청, 취소 등을 할 수 있게 된다.
    def run(self):
        print('수강자로 로그인하셨습니다. 수행하고자 하는 작업을 입력해주세요.')
        self.login_time=time.time() #run실행시 로그인 시간을 초기화 시킨다.
        while(True): #종료를 선택하기 전까지 반복하며 기능을 수행한다.
            lecturer_input = input('0- 과목 조회, 1- 과목 신청, 2- 과목 취소, 3- 요일별 수업 스케줄 확인, 4-로그인 시간 갱신, 5- 작업 종료. 입력하기: ').strip()
            if lecturer_input == '0':
                self.course_list.show_courses()
            elif lecturer_input == '1':
                self.register_course()
                time.sleep(3)
                clear()
            elif lecturer_input == '2':
                self.cancel_course()
                time.sleep(3)
                clear()
            elif lecturer_input == '3':
                self.show_user_schedule()
            elif lecturer_input =='4':
                self.time_reset()
                time.sleep(3)
                clear()
            elif lecturer_input == '5':
                print('작업을 종료합니다')
                clear()
                break
            else:
                print('입력이 잘못되었습니다. 다시 입력해주세요')
                time.sleep(3)
                clear()
    # show_all_courses 메서드는 시스템에 등록된 모든 수업을 보여주는 메서드이다.
    def show_all_courses(self):
        print(self.course_list.items)
    # register_course 메서드는 수강자가 과목을 신청할 때 사용하는 메서드이다.
    def register_course(self):
        course_number = input('신청하려는 과목 번호를 입력해주세요: ')
        if self.course_list.has_course(course_number) == False:
            print('입력하신 과목은 존재하지 않습니다.')
            return
        course = self.course_list.find_course(course_number)
        if course is None:
            print('입력하신 과목은 존재하지 않습니다.')
            return
        course_name = course[1]
        course_is_required = course[2]
        course_credits = int(course[3])
        course_date = course[4]
        course_place = course[5]
        if (course_number in self.course_numbers_set) == True:
            print('이미 신청한 과목입니다')
            return
        if self.is_enrollment_allowed(course) == False:
            print('시간대가 겹쳐 과목을 신청할 수 없습니다.')
            return
        if self.all_credits + course_credits > 17:
            print('최대 신청 학점은 17학점으로 제한되어 과목을 신청할 수 없습니다.')
            return
        if (time.time() - self.login_time) > 60 * 5:
            print('로그인 시간으로 5분이 지나 과목을 수강할 수 없습니다.')
            return
        row = -1
        col = -1
        course_date_list = course_date.split('#')
        for index, value in enumerate(course_date_list):
            if index % 2 == 0:
                col = self.cols[value]
            else:
                row = self.rows[value[0]]
                row_cnt = int(value[1])
                for row_idx in range(row, row+row_cnt):
                    self.user_schedule[row_idx][col] = str(course_number)
        self.course_numbers_set.add(course_number)
        if course_is_required == 'Required':
            self.required_count += 1
        self.all_credits += course_credits
        print(f'{course_name} 과목이 수강되었습니다.', end=' ')
        if self.required_count < 4:
            print(f'앞으로 필수로 들어야 하는 전필 과목 수는 {4 - self.required_count}개입니다.')
        else:
            print(f'전필 과목은 최소 갯수인 4개를 충족하였습니다.')
    # is_enrollment_allowed 전달받은 시간에 다른 과목이 없는지 확인하고, 다른 과목이 있으면 신청할 수 없다고 판단하는 함수이다.
    # 겹치는 시간이 있으면 False를 return한다.
    # 겹치는 시간이 없으면 True를 return한다.
    def is_enrollment_allowed(self, course):
        course_date = course[4]
        col = -1
        row = -1
        course_date_list = course_date.split('#')
        for index, value in enumerate(course_date_list):
            if index % 2 == 0:
                col = self.cols[value]
            else:
                row = self.rows[value[0]]
                row_cnt = int(value[1])
                for row_idx in range(row, row+row_cnt):
                    if self.user_schedule[row_idx][col] != '':
                        return False
        return True
    # cancel_course는 과목 신청을 취소하는 메서드이다.
    # 과목이 존재하는지, 그리고 사용자가 해당 과목을 신청했는지 여부를 먼저 판단한다.
    def cancel_course(self):
        course_number = input('취소하려는 과목 번호를 입력해주세요: ')
        course = self.course_list.find_course(course_number)
        if course is None:
            print('입력하신 과목은 존재하지 않습니다.')
            return
        if (course_number in self.course_numbers_set) == False:
            print('취소하려는 과목은 신청하지 않은 과목입니다.')
            return
        if (time.time() - self.login_time) > 60 * 5:
            print('로그인 시간으로 5분이 지나 과목을 취소할 수 없습니다.')
            return
        _, course_name, course_is_required, course_credits, course_date, course_place = course
        course_credits = int(course_credits)
        row = -1
        col = -1
        course_date_list = course_date.split('#')
        for index, value in enumerate(course_date_list):
            if index % 2 == 0:
                col = self.cols[value]
            else:
                row = self.rows[value[0]]
                row_cnt = int(value[1])
                for row_idx in range(row, row+row_cnt):
                    self.user_schedule[row_idx][col] = ''
        self.course_numbers_set.discard(course_number)
        if course_is_required == 'Required':
            self.required_count -= 1
        self.all_credits -= course_credits
        print(f'{course_name} 과목이 취소되었습니다.')
    # show_user_schedule는 수강자의 시간표를 보여주는 메서드이다.
    def show_user_schedule(self):
        for i in range(1, 6):
            day_schedule = self.user_schedule.T[i]
            print(day_schedule[0], end=': ')
            for schedule_idx, course_number in enumerate(day_schedule):
                if schedule_idx == 0:
                    continue
                if course_number != '':
                    course = self.course_list.find_course(course_number)
                    if course is None:
                        continue
                    course_name = course[1]
                    course_date = course[4]
                    course_place = course[5]
                    print(f'{course_name} - {course_place} ({course_date})', end=' ')
            print()
    def time_reset(self): #로그인 시간을 갱신하는 함수
        self.login_time=time.time()
        print('시간이 갱신되었습니다')
        print()
    def __init__(self, course_list):
        self.course_list = course_list
        self.login_time=time.time()
        self.user_schedule = np.array([['', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
                                       ['A', '', '', '', '', ''],
                                       ['B', '', '', '', '', ''],
                                       ['C', '', '', '', '', ''],
                                       ['D', '', '', '', '', ''],
                                       ['E', '', '', '', '', ''],
                                       ['F', '', '', '', '', ''],
                                       ['G', '', '', '', '', ''],
                                       ['H', '', '', '', '', ''],
                                       ['I', '', '', '', '', ''],
                                       ['J', '', '', '', '', ''],], dtype=str)
        # 총 신청 학점을 담을 변수
        self.all_credits = 0
        # 신청한 전필 과목의 갯수를 담을 변수
        self.required_count = 0
        # 신청한 과목 번호들을 담을 set
        self.course_numbers_set = set([])
        self.cols = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5}
        self.rows = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}