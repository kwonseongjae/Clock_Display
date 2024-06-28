import psutil
import time
import subprocess
import os
from datetime import datetime


def create_text_file(content, folder_path):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")
    file_name = f"{timestamp}.txt"
    file_path = os.path.join(folder_path, file_name)

    with open(file_path, "w") as file:
        file.write(content)





def run_process(process_path):
    try:
        subprocess.run(["start", "", process_path], shell=True)
    except Exception as e:
        print(f"프로세스 실행 중 오류가 발생했습니다: {e}")

def kill_process(process_name):
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            if process.info['name'] == process_name:
                process_pid = process.info['pid']
                process_to_kill = psutil.Process(process_pid)
                process_to_kill.terminate()
                print(f'프로세스 종료{process_name}')
        except:
            print(f'{process_name}종료 실패')
            pass

def check_process_running(process_name):
    for proc in psutil.process_iter(['name']):
        #print(f'여기좀 보자 {proc}')
        if proc.info['name'] == process_name:
            return True
    return False



'''
def check_process_running(process_name):
    for proc in psutil.process_iter(['name', 'cmdline']):
        if proc.info['name'] == 'python' and process_name in proc.info['cmdline']:
            return True
    return False
'''

def watchdog(process_name, check_interval):
    #script_directory = os.getcwd()
    script_directory = "C:/Clock_Display"
    folder_path = script_directory + "\log"

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

                source_path = "C:/Clock_Display/main1,sub2"
                program_path = source_path + "/clock.exe"

                
                #program_path1 = script_directory + "\\clock.py"  # 실행하려는 프로그램의 경로 정확히 입력
                print(program_path)
                # kill_process(process_name2)
                run_process(program_path)
            else:
                print(f"정상 작동중...")
           
            
            time.sleep(check_interval)
    except KeyboardInterrupt:
        print("스크립트를 종료합니다.")


def run():
    process_name = "clock.exe"
    check_interval = 5 # 초 단위로 설정 (예: 5초)
    watchdog(process_name, check_interval)

run()

