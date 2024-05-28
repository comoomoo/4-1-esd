import time
from course_list import CourseList
from course_admin_system import CourseAdminSystem
from course_registration_system import CourseRegistrationSystem
from shell_func import clear
#사용자명과 비밀번호를 확인하는 함수로

def is_student(username,password,student):
    for i in range(len(student[0])):
        if [student[0][i],student[1][i]] == [username,password]: #전달받은 사용자명과 비밀번호가 수강자 리스트에 있으면
            return student[2][i] #해당 수강자의 시스테메 인스턴스 반환
    return None #없을경우 None을 반환
    
# is_admin 함수는 username과 password를 인자로 전달받아 관리자인지 판단하는 함수이다.
# username이 root이고 password가 0000이면 관리자로 판단하도록 구현되어 있다.
def is_admin(username, password):
    if username == 'root' and password == '0000':
        return True
    return False

course_list = CourseList()

def main():
    student_info=[[],[],[]] #수강자의 정보를 저장할 리스트로 각각 사용자명, 비밀번호 수강자의 시스쳄 인스턴스를 리스트로 저장
    while(True): #프로그램을 무한 반복한다.
        print('''
프로그램 종료: 0
관리자 로그인: 1
수강자 로그인: 2
수강자 등록  : 3
              ''')
        choice = input('입력: ') #수행하길 원하는 기능에 대한 입력을 받는다
        if(choice=='0'): #0을 받으면 프로그램을 종료한다
            print('프로그램을 종료합니다.')
            break
        elif choice=='1': #1을 입력받으면 사용자명과 비밀번호를 입력받는다. 
            username = input('사용자 이름을 입력해주세요: ')
            password = input('비밀번호를 입력해주세요: ')
            if is_admin(username, password): #is_admin함수를 통하여 관리자인지 확인후에 
                course_admin_system = CourseAdminSystem(course_list) #관리자 시스템 생성후 관리자 시스템을 실행한다
               # clear() 
                course_admin_system.run() 
            else: #관리자에 해당하는 사용자 명이나 비밀번호가 아니라면 실행
                print('\n입력한 정보가 틀립니다.')
        elif choice=='2': #2를 입력받았다면
            username = input('사용자 이름을 입력해주세요: ')
            password = input('비밀번호를 입력해주세요: ')
            course_registration_system = is_student(username, password, student_info) #등록된 학생인지 확인하는 함수인 is_student를 실행한다.
            if course_registration_system != None: #반환된 값을 확인하여 None이 아니라면
                #clear()
                course_registration_system.run() #수강자 시스템을 실행한다.
            else:
                print('\n입력하신 정보를 찾을 수 없습니다.')
        elif choice=='3': #3을 입력받았을시
            username = input('사용자 이름을 입력해주세요: ')
            password = input('비밀번호를 입력해주세요: ')
            if username not in student_info[0] and username != "root": #사용자명이 중복이 아니면서 관리자 이름인 "root"가 아니라면 
                #수강자 정보 리스트에 사용자명, 비밀번호, 수강자 시스템을 추가
                student_info[0].append(username)
                student_info[1].append(password)
                course_registration_system = CourseRegistrationSystem(course_list)
                student_info[2].append(course_registration_system)
                print('\n등록이 완료되었습니다.')
            else:
                print('\n이미 존재하는 사용자 이름입니다.')
        else: #0,1,2,3 이외의 입력에 대한 처리
            print('\n잘못된 입력입니다.')
        time.sleep(2)
        #clear()

if __name__ == "__main__":
    main()