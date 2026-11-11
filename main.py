import sys

def main():
    print("🎉 나만의 퀴즈 게임에 오신 것을 환영합니다! 🎉")
    
    # 사용자가 종료를 선택할 때까지 계속 반복합니다.
    while True:
        print("\n" + "="*20)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("="*20)
        
        try:
            # input()으로 입력을 받고, strip()으로 양옆의 공백(띄어쓰기)을 제거합니다.
            choice_str = input("원하는 기능을 선택하세요 (1~5): ").strip()
            
            # 1. 빈 입력(그냥 Enter만 친 경우) 처리
            if not choice_str:
                print("⚠️ 입력값이 없습니다. 번호를 입력해 주세요.")
                continue # 아래 코드를 실행하지 않고 다시 while문 처음(메뉴 출력)으로 돌아감
                
            # 2. 문자를 입력했는지 확인 (숫자로 변환 시도)
            # 만약 "안녕" 같은 문자가 들어오면 여기서 ValueError가 발생하여 except 구문으로 이동합니다.
            choice = int(choice_str)
            
            # 3. 허용 범위(1~5) 밖의 숫자 처리
            if choice < 1 or choice > 5:
                print("⚠️ 1에서 5 사이의 숫자를 입력해 주세요.")
                continue
                
            # 정상적인 입력이 들어왔을 때의 기능 분기
            if choice == 1:
                print("👉 퀴즈 풀기 기능을 실행합니다. (구현 예정)")
            elif choice == 2:
                print("👉 퀴즈 추가 기능을 실행합니다. (구현 예정)")
            elif choice == 3:
                print("👉 퀴즈 목록 기능을 실행합니다. (구현 예정)")
            elif choice == 4:
                print("👉 최고 점수 확인 기능을 실행합니다. (구현 예정)")
            elif choice == 5:
                print("👋 게임을 종료합니다. 안녕히 가세요!")
                break # while 무한 루프를 탈출하여 프로그램 종료
                
        except ValueError:
            print("⚠️ 숫자만 입력할 수 있습니다. 다시 입력해 주세요.")
            
        # 사용자가 강제로 Ctrl+C를 누르거나(KeyboardInterrupt) 터미널 입력을 끊었을 때(EOFError)
        except (KeyboardInterrupt, EOFError):
            print("\n🚨 강제 종료 요청이 감지되었습니다.")
            print("데이터를 안전하게 저장하고 프로그램을 종료합니다. (저장 기능 구현 예정)")
            sys.exit(0) # 프로그램 안전 종료

if __name__ == "__main__":
    main()