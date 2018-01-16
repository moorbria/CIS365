import os, json
from shutil import copyfile
import pandas as pd

path_to_json = '/home/mooreb0314/GitRepos/CIS365/Projects/Project1/MLBot/testingshere/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if not pos_json.endswith('.zip')]
print(json_files)  # for me this prints ['foo.json']

for index, js in enumerate(json_files):
	with open(os.path.join(path_to_json, js)) as json_file:
		json_text = json.load(json_file)
		player_pos = 0
	
		for pos, name in enumerate(json_text['player_names']):
			if "FakePsyho" in name:
				json_text['player_names'] = "FakePsyho"
				print(str(pos) + " : " + name)
				player_pos = pos
							
	
		
		if json_text['stats'][str(player_pos)]['rank'] is 1:
			print(json_text['stats'][str(player_pos)]['rank'])
			print("win")
			with open("/home/mooreb0314/GitRepos/CIS365/Projects/Project1/MLBot/4355_20180101/" + js, "w") as text_file:
				text_file.write(json.dumps(json_text))
				text_file.close()
