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
import win32api
import win32gui
import win32con

# Pygame 초기화
pygame.init()

# 화면 크기 설정
#screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
#pygame.display.set_caption("Clock with Color Buttons")

#화면 크기 auto 설정
def get_screen_resolution():
    u32 = ctypes.windll.user32
    return u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)

resolution = get_screen_resolution()
screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)

# 제목 설정
pygame.display.set_caption("Digital Clock")

'''
# 폰트 로드 (7세그먼트 폰트 파일 경로를 지정)
font_path = "C:/Clock_Display/DSEG7Classic-Bold.ttf"
font_size = 350
font = pygame.font.Font(font_path, font_size)
'''



# 해상도에 맞게 폰트 크기를 설정 (화면 높이의 20%)
def load_font(resolution):
    #width, height = resolution
    #font_size = int(width * 0.15)
    screen_width = resolution[0]
    font_size = int(screen_width * 0.185)  # 화면 너비의 20%로 폰트 크기 설정
    print('font_size : ', font_size)
    font_path = "C:/Clock_Display/DSEG7Classic-Bold.ttf"
    return pygame.font.Font(font_path, font_size)



# 색상 설정
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 255, 0)
green = (0, 128, 0)

# 버튼 클래스 정의
class RoundButton:
    def __init__(self, text, color, center, radius):
        self.text = text
        self.color = color
        self.center = center
        self.radius = radius
        self.font = pygame.font.Font(None, 36)
        self.text_surf = self.font.render(text, True, white)
        self.text_rect = self.text_surf.get_rect(center=center)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius)
        screen.blit(self.text_surf, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            distance = ((mouse_pos[0] - self.center[0]) ** 2 + (mouse_pos[1] - self.center[1]) ** 2) ** 0.5
            if distance <= self.radius:
                return True
        return False

'''
# 버튼 생성
button1 = RoundButton(" ", white, (1780, 1050), 25)
button2 = RoundButton(" ", yellow, (1830, 1050), 25)
button3 = RoundButton(" ", green, (1880, 1050), 25)
'''

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
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption("Clock with Color Buttons")

    # Move the window to the specified display
    hwnd = pygame.display.get_wm_info()['window']
    windll.user32.SetWindowPos(hwnd, None, left, top, 0, 0, 0x0001)

    return screen, (width, height)


'''
def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
'''

def draw_text(screen, text, font, color, center):
    text_surface = font.render(text, True, color)
    # print('center 좌표 : ', center)
    text_rect = text_surface.get_rect(center=(center))
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
    my_directory = "C:/Clock_Display"
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
        print(f'여기좀 보자 {proc}')
        if proc.info['name'] == process_name:
            return True
    return False


def run_process(process_path):
    try:
        subprocess.Popen(["start", "", process_path], shell=True)
    except Exception as e:
        print(f"프로세스 실행 중 오류가 발생했습니다: {e}")


def watchdog(process_name, check_interval):
    script_directory = "C:/Clock_Display"
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

                source_path = "C:/Clock_Display/main2,sub1"
                program_path = source_path + "/watchdog_autosize_reverse.exe"
                #program_path = script_directory + "/watchdog.py"  # 실행하려는 프로그램의 경로 정확히 입력
                run_process(program_path)
            else:
                print(f"정상 작동중...")
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("스크립트를 종료합니다.")


def run():
    process_name = "watchdog_autosize_reverse.exe"  # 실행 될 프로세스
    check_interval = 5  # 초 단위로 설정 (예: 5초)
    watchdog(process_name, check_interval)


print(f"current resolution : {resolution}")
#print('font_size : ', font_size)

display_number = 0 # 첫 번째 디스플레이는 1, 두 번째 디스플레이는 0, ...

# 현재 배경색 및 텍스트 색상 설정
bg_color = black
text_color = white

screen,resolution = set_display_mode(display_number)
font = load_font(resolution)
center_x, center_y = resolution[0] // 2, resolution[1] // 2


button1 = RoundButton(" ", white, ((center_x * 2) -125, (center_y*2)-30), 25)
button2 = RoundButton(" ", yellow, ((center_x * 2) -75, (center_y*2)-30), 25)
button3 = RoundButton(" ", green, ((center_x * 2) -25, (center_y*2)-30), 25)

def main(display_number):
    global bg_color, text_color, screen, resolution, font, center_x, center_y
    clock = pygame.time.Clock()


    class DisplayChangeDetector:
        def __init__(self):
            wc = win32gui.WNDCLASS()
            wc.lpfnWndProc = self.wnd_proc
            wc.lpszClassName = 'DisplayChangeDetector'
            self.class_atom = win32gui.RegisterClass(wc)
            self.hwnd = None

        def create_window(self):
            self.hwnd = win32gui.CreateWindow(
                self.class_atom,
                'DisplayChangeWindow',
                0,
                0, 0, 0, 0,
                0, 0, 0, None
            )
            win32gui.UpdateWindow(self.hwnd)


        def wnd_proc(self, hwnd, msg, wparam, lparam):
            global screen, resolution, font, center_x, center_y
            if msg == win32con.WM_DISPLAYCHANGE:
                print(f"Display resolution changed!")
                screen, resolution = set_display_mode(display_number)
                print(f'resolution : {resolution}')
                font = load_font(resolution)
                center_x, center_y = resolution[0] // 2, resolution[1] // 2
                button1.center = ((center_x * 2) - 125, (center_y * 2) - 30)
                button2.center = ((center_x * 2) - 75, (center_y * 2) - 30)
                button3.center = ((center_x * 2) - 25, (center_y * 2) - 30)

                # 텍스트 그리기
                draw_text(screen, current_time, font, text_color, (center_x , center_y))

                # 버튼 그리기
                button1.draw(screen)
                button2.draw(screen)
                button3.draw(screen)

                pygame.display.flip()
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)


        def run(self):
            self.create_window()
            win32gui.PumpMessages()

    detector = DisplayChangeDetector()
    detector.create_window()

    start_time = time.time()
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                # elif event.type == pygame.VIDEORESIZE:
                #     display_number=1 if event.w < resolution[0] else 0
                #     screen,resolution = set_display_mode(display_number)
                #     font = load_font(resolution)
                #     center_x, center_y = resolution[0] // 2, resolution[1] // 2
                #     button1.center = ((center_x * 2) -125,  (center_y*2)-30)
                #     button2.center = ((center_x * 2) -75, (center_y*2)-30)
                #     button3.center = ((center_x * 2) -25, (center_y*2)-30)
                #     print(f"{pygame.VIDEORESIZE}")

                    # 버튼 클릭 이벤트 처리
                elif button1.is_clicked(event):
                    bg_color = black
                    text_color = white
                    
                elif button2.is_clicked(event):
                    bg_color = black
                    text_color = yellow
                    
                elif button3.is_clicked(event):
                    bg_color = green
                    text_color = white

            left, top, right, bottom = get_display_rect(display_number)
            width = right - left
            height = bottom - top

            if resolution[0] != width or resolution[1] != height:
                #print('여기 옴?')
                screen, resolution = set_display_mode(display_number)
                #print(f'resolution : {resolution}')
                #font = load_font(resolution)
                center_x, center_y = resolution[0] // 2, resolution[1] // 2
                button1.center = ((center_x * 2) - 125, (center_y * 2) - 30)
                button2.center = ((center_x * 2) - 75, (center_y * 2) - 30)
                button3.center = ((center_x * 2) - 25, (center_y * 2) - 30)

                # 텍스트 그리기
                draw_text(screen, current_time, font, text_color, (center_x - (center_x / 10), center_y))

                # 버튼 그리기
                button1.draw(screen)
                button2.draw(screen)
                button3.draw(screen)

                pygame.display.flip()
                start_time = time.time()
                # print('Check resolution...')


            # 화면 채우기
            screen.fill(bg_color)

            # 현재 시간 가져오기
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")

            # 텍스트 그리기
            draw_text(screen, current_time, font, text_color , (center_x, center_y))

            # 버튼 그리기
            button1.draw(screen)
            button2.draw(screen)
            button3.draw(screen)

            
            # 화면 업데이트
            pygame.display.flip()

            # 초당 1 프레임
            clock.tick(30)

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main(display_number)
    run()
