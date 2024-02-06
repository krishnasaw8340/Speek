from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep
from VoiceAssistant import response, rec_audio

def setup_webdriver():
    chrome_options = webdriver.ChromeOptions()
    # Allow permission for location
    chrome_options.add_argument("--use-fake-ui-for-media-stream")

    # Set up the WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    return driver

def pizza():
    driver = setup_webdriver()

    try:
        response("Opening Dominos")
        driver.get("https://www.dominos.co.in/")
        driver.maximize_window()
        sleep(2)

        # Correcting the way to find the "ORDER ONLINE NOW" link
        response("Ordering Online")
        order_online_link = driver.find_element(By.LINK_TEXT, "ORDER ONLINE NOW")
        order_online_link.click()
        sleep(2)

        # Locate and interact with the location input field
        location_input = driver.find_element(By.CLASS_NAME, "srch-cnt-srch-inpt")  # Replace with the actual class name
        location_input.click()

        response("Gathering your Location")
        location = ("Kelambakkam-Vandalur Road, Kelambakkam")

        location_input.send_keys(location)  # Send text to location search input field
        sleep(2)

        # Select the location from suggestions
        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/div[2]/div/div[1]/input').send_keys(location)
        sleep(2)

        driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div/div[3]/div/div[1]/div[2]/div[2]/div/ul/li[1]').click()
        sleep(2)

        # Rest of your code...
        phone_num = "6201862014"
        # Rest of your code...
        response("Your Phone number is " + phone_num)

        try:
            driver.find_element(By.CLASS_NAME, "prf-grp-txt").click()
            driver.find_element(By.XPATH,
                '//*[@id="__next"]/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/form/div[1]/div[2]/input').send_keys(
                phone_num)  # Send text to phone number input field
            driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/form/div[2]/input').click()
            sleep(5)
            response("What is your OTP")
            otp_log = rec_audio()
            driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[1]/div/div[3]/div[3]/div[2]/div/div[3]/div/div/div/div[2]/div/div/div/div[1]/input').send_keys(otp_log)
            sleep(2)
            response("Do you want me to order from your favorites?")
            query_fav = rec_audio()
            if "yes" in query_fav:
                try:
                    driver.find_elements(By.XPATH,
                        '//*[@id="mn-lft"]/div[6]/div/div[6]/div/div/div[2]/div[3]/div/button/span')[0].click()  # Add your favorite pizza
                    sleep(1)
                except:
                    response("The entered OTP is incorrect.")
                response("Adding your favorites to cart")
                response("Do you want me to add extra cheese to your pizza?")
                ex_cheese = rec_audio()
                if "yes" in ex_cheese:
                    response("Extra cheese added")
                    driver.find_elements(By.XPATH,
                        '//*[@id="mn-lft"]/div[6]/div/div[1]/div/div/div[2]/div[3]/div[2]/button')[0].click()  # Add extra cheese
                elif "no" in ex_cheese:
                    driver.find_elements(By.XPATH,
                        '//*[@id="mn-lft"]/div[6]/div/div[1]/div/div/div[2]/div[3]/div[1]/button/span')[0].click()
                else:
                    response("I dont know that")
                    driver.find_elements(By.XPATH,
                        '//*[@id="mn-lft"]/div[6]/div/div[1]/div/div/div[2]/div[3]/div[1]/button/span')[0].click()
                driver.find_elements(By.XPATH,
                    '//*[@id="mn-lft"]/div[16]/div/div[1]/div/div/div[2]/div[2]/div/button')[0].click()  # Add a pepsi
                sleep(1)
                response("Would you like to increase the qty?")
                qty = rec_audio()
                qty_pizza = 0
                qty_pepsi = 0
                if "yes" in qty:
                    response("Would you like to increase the quantity of pizza?")
                    wh_qty = rec_audio()
                    if "yes" in wh_qty:
                        response("How many more pizzas would you like to add? ")
                        try:
                            qty_pizza = rec_audio()
                            qty_pizza = int(qty_pizza)
                            if qty_pizza > 0:
                                talk_piz = f"Adding {qty_pizza} more pizzas"
                                response(talk_piz)
                                for i in range(qty_pizza):
                                    driver.find_elements(By.XPATH,
                                        '//*[@id="__next"]/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div[1]/div/div/div[2]/div/div/div[2]')[0].click()
                        except:
                            response("I dont know that.")
                    else:
                        pass

                    response("Would you like to increase the quantity of pepsi?")
                    pep_qty = rec_audio()
                    if "yes" in pep_qty:
                        response("How many more pepsis would you like to add? ")
                        try:
                            qty_pepsi = rec_audio()
                            qty_pepsi = int(qty_pepsi)
                            if qty_pepsi > 0:
                                talk_pep = f"Adding {qty_pepsi} more pepsis"
                                response(talk_pep)
                                for i in range(qty_pepsi):
                                    driver.find_elements(By.XPATH,
                                        '//*[@id="__next"]/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div/div/div[2]/div/div/div[2]')[0].click()
                        except:
                            response("I dont know that.")
                    else:
                        pass

                elif "no" in qty:
                    pass

                total_pizza = qty_pizza + 1
                total_pepsi = qty_pepsi + 1
                tell_num = f"This is your list of order. {total_pizza} Pizzas and {total_pepsi} Pepsis. Do you want to checkout?"
                response(tell_num)
                check_order = rec_audio()
                if "yes" in check_order:
                    response("Checking out")
                    driver.find_elements(By.XPATH,
                        '//*[@id="__next"]/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div/div/div[2]/div[2]/button')[0].click()  # Click on checkout button
                    sleep(1)
                    total = driver.find_element(By.XPATH,
                        '//*[@id="__next"]/div/div[1]/div[2]/div[3]/div[2]/div/div[6]/div/div/div[6]/span[2]/span')
                    total_price = f'total price is {total.text}'
                    response(total_price)
                    sleep(1)
                else:
                    exit()

                response("Placing your order")
                driver.find_elements(By.XPATH,
                    '//*[@id="__next"]/div/div[1]/div[2]/div[3]/div[2]/div/div[6]/div/div/div[8]/button')[0].click()  # Click on place order button
                sleep(2)

                response("Saving your location")
                driver.find_element(By.XPATH,
                    '//*[@id="__next"]/div/div[1]/div[2]/div[3]/div[2]/div/div[3]/div/div[3]/div/div/div[3]/div/div/input').click()  # Save your location
                sleep(2)

                response("Do you want to confirm your order?")
                confirm = rec_audio()
                if "yes" in confirm:
                    try:
                        driver.find_element(By.XPATH,
                            '//*[@id="__next"]/div/div[1]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[2]/button').click()
                        sleep(2)
                    except:
                        response("The store is currently offline.")
                        exit()
                    response("Placing your order")
                    response("Your order is places successfully. Wait for Dominos to deliver your order. Enjoy your day!")
                else:
                    exit()
            else:
                exit()
        except Exception as e:
            print(f"Exception: {e}")
            exit()
        sleep(5)  # For visibility, adjust as needed
    finally:
        driver.quit()

# Example usage:
pizza()
