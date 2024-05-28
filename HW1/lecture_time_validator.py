# 수업 시간이 적절한 입력인지 확인할 때 사용하는 클래스
class LectureTimeValidator:
    # is_valid 함수는 'Wed#D1#Thu#E1'과 같은 문자열을 인자로 받아 적절한 수업 시간 입력인지 True와 False를 return한다.
    def is_valid(self, lecture_time: str):
        splitted_lecture_time = lecture_time.split('#')
        if len(splitted_lecture_time) % 2 == 1:
            return False
        for index, item in enumerate(splitted_lecture_time):
            if index % 2 == 0 and self.is_days(item) == False:
                return False
            elif index % 2 == 1:
                if len(item) != 2:
                    return False
                elif item[0].isalpha() == False or item[1].isdigit() == False:
                    return False
        return True
    # 인자로 들어온 days가 요일이 맞는지 확인하는 함수. 요일이 맞으면 True를, 아니면 False를 return한다.
    def is_days(self, days):
        all_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        return days in all_days