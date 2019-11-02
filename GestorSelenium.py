from selenium import webdriver

def StartSelenium(user):

    # OPEN NEW WINDOW ON FIREFOX
    print("Initializing components")
    driver = webdriver.Firefox()

    # OPEN URL ON BROWSER
    print("Connecting")
    driver.get('https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin')

    # INSERT LOGGING DATA ON LINKEDIN
    print("Logging in")
    username = driver.find_element_by_id('username')
    username.send_keys(user.username)
    password = driver.find_element_by_id('password')
    password.send_keys(user.password)
    driver.find_element_by_css_selector('.btn__primary--large.from__button--floating').click()

    return driver