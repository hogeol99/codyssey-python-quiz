import sys

import sys

class Quiz:
    # __init__은 퀴즈 객체가 처음 만들어질 때 속성(데이터)을 초기화하는 특별한 메서드입니다.
    def __init__(self, question, choices, answer):
        self.question = question  # 문제 내용 (문자열)
        self.choices = choices    # 선택지 4개 (리스트)
        self.answer = answer      # 정답 번호 1~4 (정수)

    # 퀴즈를 화면에 예쁘게 출력하는 메서드
    def display(self):
        print(f"\nQ. {self.question}")
        # enumerate를 사용하면 리스트의 항목과 인덱스(1부터 시작)를 함께 얻을 수 있습니다.
        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    # 사용자가 입력한 정답이 맞는지 확인하는 메서드
    def check_answer(self, user_answer):
        return self.answer == user_answer


# 기본 퀴즈 5개를 만들어 리스트로 반환하는 함수입니다.

def get_default_quizzes():
    return [
        Quiz("Python에서 화면에 데이터를 출력할 때 사용하는 함수는?", ["input()", "print()", "type()", "len()"], 2),
        Quiz("Python에서 리스트(List)를 만들 때 사용하는 괄호는?", ["{ }", "( )", "[ ]", "< >"], 3),
        Quiz("다음 중 Python의 반복문 키워드가 아닌 것은?", ["for", "while", "loop", "모두 반복문이다"], 3),
        Quiz("Python에서 한 줄 주석을 작성할 때 사용하는 기호는?", ["//", "/*", "<!--", "#"], 4),
        Quiz("참(True)과 거짓(False)을 나타내는 자료형의 이름은?", ["int", "str", "bool", "float"], 3)
    ]




def main():
    print("🎉 나만의 퀴즈 게임에 오신 것을 환영합니다! 🎉")
    
    quizzes = get_default_quizzes()
    best_score = 0  # [추가] 최고 점수를 기억할 변수입니다.
    
    while True:
        print("\n" + "="*20)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("="*20)
        
        try:
            choice_str = input("원하는 기능을 선택하세요 (1~5): ").strip()
            if not choice_str:
                print("⚠️ 입력값이 없습니다. 번호를 입력해 주세요.")
                continue
                
            choice = int(choice_str)
            if choice < 1 or choice > 5:
                print("⚠️ 1에서 5 사이의 숫자를 입력해 주세요.")
                continue
                
            if choice == 1:
                print("\n🚀 퀴즈 게임을 시작합니다!")
                score = 0 
                
                for quiz in quizzes:
                    quiz.display()
                    
                    while True:
                        try:
                            ans_str = input("정답을 입력하세요 (1~4): ").strip()
                            if not ans_str: continue
                            
                            ans = int(ans_str)
                            if ans < 1 or ans > 4:
                                print("⚠️ 1에서 4 사이의 숫자를 입력해 주세요.")
                                continue
                            break
                        except ValueError:
                            print("⚠️ 숫자만 입력해 주세요.")
                    
                    if quiz.check_answer(ans):
                        print("✅ 정답입니다!")
                        score += 1
                    else:
                        print(f"❌ 틀렸습니다. 정답은 {quiz.answer}번입니다.")
                
                print(f"\n🎉 게임 종료! 총 {len(quizzes)}문제 중 {score}문제를 맞히셨습니다.")
                
                # [추가] 방금 얻은 점수가 기존 최고 점수보다 높으면 갱신합니다!
                if score > best_score:
                    print(f"🌟 축하합니다! 최고 점수 갱신! (기존: {best_score} -> 현재: {score})")
                    best_score = score
            
            
            elif choice == 2:
                print("\n[ 퀴즈 추가 ]")
                new_q = input("문제를 입력하세요: ").strip()
                
                new_choices = []
                for i in range(1, 5):
                    c = input(f"{i}번 선택지를 입력하세요: ").strip()
                    new_choices.append(c) # 리스트에 선택지 추가
                
                while True:
                    try:
                        new_a = int(input("정답 번호를 입력하세요 (1~4): ").strip())
                        if 1 <= new_a <= 4:
                            break
                        print("⚠️ 1에서 4 사이의 숫자를 입력해 주세요.")
                    except ValueError:
                        print("⚠️ 숫자만 입력해 주세요.")
                
                # 새로운 Quiz 객체를 만들어서 quizzes 리스트에 추가(append)합니다.
                quizzes.append(Quiz(new_q, new_choices, new_a))
                print("✅ 새 퀴즈가 성공적으로 추가되었습니다!")

            elif choice == 3:
                print("\n[ 퀴즈 목록 ]")
                # 등록된 퀴즈들의 문제(question)만 순서대로 보여줍니다.
                for i, quiz in enumerate(quizzes, 1):
                    print(f"{i}. {quiz.question}")

            elif choice == 4:
                print(f"\n🏆 현재 최고 점수: {best_score}점")
            
            
            elif choice == 5:
                print("👋 게임을 종료합니다. 안녕히 가세요!")
                break
                
        except ValueError:
            print("⚠️ 숫자만 입력할 수 있습니다. 다시 입력해 주세요.")
        except (KeyboardInterrupt, EOFError):
            print("\n🚨 강제 종료 요청이 감지되었습니다.")
            sys.exit(0)

if __name__ == "__main__":
    main()