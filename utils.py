import collections

#block = {'b': 2, 'a': 1}
#block2 = {'a':1, 'b':2}

def sorted_dict_by_key(unsorted_dict):
	return collections.OrderedDict(
		sorted(unsorted_dict.items()), key=lambda d:d[0])

def pprint(chains):
	for i, chain in enumerate(chains):
		print(f'{"="*25} Chain {i}{"="*25}')
		for k, v in chain.items():
			if k == 'transantions':
				print(k)
				for d in v:
					print(f'{"-"*40}')
					for kk, vv in d.items():
						print(f'{kk:30}{vv:}')
			else:
				print(f'{k:15}{v}')
	print(f'{"*"*25}')


#print(hashlib.sha256("test".encode()).hexdigest)
#print(hashlib.sha256("test".encode()).hexdigest)
#print(hashlib.sha256("test2".encode()).hexdigest)
#print(hashlib.sha256("test2".encode()).hexdigest)


