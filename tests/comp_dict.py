def comp_dict(dict_1,dict_2):
    final = True
    #check keys
    keys_1 = list(dict_1.keys())
    keys_2 = list(dict_2.keys())
    if keys_1.sort() == keys_2.sort():
        for key in keys_1:
            if dict_1[key]==dict_2[key]:
                pass
            else:
                final = False
    else:
        final = False
    return final

dict_1 = {1:2,3:4,5:6}
dict