#encoding = utf8

def query_res_to_dict_list(query_res):
    datas = list()
    descripsions = query_res.column_descriptions
    for u in query_res:
        f = {}
        for key in descripsions:
            f.update({key['name']:getattr(u,key['name'])})
        datas.append(f)
    return datas

def query_res_to_dict(obj):
    descripsions = obj.column_descriptions
    obj_1 = obj.first()
    data = {}
    for key in descripsions:
        data.update({key['name']:getattr(obj_1,key['name'])})
    return data