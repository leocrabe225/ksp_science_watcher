import tkinter
import json
import re

BODIES = "bodies"
INFLUENCES = "influences"
BIOMES = "biomes"
ID="id"
TITLE="title"
COLLECTED_SCIENCE="collectedScience"
MAX_SCIENCE="maxScience"
MULTIPLIERS="multipliers"
SURFACE_LANDED="Surface: Landed"
SURFACE_SPLASHED="Surface: Splashed"
FLYING_LOW="Flying Low"
FLYING_HIGH="Flying High"
IN_SPACE_LOW="In Space Low"
IN_SPACE_HIGH="In Space High"

def extract_science_data(filename):
	with open(filename, 'r', encoding='utf-8') as file:
		data = file.read()

	# Find the ResearchAndDevelopment scenario
	rnd_match = re.search(r'SCENARIO\s*{\s*name\s*=\s*ResearchAndDevelopment(.*?)SCENARIO', data, re.DOTALL)
	if not rnd_match:
		print("ResearchAndDevelopment scenario not found.")
		return []

	rnd_block = rnd_match.group(1)

	# Find all Science entries within the ResearchAndDevelopment block
	science_entries = re.findall(r'Science\s*{(.*?)}', rnd_block, re.DOTALL)

	science_data = []
	for entry in science_entries:
		splitEntry = entry.split("\n")
		newDict = {
			ID:splitEntry[1].split("=")[1].strip(),
			TITLE:splitEntry[2].split("=")[1].strip(),
			COLLECTED_SCIENCE:float(splitEntry[6].split("=")[1]),
			MAX_SCIENCE:float(splitEntry[8].split("=")[1])
		}
		science_data.append(newDict)

	#The following code uses RE to parse the SCIENCE fields, but as I am in no way capable of editing it, it will stay commented, and I will make my ugly parser instead
	'''for entry in science_entries:
		sci_match = re.search(r'id\s*=\s*(.*?)\s*title\s*=\s*(.*?)\s*sci\s*=\s*(.*?)\s', entry, re.DOTALL)
		if sci_match:
			science_data.append({
				'id': sci_match.group(1).strip(),
				'title': sci_match.group(2).strip().split("\n")[0],
				'science_points': float(sci_match.group(3).strip())
			})'''

	return science_data

def load_json():
	try:
		with open("bodies_biomes.json", "r") as file:
			data = json.load(file)
		return data
	except Exception as e:
		print(f"Error loading JSON: {e}")
		return {}

def GetBodiesRecursively(data: dict) -> list:
	bodies = {}
	for body in data.keys():
		bodies[body] = {BIOMES:data[body][BIOMES]}
		if (len(data[body][INFLUENCES]) != 0):
			bodies = {**bodies, **GetBodiesRecursively(data[body][INFLUENCES])}
	return bodies
	

def main():
	root = tkinter.Tk()
	root.title("Simple Tkinter Window")
	root.geometry("300x200")

	data = load_json()
	bodies = GetBodiesRecursively(data)

	with open("multipliers.csv", 'r', encoding='utf-8') as file:
		multipliers = file.read()
	splitMultipliers = multipliers.split("\n")
	del splitMultipliers[0]
	for multiplierLine in splitMultipliers:
		splitMultiplierLine = multiplierLine.split(",")
		bodies[splitMultiplierLine[0]][MULTIPLIERS] = {
			SURFACE_LANDED:splitMultiplierLine[1],
			SURFACE_SPLASHED:splitMultiplierLine[2],
			FLYING_LOW:splitMultiplierLine[3],
			FLYING_HIGH:splitMultiplierLine[4],
			IN_SPACE_LOW:splitMultiplierLine[5],
			IN_SPACE_HIGH:splitMultiplierLine[6],
		}
	
	for body in bodies.keys():
		print(body, "|||", bodies[body])

	science_results = extract_science_data("quicksave1.sfs")



	with open("experiments.csv", 'r', encoding='utf-8') as file:
		experiments = file.read()
	splitExperiments = experiments.split("\n")
	del splitExperiments[0]
	science_tree = {}
	for expe in splitExperiments:
		expeFields = expe.split(",")
		science_tree[expeFields[1]] = {}
		for body in bodies.keys():
			science_tree[expeFields[1]][body] = {}
		print(expe)
	print(science_tree)

	label = tkinter.Label(root, text="Hello, Tkinter!", font=("Arial", 14))
	label.pack(pady=20)

	button = tkinter.Button(root, text="Click Me", command=lambda: label.config(text="Button Clicked!"))
	button.pack()

	root.mainloop()

main()