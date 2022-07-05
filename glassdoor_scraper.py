from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1120, 1000)
    url ="https://www.glassdoor.com/Job/foster-city-ca-"+keyword+"-jobs-SRCH_IL.0,14_IC1163997_KO15,29.htm?src=GD_JOB_AD&srs=ALL_RESULTS&jl=1007891100315&ao=1136043&s=345&guid=00000181bfeda65bb92afaacd021b371&pos=101&t=SR-JOBS-HR&vt=w&cs=1_16d0396a&cb=1656782432051&jobListingId=1007891100315&jrtk=3-0-1g6vur9k4kcle801-1g6vur9kfjoqf800-76aaad84e43fcb11-"
    driver.get(url)
    jobs = []
    print(num_jobs)
    while len(jobs) < num_jobs: #If true, should be still looking for new jobs.
    
        #Let the page load. Change this number based on your internet speed.
        time.sleep(slp_time)
        #Test for the "Sign Up" prompt and get rid of it.
        try:
            element = driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(5)

        try:
            element = driver.find_element_by_css_selector('[alt="Close"]').click() #clicking to the X.
            print(' x out worked')
            
        except NoSuchElementException:
            print(' x out failed') 
        
        #Going through each job in this page
        job_buttonss = driver.find_elements_by_xpath("//li[@class='react-job-listing css-nhtksm eigr9kq0']")
        job_buttons = driver.find_elements_by_xpath("//li[@class='react-job-listing job-search-key-nhtksm eigr9kq0']")
        job_buttonss.extend(job_buttons)
        number_of_all_page=driver.find_element_by_class_name("paginationFooter").text
        print("Now we in {} ".format(number_of_all_page))
        for job_button in job_buttonss:  
                        
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            job_button.click()  #You might 
            time.sleep(10)
            try:
                element = driver.find_element_by_css_selector('[alt="Close"]').click() #clicking to the X.
                print(' x out worked')
                
            except NoSuchElementException:
                pass
            time.sleep(10)
            collected_successfully = False
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('//div[@class="css-xuk5ye e1tk4kwz5"]').text
                    location = driver.find_element_by_xpath('.//div[@class="css-56kyx5 e1tk4kwz1"]').text
                    job_title = driver.find_element_by_xpath('.//div[@class="css-1j389vi e1tk4kwz2"]').text
                    job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                    collected_successfully = True
                except:
                    collected_successfully = True
                   
            
            try:
                
                salary_estimate = driver.find_element_by_xpath('//span[@class="css-1hbqxax e1wijj240"]').text   
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('.//span[@class="css-1m5m32b e1tk4kwz4"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important.
           
            #Going to the Company Overflow which clicking on this these contains Size, Type , Sector ,Founded ,Industry,Revenue 
            try:
                driver.find_element_by_xpath('.//h2[@class="mb-std css-qwgulo e9b8rvy0"]').click()
                try:
                    size=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size=-1
                
                try:
                    type_of_ownership=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership=-1
                    
                try:
                    sector=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector=-1
                
                try:
                    founded=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded=-1
                try:
                    industry=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry=-1
                try:
                    revenue=driver.find_element_by_xpath('//div[@class="d-flex justify-content-start css-daag8o e1pvx6aw2"]//span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue=-1
            except NoSuchElementException:  #Rarely, some job postings do not have the "Company Overflow" tab.
                
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1
                competitors = -1

            if verbose:
                print('the Job Title is : {}'.format(job_title))
                print('the compny name is :{}'.format(company_name))
                print('the Location is {} :'.format(location))
                print('the job Description is {}:'.format(job_description))
                print('the Salary Estimate is {}:'.format(salary_estimate))
                print('the Size is : {}'.format(size))
                print('Type of Ownership  : {}'.format(type_of_ownership))
                print('The Sector is : {}'.format(sector))
                print('The Founded is : {}'.format(founded))
                print('The Industry is : {} '.format(industry))
                print('The Revenue is : {}'.format(revenue))
                
            #add job information post to the jobs    
            jobs.append({"Job Title" : job_title,
                         "Company Name":company_name,
                         "Location":location,
                         "Job Description":job_description,
                         "Salary Estimate":salary_estimate,
                         "Rating":rating,
                         "Size":size,
                         "Type of ownership":type_of_ownership,
                         "Sector":sector,
                         "Founded":founded,
                         "Industry":industry,
                         "Revenue":revenue })                             
             
        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//button[@class="nextButton css-1hq9k8 e13qs2071"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
path='chromedriver.exe'
df=get_jobs('Data Scientist', 5, False, 'chromedriver.exe', 10)
df.to_csv("data_from_glassdoor.csv",index=True)