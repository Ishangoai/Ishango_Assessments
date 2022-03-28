import pickle
import selenium.webdriver 

driver = selenium.webdriver.Firefox()
driver.get("https://coderbyte.com/sl")
pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))

