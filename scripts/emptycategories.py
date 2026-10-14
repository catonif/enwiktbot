import pywikibot
import sys

site = pywikibot.Site("en", "wiktionary")
site.login()

cat_d = pywikibot.Category(site, 'Candidates for speedy deletion')

print("----")

for empty_cat in cat_d.subcategories():
	title = empty_cat.title()
	if empty_cat.isEmptyCategory():
		print(f"Empty category {title} was marked for speedy deletion.")
		accept = input("Delete? [Yes/No/Quit] ")
		if accept == 'y':
			empty_cat.delete('Empty category')
		elif accept == 'n':
			continue
		elif accept == 'q':
			sys.exit(0)
		print("----")
	else:
		print(f"Category {title} is not empty, skipping for now.")
