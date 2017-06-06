import tabload.search
import tabload.formats.text

s = tabload.search.search("d")
r = s.__next__()
r.load()
print(tabload.formats.text.generate(r))

#for r in tabload.search.search("e"):
#	print(r)

# s = tabload.services.ukutabs.Search("e")
# for a in s:
# 	print(a)
# 	a.load()
# 	break



#import tabload.Search
#s = tabload.Search.Search("test")
#for i in s:#
#	print(i)


#import tabload.services.ukutabs.Service
#s = tabload.services.ukutabs.Service.UkuTabs()
#s.search("blank")
