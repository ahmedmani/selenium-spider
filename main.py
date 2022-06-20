from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import re, random, time, code
import random

starting_sites = ["https://store.steampowered.com/app/1105670/The_Last_Spell/"]
blocked_urls = ["https://store.steampowered.com/", "https://store.steampowered.com/about/?snr=1_4_4__global-header", "https://help.steampowered.com/en/", "https://steamcommunity.com/", "https://store.steampowered.com/?snr=1_4_4__global-responsive-menu"]
pages_to_crawl = 100
base_domain = "store.steampowered.com"
nodes = {'https://store.steampowered.com/search/?tags=3835&category3=2': 'base url', 'https://store.steampowered.com/search/': {'inum': 175, 'prev_url': 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/'}, 'https://store.steampowered.com/agecheck/app/1139900/': {'inum': 36, 'prev_url': 'https://store.steampowered.com/search/'}, 'https://store.steampowered.com/about/': {'inum': 88, 'prev_url': 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/'}, 'https://store.steampowered.com/app/632360/Risk_of_Rain_2/': {'inum': 245, 'prev_url': 'https://store.steampowered.com/about/'}, 'https://store.steampowered.com/app/581320/Insurgency_Sandstorm/': {'inum': 240, 'prev_url': 'https://store.steampowered.com/app/632360/Risk_of_Rain_2/'}, 'https://store.steampowered.com/sub/632434/': {'inum': 199, 'prev_url': 'https://store.steampowered.com/app/581320/Insurgency_Sandstorm/'}, 'https://store.steampowered.com/recommended/morelike/sub/632434/': {'inum': 169, 'prev_url': 'https://store.steampowered.com/sub/632434/'}, 'https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/': {'inum': 269, 'prev_url': 'https://store.steampowered.com/recommended/morelike/sub/632434/'}, 'https://store.steampowered.com/agecheck/app/218620/': {'inum': 36, 'prev_url': 'https://store.steampowered.com/app/730/CounterStrike_Global_Offensive/'}, 'https://store.steampowered.com/app/1029690/Sniper_Elite_5/': {'inum': 178, 'prev_url': 'https://store.steampowered.com/agecheck/app/218620/'}, 'https://store.steampowered.com/tags/en/Multiplayer/': {'inum': 260, 'prev_url': 'https://store.steampowered.com/app/1029690/Sniper_Elite_5/'}, 'https://store.steampowered.com/tags/en/Multiplayer/4182/': {'inum': 278, 'prev_url': 'https://store.steampowered.com/tags/en/Multiplayer/'}, 'https://store.steampowered.com/app/364360/Total_War_WARHAMMER/': {'inum': 300, 'prev_url': 'https://store.steampowered.com/tags/en/Multiplayer/4182/'}, 'https://store.steampowered.com/app/1072040/Panzer_Corps_2/': {'inum': 323, 'prev_url': 'https://store.steampowered.com/app/364360/Total_War_WARHAMMER/'}, 'https://store.steampowered.com/news/app/1072040/view/3225149691072104126': {'inum': 101, 'prev_url': 'https://store.steampowered.com/app/1072040/Panzer_Corps_2/'}, 'https://store.steampowered.com/developer/Slitherine/': {'inum': 102, 'prev_url': 'https://store.steampowered.com/news/app/1072040/view/3225149691072104126'}, 'https://store.steampowered.com/app/1089840/Armored_Brigade/': {'inum': 173, 'prev_url': 'https://store.steampowered.com/developer/Slitherine/'}, 'https://store.steampowered.com/tags/en/Strategy/': {'inum': 36, 'prev_url': 'https://store.steampowered.com/app/1089840/Armored_Brigade/'}, 'https://store.steampowered.com/app/1604030/V_Rising/': {'inum': 255, 'prev_url': 'https://store.steampowered.com/app/794260/Outward_Definitive_Edition/'}, 'https://store.steampowered.com/app/264710/Subnautica/': {'inum': 272, 'prev_url': 'https://store.steampowered.com/app/1604030/V_Rising/'}, 'https://store.steampowered.com/tags/en/Massively%20Multiplayer/': {'inum': 186, 'prev_url': 'https://store.steampowered.com/app/264710/Subnautica/'}, 'https://store.steampowered.com/app/1845260/_/': {'inum': 212, 'prev_url': 'https://store.steampowered.com/tags/en/Massively%20Multiplayer/'}, 'https://store.steampowered.com/genre/Early%20Access/': {'inum': 258, 'prev_url': 'https://store.steampowered.com/app/1845260/_/'}, 'https://store.steampowered.com/app/1169040/Necesse/': {'inum': 216, 'prev_url': 'https://store.steampowered.com/genre/Early%20Access/'}, 'https://store.steampowered.com/tags/en/Action/': {'inum': 271, 'prev_url': 'https://store.steampowered.com/app/1169040/Necesse/'}, 'https://store.steampowered.com/tags/en/Action/1774/': {'inum': 36, 'prev_url': 'https://store.steampowered.com/tags/en/Action/'}, 'https://store.steampowered.com//mobile': {'inum': 36, 'prev_url': 'https://store.steampowered.com/tags/en/Action/1774/'}, 'https://store.steampowered.com/steamdeck': {'inum': 169, 'prev_url': 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/'}, 'https://store.steampowered.com/news/': {'inum': 37, 'prev_url': 'https://store.steampowered.com/agecheck/app/252490/'}, 'https://store.steampowered.com/news/collection/press/': {'inum': 69, 'prev_url': 'https://store.steampowered.com/news/'}, 'https://store.steampowered.com/news/collection/steam/': {'inum': 34, 'prev_url': 'https://store.steampowered.com/news/collection/press/'}, 'https://store.steampowered.com/agecheck/app/271590/': {'inum': 37, 'prev_url': 'https://store.steampowered.com/news/collection/steam/'}, 'https://store.steampowered.com/login/': {'inum': 34, 'prev_url': 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/'}, 'https://store.steampowered.com/labs/': {'inum': 98, 'prev_url': 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/'}, 'https://store.steampowered.com/sale/winter2020_coop': {'inum': 186, 'prev_url': 'https://store.steampowered.com/labs/'}, 'https://store.steampowered.com/sale/winter2020_VR': {'inum': 187, 'prev_url': 'https://store.steampowered.com/sale/winter2020_coop'}, 'https://store.steampowered.com/points/shop': {'inum': 87, 'prev_url': 'https://store.steampowered.com/agecheck/app/1245620/'}, 'https://store.steampowered.com/points/shop/c/emoticons': {'inum': 74, 'prev_url': 'https://store.steampowered.com/points/shop'}, 'https://store.steampowered.com/points/shop/c/backgrounds': {'inum': 71, 'prev_url': 'https://store.steampowered.com/points/shop/c/emoticons'}, 'https://store.steampowered.com/points/shop/c/keyboard': {'inum': 70, 'prev_url': 'https://store.steampowered.com/points/shop/c/backgrounds'}, 'https://store.steampowered.com/points/shop/c/itembundles': {'inum': 76, 'prev_url': 'https://store.steampowered.com/points/shop/c/keyboard'}, 'https://store.steampowered.com/points/shop/c/profilebundles': {'inum': 82, 'prev_url': 'https://store.steampowered.com/points/shop/c/itembundles'}, 'https://store.steampowered.com/points/shop/c/profilebundles/cluster/0': {'inum': 77, 'prev_url': 'https://store.steampowered.com/points/shop/c/profilebundles'}, 'https://store.steampowered.com/points/shop/c/artistprofiles': {'inum': 73, 'prev_url': 'https://store.steampowered.com/points/shop/c/profilebundles/cluster/0'}, 'https://store.steampowered.com/points/shop/c/avatar': {'inum': 36, 'prev_url': 'https://store.steampowered.com/points/shop/c/artistprofiles'}, 'https://store.steampowered.com/agecheck/app/252490/': {'inum': 161, 'prev_url': 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/'}, 'https://store.steampowered.com/join/': {'inum': 36, 'prev_url': 'https://store.steampowered.com/agecheck/app/391220/'}, 'https://store.steampowered.com/app/1426210/It_Takes_Two/': {'inum': 34, 'prev_url': 'https://store.steampowered.com/join/'}, 'https://store.steampowered.com/app/353380/Steam_Link/': {'inum': 159, 'prev_url': 'https://store.steampowered.com/app/1426210/It_Takes_Two/'}, 'https://store.steampowered.com/points/howitworks': {'inum': 34, 'prev_url': 'https://store.steampowered.com/app/353380/Steam_Link/'}, 'https://store.steampowered.com/app/1332010/Stray/': {'inum': 177, 'prev_url': 'https://store.steampowered.com/points/howitworks'}, 'https://store.steampowered.com/tags/en/Exploration/': {'inum': 186, 'prev_url': 'https://store.steampowered.com/app/1332010/Stray/'}, 'https://store.steampowered.com/app/794260/Outward_Definitive_Edition/': {'inum': 269, 'prev_url': 'https://store.steampowered.com/tags/en/Exploration/'}, 'https://store.steampowered.com/agecheck/app/1245620/': {'inum': 159, 'prev_url': 'https://store.steampowered.com/app/794260/Outward_Definitive_Edition/'}, 'https://store.steampowered.com/points/shop/app/1880140': {'inum': 82, 'prev_url': 'https://store.steampowered.com/agecheck/app/1245620/'}, 'https://store.steampowered.com/': {'inum': 272, 'prev_url': 'https://store.steampowered.com/points/shop/app/1880140'}, 'https://store.steampowered.com/app/1371720/Card_Shark/': {'inum': 279, 'prev_url': 'https://store.steampowered.com/'}, 'https://store.steampowered.com/app/1965410/Rolando_The_Majestic/': {'inum': 220, 'prev_url': 'https://store.steampowered.com/app/1371720/Card_Shark/'}, 'https://store.steampowered.com/agecheck/app/391220/': {'inum': 165, 'prev_url': 'https://store.steampowered.com/app/1965410/Rolando_The_Majestic/'}, 'https://store.steampowered.com/app/1628580/HTC_VIVE_Pro_2/': {'inum': 184, 'prev_url': 'https://store.steampowered.com/agecheck/app/391220/'}}




def start():

	pages_crawled = 0
	chrome_options = Options()
	chrome_options.add_extension('C:/Users/ahmed/OneDrive/Bureau/liquidrain/scraperext.crx')
	driver = webdriver.Chrome("c:/users/ahmed/onedrive/bureau/chromedriver", chrome_options=chrome_options)
	base_url = random.choice(starting_sites)

	nodes = {}
	nodes[base_url] = "base url"
	driver.get(base_url)
					

	i = 0
	while pages_crawled <= pages_to_crawl:
		driver_len = len(driver.window_handles)
		if len(driver.window_handles) > 1:
			for i in range(driver_len - 1, 0, -1):
				driver.switch_to.window(driver.window_handles[i]) #will close the last tab first.
				driver.close()

			driver.switch_to.window(driver.window_handles[0])

		x = driver.find_elements(By.XPATH, "//a[@href]")
		if not x:
			url = nodes.keys()[-1]
			i = nodes[url]["inum"] + 1
			driver.get(url)
			
		
		else:
			try:
				prev_url = driver.current_url
				if i >= len(x):
					url = nodes.keys()[-1]
					i = nodes[url]["inum"]
					driver.get(url)
					
				
				next_url = x[i].get_attribute("href") 
				if ("http" in next_url) and ("store.steampowered.com" in next_url):
					if (next_url.split("?")[0] in blocked_urls) or (next_url in nodes.keys()):
						print(f"{next_url} is blocked or already crawled")
						raise Exception()

					x[i].click()
					print("click successful on x[i] = {}, i = {}".format(i, x[i]))
					if driver.current_url.split("?")[0] == prev_url.split("?")[0]:
						print("url sent us back to previous page : " + driver.current_url)
						raise Exception()

				else:
					print("url rejected")
					raise Exception()
					


			except Exception as ex:

				i = random.randint(0, len(x))

			else:

				nodes[prev_url.split("?")[0]] = {"inum": i, "prev_url": list(nodes)[-1] }


				print(nodes)
				if driver.current_url.split("?")[0] in nodes.keys():
					i = nodes[driver.current_url.split("?")[0]]["inum"] + 1 
					print("{} already crawled before pulling inum : {}".format(driver.current_url, i) )
				else:
					print('url not crawled before i = 0')
					i = 0
				pages_crawled += 1



if __name__ == '__main__':
	start()
