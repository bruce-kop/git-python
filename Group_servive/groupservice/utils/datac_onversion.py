#encoding = utf8

def query_res_to_dict(query_res):
    friends = list()
    descripsions = query_res.column_descriptions
    for u in query_res:
        f = {}
        for key in descripsions:
            f.update({key['name']:getattr(u,key['name'])})
        friends.append(f)
    return friends