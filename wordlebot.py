from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import string, re


dictionary = open("/Users/hardit/Desktop/wordle_words.txt", "r")
words = dictionary.readlines()
dictionary.close()
solutions = []
for word in words:
    solutions.append(word.strip())

class LetterState:
    state = 'abs'
    text = ''


#function defintions2
def substring_after(s, delim):
    return s.partition(delim)[2]

def replace_str_index(text,index,replacement):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def extract_letter_state(input_word ,row):
    letters = row.find_all('div')


    

    #letter 1
    global l1t
    global l1s
    ltr1 = str(letters[1])
    ltr1 = substring_after(ltr1 , " data-state=")
    l1t = str(input_word[0])

    
    if ltr1[1] == "p":
        l1s = "pre"
    elif ltr1[1] == "c":
        l1s = "cor"
    else:
        l1s = "abs"
    
    #letter 2
    global l2t
    global l2s
    ltr2 = str(letters[3])
    ltr2 = substring_after(ltr2 , " data-state=")
    l2t = input_word[1]
   
    if ltr2[1] == "p":
        l2s = "pre"
    elif ltr2[1] == "c":
        l2s = "cor"
    else:
        l2s = "abs"
    
     #letter 3
    global l3t
    global l3s
    ltr3 = str(letters[5])
    ltr3 = substring_after(ltr3 , " data-state=")
    l3t = input_word[2]
    
    if ltr3[1] == "p":
        l3s = "pre"
    elif ltr3[1] == "c":
        l3s = "cor"
    else:
        l3s = "abs"
     #letter 4
    global l4t
    global l4s
    ltr4 = str(letters[7])
    ltr4 = substring_after(ltr4 , " data-state=")
    l4t = input_word[3]
    
    if ltr4[1] == "p":
        l4s = "pre"
    elif ltr4[1] == "c":
        l4s = "cor"
    else:
        l4s = "abs"
    
     #letter 5
    global l5t
    global l5s
    ltr5 = str(letters[9])
    ltr5 = substring_after(ltr5 , " data-state=")
    l5t = input_word[4]
    if ltr5[1] == "p":
        l5s = "pre"
    elif ltr5[1] == "c":
        l5s = "cor"
    else:
        l5s = "abs"


def append_arg(letter_state , letter_text , letter_pos):
    global arg1
    global arg2
    global arg3
    global arg4
    
    l_arg3 = list(arg3)
    l_arg4 = list(arg4)
    letter_pos  -= 1
    
    if letter_text not in arg1:
        if letter_state != "abs":
            arg1 = arg1 + letter_text
        else:
            arg2 = arg2 + letter_text
        
    if letter_state == "cor":
        l_arg3[letter_pos] = letter_text
        
    if letter_state == "pre":
        l_arg4[letter_pos] = letter_text
        
    arg4 = ''.join(l_arg4)
    arg3 = ''.join(l_arg3)
    
    
def main_func(solutions=solutions):
    # this will be the array with the possible answers
    

    solutions = [x for x in solutions if all(y in x for y in arg1)]


    solutions = [x for x in solutions if all(y not in x for y in arg2)]


    positions = arg3
    positions = positions.replace("_", ".")

    # match based on positions
    positions_pattern = "^" + positions + "$"
    pattern = re.compile(positions_pattern)

    new_solutions = []
    for word in solutions:
        if pattern.match(word):
            new_solutions.append(word.strip())
    solutions = new_solutions

    w_positions = arg4
    
    if w_positions == "_____":
        count = 0
        for word in solutions:
            #print(word)
            count += 1

    else:
        location = 0
        for char in w_positions:
            if char != "_":
                w_positions = '_____'
                w_positions = replace_str_index(w_positions , location , char)
                w_positions = w_positions.replace("_", ".")
                # match based on positions
                w_positions_pattern = "^" + w_positions + "$"
                w_pattern = re.compile(w_positions_pattern)
                temp_solution = []
                for word in solutions:
                    if str(w_pattern.match(word)) == "None":
                        temp_solution.append(word.strip())
                solutions = temp_solution
            location+=1
    count = 0
    for word in solutions:
        #print(word)
        count+= 1

    print ("{0} words chosen to select\n".format(count))
    if count == 0:
        exit()

    if count == 1:
        print ("You won!")
        exit()
    return solutions
    
#END OF FUNCTION DELCARATIONS




driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.nytimes.com/games/wordle/index.html")
time.sleep(3)
driver.find_element(By.XPATH, "/html/body/div/div/dialog/div/button").click()
driver.execute_script(f"window.scrollTo({0},{500})")
time.sleep(2)

input_word = 'crate'


l1 = l2 = l3 = l4 = l5 = ""
l1s = l2s = l3s = l4s = l5s= ""
l1t= l2t = l3t = l4t = l5t =""


    
#arg1 is corect letters
#arg2 is wrong letters
#arg3 is correct position of letter i.e. green i.e. correct
#arg4 is wrong position of correct letter i.e. yellow i.e. present
arg1 = ""
arg2 = ""
arg3 = "_____"




for x in range(6):
    row_cnt = x+1
    actions = ActionChains(driver)
    actions.send_keys(input_word)
    actions.perform()
    actions.send_keys(Keys.ENTER)
    actions.perform()
    
    time.sleep(7)
    src = driver.page_source
    # print("Checking source")
    soup = BeautifulSoup(src, 'lxml')
    
    row_num = soup.find('div', {'aria-label': "Row {0}".format(row_cnt)})
    # print(row1)
    # print("\n\n\n")
    
    
    extract_letter_state(input_word ,row_num)
    l1 = LetterState()
    l2 = LetterState()
    l3 = LetterState()
    l4 = LetterState()
    l5 = LetterState()
    
    l1.state = l1s
    l2.state = l2s
    l3.state = l3s
    l4.state = l4s
    l5.state = l5s
    
    l1.text=  l1t
    l2.text = l2t
    l3.text = l3t
    l4.text = l4t
    l5.text = l5t
    arg4 = "_____"
    
    
    print("Row {0}: \n".format(row_cnt))
    print("L1:" ,l1.text , "-" , str(l1.state))
    print("L2:" ,l2.text , "-" , str(l2.state))
    print("L3:" ,l3.text , "-" , str(l3.state))
    print("L4:" ,l4.text , "-" , str(l4.state))
    print("L5:" ,l5.text , "-" , str(l5.state))

            
    append_arg(l1.state , l1.text , 1)
    append_arg(l2.state , l2.text , 2)
    append_arg(l3.state , l3.text , 3)
    append_arg(l4.state , l4.text , 4)
    append_arg(l5.state , l5.text , 5)
    
    print(arg1)
    print(arg2)
    print(arg3)
    print(arg4)
    
    
    solutions = main_func()
    input_word = solutions[0]






