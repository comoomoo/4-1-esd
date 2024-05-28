import numpy as np
import os
import time
from lecture_time_validator import LectureTimeValidator
from shell_func import clear

basics_file_path = os.path.join(os.path.dirname(__file__), 'basics.txt')
class CourseList:
    # load_courses 메서드는 basics.txt 파일의 내용을 읽어와 self.items에 ndarray 타입으로 값을 지정해주는 메서드이다.
    # basics.txt 파일이 경로에 존재하지 않을 경우 과목을 빈 배열로 초기화한다.
    def load_courses(self):
        if os.path.exists(basics_file_path):
            self.items = np.loadtxt(basics_file_path, dtype=str, comments=None)
        else:
            print('과목 데이터베이스 파일이 없습니다. 과목을 빈 목록으로 초기화합니다.')
            self.items = np.array([[]], dtype=str)
            print(len(self.items))
    # save_courses 메서드는 basics.txt 파일에 self.items의 내용을 저장해주는 메서드이다.
    def save_courses(self):
        np.savetxt(basics_file_path, self.items, fmt='%s', delimiter='	', comments='')
    # append_course 메서드는 새로운 과목을 self.items 마지막에 추가해주는 메서드이다.
    def append_course(self, course: np.ndarray):
        # 과목이 빈 목록일 경우
        if len(self.items[0]) == 0:
            self.items = course
            return
        self.items = np.append(self.items, course, axis=0)
    # find_course_index 메서드는 self.items에서 과목 번호가 일치하는 과목이 있는지 찾는 메서드이다.
    # 일치하는 과목이 있으면 해당 과목의 인덱스를 return한다.
    # 일치하는 과목이 없으면 None을 return한다.
    def find_course_index(self, course_number):
        if len(self.items[0]) == 0:
            return None
        course_index = np.where(self.items.T[0] == str(course_number))[0]
        if len(course_index) == 0:
            return None
        else:
            return course_index[0]
    # find_course 메서드는 self.items에서 과목 번호가 일치하는 과목이 있는지 찾는 메서드이다.
    # 일치하는 과목이 있으면 해당 과목을 return한다.
    # 일치하는 과목이 없으면 None을 return한다.
    def find_course(self, course_number):
        course_index = self.find_course_index(course_number)
        if course_index == None:
            return None
        return self.items[course_index]
        
    # has_course 메서드는 self.items에 과목 번호와 일치하는 과목이 있는지 찾는 메서드이다.
    # 일치하는 과목이 있으면 True를, 없으면 False를 return한다.
    def has_course(self, course_number):
        return self.find_course_index(course_number) != None
    # delete_course 메서드는 self.items에서 과목 번호와 일치하는 과목을 삭제하는 메서드이다.
    # 일치하는 과목이 없다면 삭제할 수 없음을 출력하고 동작을 마친다.
    # 일치하는 과목이 있다면 일치하는 과목을 삭제하고 삭제하였음을 출력한다.
    def delete_course(self, course_number):
        delete_index = self.find_course_index(course_number)
        if delete_index != None:
            self.items = np.delete(self.items, delete_index, axis=0)
            print(f"과목 번호 {course_number}을(를) 삭제하였습니다.")
        else:
            print(f"과목 번호 {course_number}을(를) 찾을 수 없습니다.")
        time.sleep(3)
        clear()
    # edit_course 메서드는 course_number를 인자로 전달받아 과목 번호와 일치하는 과목을 수정하는 메서드이다.
    # 해당 메서드에서는 사용자에게 입력을 받아 과목의 정보를 수정한다.
    def edit_course(self, course_number):
        edit_index = self.find_course_index(course_number)
        if edit_index != None:
            while(True):
                user_input = input('변경하고자 하는 과목 정보를 선택하여 주십시오.\n0- 과목 번호, 1- 과목명, 2- 전필여부, 3- 학점, 4- 수업 시간, 5- 수업 장소, 6- 작업 종료. 입력: ').strip()
                if user_input == '0':
                    while(True):
                        course_number = input('과목 번호를 입력해주세요: ')
                        if course_number.isdigit() == False:
                            print("과목 번호는 숫자만 입력해야 합니다. 다시 입력해주세요.")
                            continue
                        self.items[edit_index][0] = course_number
                        break
                elif user_input == '1':
                    course_name = input('과목명을 입력해주세요: ')
                    self.items[edit_index][1] = course_name
                elif user_input == '2':
                    while(True):
                        is_required = input('전필 여부를 입력해주세요 (Elective, Required): ')
                        if is_required != 'Elective' and is_required != 'Required':
                            print('전필 여부는 Elective나 Required로 입력해야 합니다. 다시 입력해주세요.')
                            continue
                        self.items[edit_index][2] = is_required
                        break
                elif user_input == '3':
                    while(True):
                        credits = input('학점을 입력해주세요: ')
                        if credits.isdigit() == False:
                            print("학점은 숫자만 입력해야 합니다. 다시 입력해주세요.")
                            continue
                        self.items[edit_index][3] = credits
                        break
                elif user_input == '4':
                    validator = LectureTimeValidator()
                    while(True):
                        lecture_time = input('수업 시간을 입력해주세요: ')
                        if validator.is_valid(lecture_time) == False:
                            print("수업 시간은 다음과 같은 포맷으로 입력해야 합니다. 예) Mon#D1#Wed#D1\n다시 입력해주세요.")
                            continue
                        self.items[edit_index][4] = lecture_time
                        break
                elif user_input == '5':
                    while(True):
                        lecture_place = input('수업 장소를 입력해주세요: ')
                        classroom_number = lecture_place.split('#')
                        if len(classroom_number) != 2 or (len(classroom_number) == 2 and classroom_number[1].isdigit() == False):
                            print("수업 장소는 다음과 같은 포맷으로 입력해야 합니다. 예) Woncheon#538\n다시 입력해주세요.")
                            continue
                        self.items[edit_index][5] = lecture_place
                        break
                elif user_input == '6':
                    return
                else:
                    print('입력이 잘못되었습니다. 다시 입력해주세요')
                    continue
                print(f"변경된 정보: {self.items[edit_index]}")
        else:
            print(f"과목 번호 {course_number}을(를) 찾을 수 없습니다.")
        time.sleep(3)
        clear()
    # show_courses 메서드는 등록된 과목들을 보여주는 메서드이다.
    def show_courses(self):
        print(self.items)
    def __init__(self):
        self.items = np.array([], dtype=str)
        self.load_courses()
