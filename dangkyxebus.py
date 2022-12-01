from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telegram
import time
from datetime import datetime
from datetime import timedelta
import json

# Screen shot
def save_screenshot(driver: webdriver.Chrome, path: str = '/tmp/screenshot.png') -> None:
    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script('return document.body.parentNode.scrollWidth')
    required_height = driver.execute_script('return document.body.parentNode.scrollHeight')
    driver.set_window_size(required_width, required_height)
    driver.save_screenshot(path)  # has scrollbar
    # driver.find_element_by(By.TAG_NAME, 'body').screenshot(path)  # avoids scrollbar
    # driver.set_window_size(original_size['width'], original_size['height'])

tele_token = '1914822073:AAGY3gT842M9vS3_-6V37gwiDeQa6mu_VzU'
chat_id = '943105950'
msg = ''
result = False
options = Options()
options.headless = True
options.add_argument("--window-size=2316,1080")
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(
    options=options) #, executable_path='/samsung/chromedriver'

while True:
    driver.get("https://203.254.249.240/dangkyxebus")
    try:
        # comp_select = Select(driver.find_element(By.ID,"CompName"))
        comp_select = Select(driver.find_element(By.XPATH,"//select[@id='CompName']")) #//select[@id='CompName']//h4[1]//b[1]
		# print(comp_select)
        comp_select.select_by_index('1')

        # driver.switch_to_window(driver.window_handles[1])

        driver.find_element(By.ID, 'GenNo').send_keys('14502242')
        driver.find_element(By.ID, 'Fullname').send_keys('Nguyễn Văn Nguyện')
        driver.find_element(By.ID, 'otp').send_keys('000036')
        # Click vao truy cap
        try:
            driver.find_element(By.XPATH, '/html/body/div/form/fieldset/div/div[6]/input[1]').click()
        except:
            pass

        # Chon ngay di xe bus
        try:
            # Thoi gian tiem
            # current_day = datetime.now().strftime("%d/%m/%Y")
            # thu2 = (datetime.now() + timedelta(days=1) ).strftime("%d/%m/%Y")
            for i in range(2, 9):
                # Cuoi tuan nghỉ
                if i == 7 or i == 8:
                    try:
                        cuoituan_select = Select(driver.find_element(By.ID,
                        "answer1_"+"".join(str(i))))
                        cuoituan_select.select_by_index(1)
                        print('1'+"".join(str(i)))
                    except:
                        pass
                else:
                    # 1
                    try:
                        ngaysudung_select = Select(driver.find_element(By.ID,
                        "answer1_"+"".join(str(i))))
                        ngaysudung_select.select_by_index(2)
                        print('1'+"".join(str(i)))
                    except:
                        pass
                    # 2
                    try:
                        calamviec_select = Select(driver.find_element(By.ID,
                        "answer2_"+"".join(str(i))))
                        calamviec_select.select_by_visible_text('Ca ngày')
                        print('2'+"".join(str(i)))
                    except:
                        pass
                    # 3
                    try:
                        chieusudung_select = Select(driver.find_element(By.ID,
                        "answer3_"+"".join(str(i))))
                        chieusudung_select.select_by_visible_text('Đi làm - Đi về')
                        print('3'+"".join(str(i)))
                    except:
                        pass
                    # 4
                    try:
                        tuyenxedi_select = Select(driver.find_element(By.ID,
                        "answer4_"+"".join(str(i))))
                        tuyenxedi_select.select_by_index('7')
                        print('4'+"".join(str(i)))
                    except:
                        pass
                    # 5
                    try:
                        tuyenxeve_select = Select(driver.find_element(By.ID,
                        "answer5_"+"".join(str(i))))
                        tuyenxeve_select.select_by_index('7')
                        print('5'+"".join(str(i)))
                    except:
                        pass
                    # 6
                    try:
                        khunggiove = Select(driver.find_element(By.NAME,
                        "answer6_"+"".join(str(i))))
                        khunggiove.select_by_index(2)
                        print("6"+"".join(str(i)))
                    except:
                        pass
                    # 7
                    try:
                        mucdich_select = Select(driver.find_element(By.ID,
                        "answer7_"+"".join(str(i))))
                        mucdich_select.select_by_visible_text('Công việc')
                        print('7'+"".join(str(i)))
                    except:
                        pass
                    # 8
                    try:
                        baixe_select = Select(driver.find_element(By.ID,
                        "answer8_"+"".join(str(i))))
                        baixe_select.select_by_visible_text('Cổng Nam')
                        print('8'+"".join(str(i)))
                    except:
                        pass
                
                time.sleep(1)
        except:
            pass
        
        # Cuoi tuan

        # Cam ket
        try:
            driver.find_element(By.ID,'QYN').click()
        except:
            pass

        # Nhấn nút gửi đi
        try:
            driver.find_element(By.XPATH, "//input[@type='submit']").click()
        except:
            print('Nhấn gửi không thành công')
            pass
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present(),
                                        'Gửi đi thành công!')
            alert = driver.switch_to.alert
            alert.accept()
            print("alert accepted")
        except TimeoutException:
            print("no alert")
            pass
        try:
            # Kiểm tra kết quả
            driver.find_element(By.CLASS_NAME, "validation-summary-success")
            msg = "Đăng ký thành công"
            result = True
        except:
            msg = "Chưa thành công"
            result = False
    except :
        msg = "Chưa thành công"
        result = False


    # driver.save_screenshot('dangkyxebus.png')
    save_screenshot(driver,"dangkyxebus.png")

    if result == True:
        telegram_notify = telegram.Bot(tele_token)
        telegram_notify.send_photo(chat_id=chat_id, photo=open('dangkyxebus.png', 'rb'), caption=msg)
        break
    if result == False:
        current_time = datetime.now().hour
        if(current_time - 15 > 0):
            break
        try:
            # telegram_notify = telegram.Bot(tele_token)
            # telegram_notify.send_message(chat_id=chat_id, text=msg+", Cần truy cập link sau để khai báo:\n https://203.254.249.240/dangkyxebus")
            # Gửi picture qua telegram
            telegram_notify = telegram.Bot(tele_token)
            telegram_notify.send_photo(chat_id=chat_id, photo=open('dangkyxebus.png', 'rb'), caption=msg+", AhihiCần truy cập link sau để khai báo:\n https://203.254.249.240/dangkyxebus")
            
        except Exception as ex:
            print(ex)

        time.sleep(1800)