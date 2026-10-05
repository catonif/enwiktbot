import pywikibot
import sys
import json

site = pywikibot.Site("en", "wiktionary")
site.login()

action_path = sys.argv[1]

print("Loading action", action_path)
print("====")

with open(action_path, "r") as action_file:
	action = json.load(action_file)

pagetitle = action['pagetitle']
editsummary = action['editsummary']
substitutions = action['substitutions']

page = pywikibot.Page(site, pagetitle)

for ref_page in page.backlinks():
	namespace = ref_page.namespace()
	if namespace == '' or namespace == 'Reconstruction':
		og_text = ref_page.text
		out_text = og_text
		for str_from, str_to in substitutions:
			out_text = out_text.replace(str_from, str_to)
		if og_text != out_text:
			print("[TITLE]", ref_page.title())
			print("----")
			og_lines = og_text.splitlines()
			out_lines = out_text.splitlines()
			for line_index, og_line in enumerate(og_lines):
				out_line = out_lines[line_index]
				if out_line != og_line:
					print("[OLD]", og_line)
					print("[NEW]", out_line)
					print("----")
			accept = input("Do you agree with the changes? [Yes/No/Quit] ")
			if accept == 'y':
				ref_page.text = out_text
				ref_page.save(summary=editsummary)
				print("Change done!")
			elif accept == 'n':
				continue
			elif accept == 'q':
				sys.exit(0)
			print("====")
		else:
			# Null-edit.
			ref_page.touch()
