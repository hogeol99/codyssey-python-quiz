import sys
import json  # [추가] JSON 파일을 다루기 위한 모듈
import os    # [추가] 파일이 존재하는지 확인하기 위한 모듈

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
    
     # 퀴즈 객체를 파일에 저장하기 쉬운 '딕셔너리' 형태로 변환하는 메서드입니다.
    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# 기본 퀴즈 5개를 만들어 리스트로 반환하는 함수입니다.

def get_default_quizzes():
    return [
        Quiz("Python에서 화면에 데이터를 출력할 때 사용하는 함수는?", ["input()", "print()", "type()", "len()"], 2),
        Quiz("Python에서 리스트(List)를 만들 때 사용하는 괄호는?", ["{ }", "( )", "[ ]", "< >"], 3),
        Quiz("다음 중 Python의 반복문 키워드가 아닌 것은?", ["for", "while", "loop", "모두 반복문이다"], 3),
        Quiz("Python에서 한 줄 주석을 작성할 때 사용하는 기호는?", ["//", "/*", "<!--", "#"], 4),
        Quiz("참(True)과 거짓(False)을 나타내는 자료형의 이름은?", ["int", "str", "bool", "float"], 3)
    ]

# 💾 데이터를 파일로 저장하는 함수
def save_data(quizzes, best_score):
    quiz_list = []
    for quiz in quizzes:
        quiz_list.append(quiz.to_dict()) # 퀴즈들을 딕셔너리로 변환해서 리스트에 담음
        
    data = {
        "best_score": best_score,
        "quizzes": quiz_list
    }
    
    # state.json 파일에 쓰기 모드(w)로 저장합니다.
    with open("state.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 📂 파일에서 데이터를 불러오는 함수
def load_data():
    # 파일이 없으면 기본 퀴즈와 0점을 반환합니다.
    if not os.path.exists("state.json"):
        return get_default_quizzes(), 0
        
    try:
        # 2. 파일이 있으면 읽기 모드로 엽니다.
        with open("state.json", "r", encoding="utf-8") as f:
            data = json.load(f) # 여기서 파일이 손상되었다면 에러가 발생합니다!
            
        best_score = data.get("best_score", 0)
        quiz_list = data.get("quizzes", [])
        
        quizzes = []
        for q in quiz_list:
            quizzes.append(Quiz(q["question"], q["choices"], q["answer"]))
            
        if len(quizzes) == 0:
            quizzes = get_default_quizzes()
            
        return quizzes, best_score
        
    # 3. [추가] JSON 파일 형식이 망가졌을 때(손상되었을 때) 처리
    except json.JSONDecodeError:
        print("\n⚠️ [경고] 저장된 데이터 파일(state.json)이 손상되었습니다.")
        print("🔄 기본 퀴즈 데이터로 초기화하여 게임을 시작합니다.\n")
        return get_default_quizzes(), 0
        
    # 4. [추가] 그 외 예상치 못한 에러가 발생했을 때 처리
    except Exception as e:
        print(f"\n⚠️ [경고] 데이터를 불러오는 중 알 수 없는 오류가 발생했습니다: {e}")
        print("🔄 기본 퀴즈 데이터로 초기화하여 게임을 시작합니다.\n")
        return get_default_quizzes(), 0


def main():
    print("🎉 나만의 퀴즈 게임에 오신 것을 환영합니다! 🎉")
    
    # 1️⃣ [수정] 시작할 때 파일에서 데이터를 불러옵니다.
    quizzes, best_score = load_data()
    
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
                    # 2️⃣ [추가] 최고 점수가 갱신되었으니 파일에 저장합니다.
                    save_data(quizzes, best_score)
            
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
                # 3️⃣ [추가] 새 퀴즈가 추가되었으니 파일에 저장합니다.
                save_data(quizzes, best_score)

            elif choice == 3:
                print("\n[ 퀴즈 목록 ]")
                # 등록된 퀴즈들의 문제(question)만 순서대로 보여줍니다.
                for i, quiz in enumerate(quizzes, 1):
                    print(f"{i}. {quiz.question}")

            elif choice == 4:
                print("\n--- 🏆 최고 점수 확인 ---")
                # [추가] 아직 퀴즈를 풀지 않았거나 점수가 0점인 경우를 처리합니다.
                if best_score == 0:
                    print("아직 퀴즈를 풀지 않았거나 획득한 점수가 없습니다.")
                    print("1번 메뉴를 선택해 퀴즈에 먼저 도전해 보세요! 💪")
                else:
                    print(f"현재 최고 점수는 {best_score}점 입니다! 🎉")
                print("------------------------\n")
                
            
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