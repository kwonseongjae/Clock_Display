import pygame
import sys
import os
from datetime import datetime, timedelta
import logging
import subprocess
import time
import ctypes
import ctypes.wintypes
from ctypes import windll, Structure, c_long, byref


# Pygame 초기화
pygame.init()

# 화면 크기 설정
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
pygame.display.set_caption("Clock with Color Buttons")

# 제목 설정
pygame.display.set_caption("Digital Clock")

# 폰트 로드 (7세그먼트 폰트 파일 경로를 지정)
font_path = "C:/Users/BT/ClockTest/DSEG7Classic-Bold.ttf"
font_size = 380
font = pygame.font.Font(font_path, font_size)

# 색상 설정
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
green = (0, 128, 0)

# 버튼 클래스 정의
class Button:
    def __init__(self, text, color, x, y, width, height):
        self.text = text
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 36)
        self.text_surf = self.font.render(text, True, white)
        self.text_rect = self.text_surf.get_rect(center=self.rect.center)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

# 버튼 생성
button1 = Button("B", black, 1200, 1000, 200, 50)
button2 = Button("Black & Yellow", yellow, 1450, 1000, 200, 50)
button3 = Button("Green & White", green, 1700, 1000, 200, 50)

#디스플레이 설정
class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

def get_display_rect(display_number):
    monitors = []

    def callback(hMonitor, hdcMonitor, lprcMonitor, dwData):
        r = lprcMonitor.contents
        monitors.append((r.left, r.top, r.right, r.bottom))
        return True

    MonitorEnumProc = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_ulong, ctypes.c_ulong, ctypes.POINTER(ctypes.wintypes.RECT), ctypes.c_double)
    windll.user32.EnumDisplayMonitors(None, None, MonitorEnumProc(callback), 0)

    if display_number >= len(monitors):
        raise ValueError(f"Invalid display number: {display_number}")

    return monitors[display_number]

def set_display_mode(display_number):
    # Get the coordinates of the specified display
    left, top, right, bottom = get_display_rect(display_number)
    width = right - left
    height = bottom - top

    # Create the Pygame window
    screen = pygame.display.set_mode((1920, 1080), pygame.NOFRAME)
    pygame.display.set_caption("Clock with Color Buttons")

    # Move the window to the specified display
    hwnd = pygame.display.get_wm_info()['window']
    windll.user32.SetWindowPos(hwnd, None, left, top, width, height, 0x0001)

    return screen


'''
def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
'''

def draw_text(screen, text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)




def log_remover(log_root_path):
    # 디렉토리 내의 모든 파일 목록 가져오기
    files = os.listdir(log_root_path)
    sub_directories = sorted([item for item in files if os.path.isdir(os.path.join(log_root_path, item))
                              and len(item) == 6  # 이름이 6글자인지 확인
                              and item.isdigit()])
    # print(sub_directories)
    if len(sub_directories) > 12:
        for i in range(len(sub_directories) - 12):
            try:
                os.system(f'rd /s /q "{log_root_path}\\{sub_directories[i]}"')
            except:
                print('directory remove fail...')
    else:
        pass


def start_log():
    my_directory = "C:/Users/BT/ClockTest"
    dir_name = datetime.now().strftime('%Y%m')
    log_root_path = my_directory + "\save_log"
    log_folder_path = log_root_path + "\\" + dir_name
    try:
        os.makedirs(log_folder_path, exist_ok=True)
        print(f"make directory : {log_folder_path}")
    except FileExistsError:
        print(f"already exist : {log_folder_path}")
    log_remover(log_root_path)
    current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log_filename = f'{log_folder_path}\\{current_time}.log'
    print('log_filename',log_filename)
    try:
        # 로그 파일을 쓰기 모드로 엽니다. 파일이 없으면 새로 생성됩니다.
        with open(log_filename, "w") as log_file:
            pass  # 아무 내용도 작성하지 않습니다.
        print(f"log 파일 '{log_filename}'가 생성되었습니다.")
    except Exception as e:
        print(f"log 파일 생성 중 오류가 발생했습니다: {str(e)}")
    logging.basicConfig(filename=log_filename, encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')


start_log()

def create_folder(folder_path):
    try:
        os.makedirs(folder_path, exist_ok=True)
        print(f"make directory : {folder_path}")
    except FileExistsError:
        print(f"already exist : {folder_path}")
        pass

def create_text_file(content, folder_path):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}.txt"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as file:
        file.write(content)


def check_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return True
    return False


def run_process(process_path):
    try:
        subprocess.Popen(["start", "", process_path], shell=True)
    except Exception as e:
        print(f"프로세스 실행 중 오류가 발생했습니다: {e}")


def watchdog(process_name, check_interval):
    script_directory = "C:/Users/BT/ClockTest"
    folder_path = script_directory + "\log" # 와치독 로그 저장될 디렉토리
    try:
        while True:
            if not check_process_running(process_name):
                try:
                    os.makedirs(folder_path, exist_ok=True)
                except FileExistsError:
                    pass
                file_content = f"프로세스 '{process_name}'이(가) 실행되지 않았습니다. 재시작 합니다."
                print(file_content)
                create_text_file(file_content, folder_path)

                source_path = "C:/Users/BT/ClockTest"
                program_path = source_path + "/watchdog.py"
                #program_path = script_directory + "/watchdog.py"  # 실행하려는 프로그램의 경로 정확히 입력
                run_process(program_path)
            else:
                print(f"정상 작동중...")
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("스크립트를 종료합니다.")


def run():
    process_name = "py.exe"  # 실행 될 프로세스
    check_interval = 5  # 초 단위로 설정 (예: 5초)
    watchdog(process_name, check_interval)



# 현재 배경색 및 텍스트 색상 설정
bg_color = black
text_color = white


def main(display_number):
   
    global bg_color, text_color
    clock = pygame.time.Clock()

    screen = set_display_mode(display_number)
                              
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()


                    # 버튼 클릭 이벤트 처리
                if button1.is_clicked(event):
                    bg_color = black
                    text_color = white
                    
                elif button2.is_clicked(event):
                    bg_color = black
                    text_color = yellow
                    
                elif button3.is_clicked(event):
                    bg_color = green
                    text_color = white

            # 화면 채우기
            screen.fill(bg_color)

            # 현재 시간 가져오기
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            # 텍스트 그리기
            draw_text(screen, current_time, font, text_color , 860, 540)

            # 버튼 그리기
            button1.draw(screen)
            button2.draw(screen)
            button3.draw(screen)

            
            # 화면 업데이트
            pygame.display.flip()

            # 초당 1 프레임
            clock.tick(1)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    display_number = 0 # 첫 번째 디스플레이는 0, 두 번째 디스플레이는 1, ...
    main(display_number)
    run()
