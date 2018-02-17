import os, json
from shutil import copyfile
import pandas as pd

path_to_json = '/home/mooreb0314/GitRepos/CIS365/Projects/Project1/MLBot/replays/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if not pos_json.endswith('.zip')]
#print(json_files)  # for me this prints ['foo.json']
count = 0
for index, js in enumerate(json_files):
	with open(os.path.join(path_to_json, js)) as json_file:
		#print(str(js))
		json_text = json.load(json_file)
		player_pos = 0
		
		for pos, index in enumerate(json_text['player_names']):
			if 'FakePsyho' in json_text['player_names'][pos]:
				json_text['player_names'][pos] = 'FakePsyho' 
				print("index: " + str(count) + " | Player: " + json_text['player_names'][pos] + " | Players: " + str(len(json_text['player_names'])))
				count += 1

	
		#for pos, index in enumerate(json_text['stats']):
		#	if json_text['stats'][str(pos)]['rank'] is 1:
		#		player_pos = pos
		#json_text['player_names'][player_pos] = "Winner_v1"
				player_count = len(json_text['player_names'])
		count_folder = str(player_count)
		#print("/home/mooreb0314/GitRepos/CIS365/Projects/Project1/MLBot/all_recent/" + count_folder + "s/" + map_size_folder + "/")
		with open("/home/mooreb0314/GitRepos/CIS365/Projects/Project1/MLBot/all_recent/" + count_folder + "s/" + js, "w") as text_file:
			text_file.write(json.dumps(json_text))
			text_file.close()

