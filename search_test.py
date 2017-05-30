import tabload.services.ukutabs

s = tabload.services.ukutabs.Search("d")
for a in s:
	print(a)
	a.load()
	break



#import tabload.Search
#s = tabload.Search.Search("test")
#for i in s:#
#	print(i)


#import tabload.services.ukutabs.Service
#s = tabload.services.ukutabs.Service.UkuTabs()
#s.search("blank")
