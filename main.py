import json
import os
import sys

# 1. 개별 퀴즈를 담당하는 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

# 2. 게임 전체를 관리하는 클래스 (요구사항 반영!)
class QuizGame:
    def __init__(self):
        # 속성: 퀴즈 목록, 최고 점수
        self.quizzes = []
        self.best_score = 0
        self.load_data() # 게임이 생성될 때 자동으로 데이터를 불러옵니다.

    def get_default_quizzes(self):
        return [
            Quiz("파이썬의 창시자는?", ["1. 귀도 반 로섬", "2. 제임스 고슬링", "3. 데니스 리치", "4. 리누스 토발즈"], 1),
            Quiz("파이썬의 리스트 추가 메서드는?", ["1. add()", "2. append()", "3. insert()", "4. push()"], 2),
            Quiz("파이썬에서 함수를 정의할 때 쓰는 키워드는?", ["1. func", "2. def", "3. function", "4. define"], 2),
            Quiz("파이썬의 딕셔너리는 어떤 구조인가요?", ["1. LIFO", "2. FIFO", "3. Key-Value", "4. Index-Value"], 3),
            Quiz("파이썬에서 문자열 길이를 구하는 함수는?", ["1. length()", "2. size()", "3. len()", "4. count()"], 3)
        ]

    # 메서드: 파일 불러오기
    def load_data(self):
        if not os.path.exists("state.json"):
            self.quizzes = self.get_default_quizzes()
            return
            
        try:
            with open("state.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                
            self.best_score = data.get("best_score", 0)
            quiz_list = data.get("quizzes", [])
            
            for q in quiz_list:
                self.quizzes.append(Quiz(q["question"], q["choices"], q["answer"]))
                
            if len(self.quizzes) == 0:
                self.quizzes = self.get_default_quizzes()
                
        except json.JSONDecodeError:
            print("\n⚠️ [경고] 데이터 파일이 손상되었습니다. 기본 퀴즈로 초기화합니다.\n")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
        except Exception as e:
            print(f"\n⚠️ [경고] 알 수 없는 오류 발생: {e}. 기본 퀴즈로 초기화합니다.\n")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0

    # 메서드: 파일 저장하기
    def save_data(self):
        data = {
            "best_score": self.best_score,
            "quizzes": [q.to_dict() for q in self.quizzes]
        }
        with open("state.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # 메서드: 퀴즈 풀기
    def play_quiz(self):
        print("\n--- 🎮 퀴즈 풀기 ---")
        score = 0
        for i, quiz in enumerate(self.quizzes):
            print(f"\n문제 {i+1}. {quiz.question}")
            for choice in quiz.choices:
                print(choice)
                
            while True:
                # 1. 입력 앞뒤 공백 제거 (.strip() 사용)
                raw_input = input("정답을 입력하세요 (번호): ").strip()
                
                # 2. 빈 입력(그냥 Enter)인 경우 처리
                if not raw_input: # 또는 if raw_input == "":
                    print("⚠️ 아무것도 입력하지 않으셨습니다. 정답 번호를 입력해주세요.")
                    continue # 다시 입력받도록 while문 처음으로 돌아감
                    
                # 3. 숫자 변환 시도 및 실패(abc 등) 처리
                try:
                    user_answer = int(raw_input)
                except ValueError:
                    print("⚠️ 숫자만 입력해주세요! (예: 1)")
                    continue
                    
                # 4. 허용 범위 밖 숫자(예: 0, 9) 입력 시 처리
                
                if user_answer < 1 or user_answer > 4:
                    print(f"⚠️ 보기의 범위(1~4) 안에서 입력해주세요.")
                    continue
                    
                # 모든 검증을 무사히 통과했다면 while 반복문 탈출!
                break
                    
            if user_answer == quiz.answer:
                print("✅ 정답입니다!")
                score += 10
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer}번입니다.")
                
        print(f"\n게임 종료! 당신의 점수는 {score}점 입니다.")
        
        if score > self.best_score:
            print(f"🎉 최고 점수 갱신! (기존: {self.best_score} -> 현재: {score})")
            self.best_score = score
            self.save_data()

        # 메서드: 퀴즈 추가
    def add_quiz(self):
        print("\n--- ➕ 퀴즈 추가 ---")
        
        # 1. 문제 입력 (빈칸 방지)
        while True:
            question = input("문제를 입력하세요: ").strip() # .strip()으로 양쪽 공백 제거
            if question: # 공백 제거 후 내용이 있으면(True) 통과
                break
            print("⚠️ 빈칸은 입력할 수 없습니다. 다시 입력해주세요.")

        # 2. 보기 입력 (빈칸 방지)
        choices = []
        for i in range(1, 5):
            while True:
                choice = input(f"{i}번 보기를 입력하세요: ").strip()
                if choice:
                    choices.append(f"{i}. {choice}")
                    break
                print("⚠️ 빈칸은 입력할 수 없습니다. 다시 입력해주세요.")
            
        # 3. 정답 입력 (빈칸 및 예외 처리)
        while True:
            answer_input = input("정답 번호를 입력하세요 (1~4): ").strip()
            if not answer_input:
                print("⚠️ 빈칸은 입력할 수 없습니다.")
                continue
                
            try:
                answer = int(answer_input)
                if 1 <= answer <= 4:
                    break
                else:
                    print("⚠️ 1에서 4 사이의 숫자를 입력해주세요.")
            except ValueError:
                print("⚠️ 숫자만 입력해주세요!")
                
        self.quizzes.append(Quiz(question, choices, answer))
        self.save_data()
        print("✅ 퀴즈가 성공적으로 추가되었습니다!")

    # 메서드: 목록 보기
    def show_quiz_list(self):
        print("\n--- 📋 퀴즈 목록 ---")
        for i, quiz in enumerate(self.quizzes):
            print(f"{i+1}. {quiz.question}")
        print("--------------------")

    # 메서드: 점수 확인
    def show_best_score(self):
        print("\n--- 🏆 최고 점수 확인 ---")
        if self.best_score == 0:
            print("아직 퀴즈를 풀지 않았거나 획득한 점수가 없습니다.")
        else:
            print(f"현재 최고 점수는 {self.best_score}점 입니다! 🎉")
        print("------------------------\n")

        # 메서드: 메뉴 표시 및 게임 실행
    def run(self):
        while True:
            print("\n=== 🧠 파이썬 퀴즈 게임 ===")
            print("1. 퀴즈 풀기")
            print("2. 퀴즈 추가")
            print("3. 퀴즈 목록 보기")
            print("4. 최고 점수 확인")
            print("5. 종료")
            print("===========================")
            
            menu_input = input("메뉴를 선택하세요: ").strip()
            
            # [추가] 빈칸 입력 방지
            if not menu_input:
                print("⚠️ 빈칸은 입력할 수 없습니다. 메뉴 번호를 입력해주세요.")
                continue
                
            try:
                choice = int(menu_input)
            except ValueError:
                print("⚠️ 숫자로만 입력해주세요!")
                continue
                
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quiz_list()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                print("게임을 종료합니다. 안녕히 가세요! 👋")
                break
            else:
                print("⚠️ 1~5 사이의 번호를 선택해주세요.")

if __name__ == "__main__":
    try:
        game = QuizGame() # 게임 객체 생성
        game.run()        # 게임 실행
        
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 또는 입력 스트림 강제 종료 시 이곳이 실행됩니다.
        print("\n\n⚠️ [안내] 프로그램이 강제 중단되었습니다.")
        print("현재까지의 데이터를 안전하게 저장하고 프로그램을 종료합니다...")
        
       
        game.save_data() 
        
        sys.exit(0) # 에러 없이 안전하게 프로그램 종료