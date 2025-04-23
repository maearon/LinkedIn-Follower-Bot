from random import *
import time
import datetime
import os

import nodriver as uc
from nodriver import *

browserPath = '/usr/bin/google-chrome'  # Đường dẫn Chrome trên Ubuntu
profilePath = os.path.expanduser('~/code/LinkedIn-Follower-Bot/LinkedInProfile')  # Đường dẫn user data

LoggedIn = 1  # Giả định đã login sẵn

async def main():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    total_accounts = 0
    Skip = 0
    log_file_path = "AccountLog.txt"

    # Nếu file log chưa tồn tại, tạo mới
    if not os.path.exists(log_file_path):
        with open(log_file_path, 'w') as f:
            pass

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            parts = line.strip().split(" on ")
            if len(parts) != 2:
                continue
            accounts_part = parts[0]
            date_part = parts[1]

            try:
                accounts_count = int(accounts_part.split(": ")[1])
                log_date = datetime.datetime.strptime(date_part, '%Y-%m-%d')
                if log_date >= datetime.datetime.now() - datetime.timedelta(days=7):
                    total_accounts += accounts_count
            except:
                continue

    if total_accounts >= 100:
        Skip = 1
        print("Total Accounts This Week: " + str(total_accounts))

    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if current_date in line:
                Skip = 1
                print("Already ran today: " + current_date)
                print("Total Accounts This Week: " + str(total_accounts))

    if not Skip:
        x = 0
        y = 0
        try:
            driver = await uc.start(
                headless=False,
                browser_executable_path=browserPath,
                user_data_dir=profilePath,
                browser_args=[
                    f"--window-size={randint(800, 1600)},{randint(600, 1000)}"
                ]
            )

            tab = await driver.get("https://www.linkedin.com/mynetwork/grow/")
            if LoggedIn:
                await driver.wait(time=random())
                bottomFrame = await tab.find("People you may know", timeout=25)

                while y < 10:
                    await bottomFrame.scroll_into_view()
                    time.sleep(1)
                    y += 1

                connectBars = await tab.find_all("to connect", timeout=25)
                for bar in connectBars:
                    if x >= 25:
                        break
                    await bar.scroll_into_view()
                    await bar.click()
                    time.sleep(2 + 5 * random())
                    x += 1

                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"Accounts ran: {x} on {current_date}\n")

                await tab.close()
            else:
                input("Press Enter to continue...")
                await tab.close()
        except Exception as e:
            print("Lỗi xảy ra:", e)
            if x > 0:
                with open(log_file_path, 'a') as log_file:
                    log_file.write(f"Accounts ran: {x} on {current_date}\n")
            try:
                await tab.close()
            except:
                pass

if __name__ == "__main__":
    uc.loop().run_until_complete(main())
