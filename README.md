# Clock_Display

## 프로그램 설명
## Window 시간을 동기화 후, 화면에 출력해주는 간단한 프로그램
### 1. window app
### 2. CLOCK (font : fixed seven segment)
### 3. Full HD(1920*1080)
### 4. 부팅시 자동실행
### 5. 윈도우 시계와 동기화
### 6. 시 분 초 (연, 월x => 추가가능)
### 7. log기록
### 8. main program 감시하는 watchdog프로그램
### 9. watchdog 실행 시, main program 감시, 실행되지 않았으면(5초마다) 오류 메세지 발생 및 log기록 후, main program 실행
### 10. main program 실행 시, watchdog 감시, 실행되지 않았으면(5초마다) 오류 메세지 발생 및 log기록 후, watchdog 실행
### 11. Display 1에 실행화면 띄울 지 ,Display 2에 실행화면 띄울지 선택
### 12. 오른쪽 하단 버튼 3개 구현
### 13. 검정바탕에 흰색 숫자, 검정바탕에 노란색 숫자, 초록바탕에 흰색 숫자 선택가능

<img width="80%" src="https://github.com/kwonseongjae/Clock_Display/assets/18046794/4effb57f-aed7-4f9e-ba9e-8d683c6abe0c"/>

#### 프로그램 실행순서
#### 1. git clone
#### 2. 경로는 C드라이브 최상단 고정, C:/Clock_Display
#### 3. exe파일로 실행되게끔 설정해놨지만, 용량문제로 py파일을 직접 exe파일로 변환해서 사용해야합니다
#### 4. 자신이 디스플레이를 모니터1에 띄울 시 C:/ClockDisplay에 main2,sub1폴더 생성 , 모니터2에 띄울건지 main1,sub1폴더 생성
#### 5. win + r cmd창 실행 후 cd C:/Clock_Display 명령어 실행
#### 6-1. 디스플레이1에 띄울 시 , pyinstaller --onefile --noconsole --add-data "C:/Clock_Display/DSEG7Classic-Bold.ttf;." clock_reverse.py 실행 후 clock_reverse.exe파일 생성, 
####    pyinstaller --onefile --noconsole --add-data "C:/Clock_Display/DSEG7Classic-Bold.ttf;." watchdog_reverse.py 실행 후 watchdog_reverse.exe 파일 생성
####    dist폴더 안에 2개의 exe파일을 main2,sub1폴더 안으로 복사/붙여넣기 후, watchdog_reverse.exe 실행
#### 6-2.  디스플레이2에 띄울 시 , pyinstaller --onefile --noconsole --add-data "C:/Clock_Display/DSEG7Classic-Bold.ttf;." clock.py 실행 후 clock.exe파일 생성, 
####    pyinstaller --onefile --noconsole --add-data "C:/Clock_Display/DSEG7Classic-Bold.ttf;." watchdog.py 실행 후 watchdog.exe 파일 생성
####    dist폴더 안에 2개의 exe파일을 main1,sub2폴더 안으로 복사/붙여넣기 후, watchdog.exe 실행

### clock.exe와 clock_reverse.exe 실행 시 종료하고 싶으면 esc로 종료 가능, 하지만 watchdog프로그램이 실행 중이기 때문에 5초 후 다시 켜집니다.
### watchdog.exe와 clock.exe 프로세스 2개를 종료해야지만 프로그램 종료됨.
