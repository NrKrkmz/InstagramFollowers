from instagramUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver_path = "/home/nur/Downloads/chromedriver_linux64/chromedriver"

class Instagram:
    def __init__(self, username, password):

        self.browserProfile = webdriver.ChromeOptions()
        self.browserProfile.add_experimental_option('prefs', {'intl.accept_languages': 'en , en_US'})
        self.browser = webdriver.Chrome(driver_path, chrome_options=self.browserProfile)
        self.username = username
        self.password = password


    def signIn(self):
        self.browser.get('https://www.instagram.com/accounts/login/?hl=tr')
        time.sleep(3)
        usernameInput = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label/input')
        passwordInput = self.browser.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label/input')

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)
        time.sleep(3)


    def getFollowers(self):

       # self.browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div/section/div/button').click()
        #time.sleep(2)

        self.browser.get(f'https://www.instagram.com/{self.username}')
        time.sleep(2)
        self.browser.find_element_by_tag_name(f'a[href="/{self.username}/followers/"]').click()
        time.sleep(2)
        
        dialog = self.browser.find_element_by_css_selector('div[role=dialog] ul')
        followerCount = len(dialog.find_elements_by_css_selector("li"))

        print(f'first count: {followerCount}')

        action = webdriver.ActionChains(self.browser)

        while True:
            dialog.click()
            action.key_down(Keys.END).perform()
            
            time.sleep(0.5)

            newCount = len(dialog.find_elements_by_css_selector('li'))

            if followerCount != newCount:
                followerCount = newCount
                print(f'second count : {newCount}')
                time.sleep(1)
            else:
                break
        
        followers = dialog.find_elements_by_css_selector('li')

        followerList = []
        i = 0
        for user in followers:
            i += 1
            if i == max :
                break
            link = user.find_element_by_css_selector('a').get_attribute('href')
            followerList.append(link)

        with open('followers.txt', 'w', encoding='UTF-8') as file:
            for item in followerList:
                file.write(item + '\n')

    def followUser(self, username):
        self.browser.get('https://www.instagram.com/' + username)
        time.sleep(2)

        followButton = self.browser.find_element_by_tag_name('button')
        print(followButton.text)
        if followButton.text != 'Following': 
            followButton.click()
            time.sleep(2)
        else:
            print('Following !')


    def unFollowUser(self, username):

        self.browser.get('https://www.instagram.com/'+username)
        time.sleep(2)

        unFollowButton = self.browser.find_element_by_tag_name("button")

        if unFollowButton.text == 'Following':

            unFollowButton.click()
            time.sleep(2)
            self.browser.find_element_by_xpath('//button[text()="Unfollow"]').click()

        else :

            print('Not Following !')



instagram = Instagram(username,password)
instagram.signIn()
instagram.getFollowers()
#instagram.followUser()
#instagram.unFollowUser()

