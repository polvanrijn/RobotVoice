from bs4 import BeautifulSoup
import requests
base_URL = "https://robots.ieee.org"
URL = base_URL + "/robots"

output_json = "["

page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.findAll("div", {"class":"robot-thumb p-0 mb-3 mb-md-4 mb-lg-5 m-0 px-2 px-md-3"})
n_robots = 0
for r in results:
    n_robots += 1
    print("Scraping robot no " + str(n_robots))
    output_json+="{"
    name = r.find('h3', attrs={'class':'robot-thumb-text text-center small d-block'}).contents[0]
    robot_inner_a = r.find('a')
    robot_url = base_URL + robot_inner_a['href']
    robot_images = []
    thumb_img = base_URL + robot_inner_a.find('img')['data-retina'][2:]
    robot_images.append(thumb_img)
    page_robot = requests.get(robot_url)
    soup_robot = BeautifulSoup(page_robot.content, "html.parser")
    description = soup_robot.findAll('p', {'class':'lead pt-2'})[0].contents[0]
    all_dl = soup_robot.findAll('dl', {'class':"pt-1"})
    dl_creator = all_dl[0]
    creator = dl_creator.find('a').contents[0]
    dl_country = all_dl[1]
    country = dl_country.find('dd').contents[0]
    dl_year = all_dl[2]
    year = dl_year.find('dd').contents[0]
    dl_type = all_dl[3]
    type = dl_type.find('dd').contents[0].split(',')
    specs = soup_robot.findAll('dd',{'class':'col-sm-8 pb-2 mb-2'})
    features = specs[0].contents[0]
    height = specs[1].contents[0]
    length = specs[2].contents[0]
    width = specs[3].contents[0]
    weight = specs[4].contents[0]
    speed = specs[5].contents[0]
    sensors = specs[6].contents[0]
    actuators = specs[7].contents[0]
    all_imgs=soup_robot.findAll('a',{'class':'carousel-cell'})
    for img in all_imgs:
        # If 10th character of href is a 'p', then the object is a photo
        if img['href'][9] == 'p':
            src_postfix = img.find('img')['src']
            src = robot_url + src_postfix
            robot_images.append(src)

    output_json += "\"name\":\"" + name + "\","
    output_json += "\"page_url\":\"" + robot_url + "\","
    output_json += "\"description\":\"" + description.replace('"', '\\"') + "\","
    output_json += "\"photos\":" + str(robot_images).replace('\'', '\"') + ","
    output_json += "\"types\":" + str(type).replace('\'', '\"') + ","
    output_json += "\"creator\":\"" + creator + "\","
    output_json += "\"country\":\"" + country + "\","
    output_json += "\"year\":\"" + year + "\","
    output_json += "\"features\":\"" + features.replace('"', '\\"') + "\","
    output_json += "\"height\":\"" + height + "\","
    output_json += "\"length\":\"" + length + "\","
    output_json += "\"width\":\"" + width + "\","
    output_json += "\"speed\":\"" + speed + "\","
    output_json += "\"sensors\":\"" + sensors.replace('"', '\\"') + "\","
    output_json += "\"actuators\":\"" + actuators.replace('"', '\\"') + "\""
    output_json += "},"

# delete last comma
output_json = output_json[:-1]
output_json += "]"
file = open('robots.json', 'w')
file.write(output_json)
file.close()
print(str(n_robots) + " robots found.")

