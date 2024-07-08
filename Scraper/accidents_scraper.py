import csv
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.edge.service import Service



class Driver:
    def __init__(self):
        self.index = 1
        edge_options = Options()
        #edge_options.add_argument("--no-sandbox")
        #edge_options.add_argument("--disable-gpu")        
        edge_options.add_argument("--disable-extensions")        
        #edge_options.add_argument("--enable-features=VaapiVideoDecode")
        edge_options.add_argument("--ignore-gpu-blocklist")
        edge_options.add_argument('--ignore-certificate-errors')
        edge_options.add_argument('--incognito')
        edge_options.add_argument('--incognito')
        #edge_options.add_argument('--headless')
        edge_options.add_argument('--headless=new')
        edge_options.page_load_strategy = 'eager'
        service = Service(executable_path="C:\\Users\\Fohacker\\Downloads\\edgedriver_win64 (1)\\msedgedriver.exe")

        self.driver = webdriver.Edge(options=edge_options, service=service)

    def extract_accidents(self, column_names):
        self.driver.get("https://aviation-safety.net/database/")

        for i in range(2023, 2025):
            print(f'analisando ano {i}')
            base_url = "https://aviation-safety.net/database/year/%d" % i
            self.link = base_url
            self.driver.get(self.link)
            elements = self.driver.find_elements(
                By.XPATH, f'//a[contains(text(), "{i}")]'
            )

            page_number = 1
            print(len(elements))
            if len(elements) != 100:
                print('Diferente de 100 elements')
                self.getDataFromPage(elements, column_names)
                
            else:
                while len(elements) == 100:
                    print('Igual a 100 elements')
                    print(f'Page number = {page_number}')
                    self.link = base_url + "/%d" % page_number
                    print(self.link)
                    self.driver.get(self.link)
                    elements = self.driver.find_elements(
                        By.XPATH, f'//a[contains(text(), "{i}")]'
                    )
                    self.getDataFromPage(elements, column_names)
                    page_number += 1

        print('------- Encerrando analise -----------')
        self.driver.quit()

    def getDataFromPage(self, elements, column_names):
        print('entrou em getDataFromPage')
        
        arr = []       
        for ind, el in enumerate(elements):
            # index            
            try:
                el.click()
            except StaleElementReferenceException:
                print("Click not working ")
            except Exception as e:
                print(f"An unexpected error occurred while finding element: {e}")
            
            #print(el.accessible_name)
            index = self.driver.current_url.split('/')[-1]
            print(index)
            arr.append(index)
            for col in column_names[1:]:
                if col == "Type Code:":
                    field = self.driver.find_element(By.XPATH,"//table/tbody/tr[td[contains(.,'Type:')]]/td[2]/a")
                    field = field.get_attribute('href').split('/')[-1]                              
                    
                else:
                    field = self.getObject(f"//table/tbody/tr[td[contains(.,'{col}')]]/td[2]")
                print(field)
                arr.append(field)
            
            self.parseData(accidents_filename,"a", arr)
            arr = []
            try:
                self.driver.back()
            except WebDriverException:
                self.driver.get(self.link)
                print("Failed to navigate back")
        
        

    def extract_countries(self):
        self.driver.get("https://aviation-safety.net/database/country/")

        elements = self.driver.find_elements(
                        By.XPATH, '//*[@id="contentcolumn"]/div/p/table/tbody/tr/td/a | //*[@id="contentcolumn"]/div/p/table/tbody/tr/td/p/a'
                    )
        
        for el in elements:
            arr = []
            country_name = el.text
            country_code = el.get_attribute('href').split('/')[-1]
            arr.append(country_name)
            arr.append(country_code)
            self.parseData(countries_filename,"a",arr)
    
    def extract_aircrafts(self):
        

        # Para cada letra
        for character in string.ascii_uppercase:
            self.driver.get(f'https://aviation-safety.net/asndb/types/{character}')

            # Pegar os elementos
            elements = self.driver.find_elements(
                        By.XPATH, '//*[@id="myTable"]/tbody/tr'
                    )
            
            print(elements)
            # Para cada elemento da pagina
            arr = []
            for el in elements:           
                print('começo do for')
                print(el.text)
                print(self.driver.current_url)
                
                
                name_and_code_el = el.find_element(By.XPATH,'.//td/a')
                print('printando name and code')
                print(name_and_code_el.text)
                aircraft_name = name_and_code_el.text
                aircraft_code = name_and_code_el.get_attribute('href').split('/')[-1]
                year_of_first_flight = el.find_element(By.XPATH,'.//td[2]').text

                arr.append(aircraft_name)
                arr.append(aircraft_code)
                arr.append(year_of_first_flight)
                
                # Clicar e pegar os dados do pais
                try:
                    name_and_code_el.click()
                    print('cliquei no nome')
                    print(self.driver.current_url)
                except StaleElementReferenceException:
                    print("Click not working ")
                except Exception as e:
                    print(f"An unexpected error occurred while finding element: {e}")
                
                # Pegar o código do país                
                try:
                    img_name = self.driver.find_element(By.XPATH,'//*[@id="contentcolumnfull"]/div/div[2]/table/tbody/tr[1]/td[2]/img')
                    manufacturer_country_code = img_name.get_attribute('src').split('/')[-1].split('.')[0]
                except NoSuchElementException:
                    print("No country identified")
                    manufacturer_country_code = ""    

                # Escrever o dado e zerar o array
                arr.append(manufacturer_country_code)

                self.parseData(aircrafts_filename,"a", arr)
                
                arr = []
                # Voltar
                
                try:
                    self.driver.back()
                    print('voltar')
                    print(self.driver.current_url)
                except WebDriverException:
                    self.driver.get(self.link)
                    print("Failed to navigate back")

                
                


        

        


    def getObject(self, strXPath):

        try:
            o = self.driver.find_element(By.XPATH, strXPath)
            if o.text == "" or o.text is None or o.text == " ":
                res = " "
            else:
                res = o.text
        except NoSuchElementException:
            print("No such object", strXPath)
            return " "
        except NoSuchWindowException:
            print("No such window", strXPath)
            return " "
        except StaleElementReferenceException:
            print("Element is stale")
            return " "

        return res

    def get_index(self, column_names, column_name):
        try:
            index = column_names.index(column_name)
            return index
        except ValueError:
            print("ERROR", column_name, self.index)
            return 29

    def getImageLink(self, strXPath):
        try:
            image_link = self.driver.find_element(By.XPATH, strXPath).get_attribute(
                "src"
            )
        except NoSuchElementException:
            #print("Image does not exist")
            return " "
        except NoSuchWindowException:
            print("No such window")
            return " "
        except StaleElementReferenceException:
            print("Image is stale")
            return " "

        return image_link

    def parseData(self, file_name, option, row):
        filecsv = file_name

        with open(filecsv, option, newline="\n", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def printData(self,name):
        filecsv = name

        with open(filecsv, "r", encoding="utf-8") as file:
            reader = csv.reader(file)

            for row in reader:
                print(row)



accident_column_names =["Index:",
                        "Date:",
                        "Time:",
                        "Type:",
                        "Type Code:",
                        "Owner/operator:",
                        "Registration:",
                        "MSN:",
                        "Year of manufacture:",
                        "Engine model:",
                        "Total airframe hrs:",
                        "Cycles:",
                        "Fatalities:",
                        "Other fatalities:",
                        "Aircraft damage:",
                        "Category:",
                        "Location:",
                        "Phase:",
                        "Nature:",
                        "Departure airport:",
                        "Destination airport:",
                        "Investigating agency:",
                        "Confidence Rating:"]

countries_col_names = ["Country Name",
                       "Country Code"]

aircrafts_col_names = ["Aircraft Name", 
                       "Aircraft Code", 
                       "Year of First Flight", 
                       "Manufacturer Country"]

accidents_filename = "data.csv"
countries_filename = "countries_data.csv"
aircrafts_filename = "aircrafts_data.csv"


tasker = Driver()
print(len(countries_filename))
print('Colunas')
tasker.parseData(accidents_filename,"w", accident_column_names)
tasker.extract_accidents(accident_column_names)

#tasker.parseData(countries_filename,"w", countries_col_names)
#tasker.extract_countries()

#tasker.parseData(aircrafts_filename,"w", aircrafts_col_names)
#tasker.extract_aircrafts()



