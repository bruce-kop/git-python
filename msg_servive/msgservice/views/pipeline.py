#encoding=utf8

def make_pipeline(**kwargs):
    pageIndex = 'pageIndex' in kwargs and kwargs['pageIndex'] or None
    pageSize = 'pageSize' in kwargs and kwargs['pageSize'] or None
    match = 'match' in kwargs and kwargs['match'] or None
    document = 'document' in kwargs and kwargs['document'] or None


    if not match or not pageSize or not pageIndex or not document:
        return None

    pipeline = [
        {
            '$lookup':
                {
                    'from': document,
                    'localField': 'msg_id',
                    'foreignField': 'id',
                    'as': 's_msg_id'
                },
        },
        {
            '$replaceRoot':
                {
                    'newRoot':
                        {
                            '$mergeObjects': [
                                {
                                    '$arrayElemAt':
                                        ["$s_msg_id", 0]
                                }, "$$ROOT"
                            ]
                        }
                }
        },

        {
            '$facet':
                {
                    "total": [
                        {
                            '$match': match,

                        },
                        {"$count": "total"}
                    ],
                    'data':[
                        {
                            '$project':
                                {
                                    's_msg_id': 0,
                                    '_id': 0,
                                    'msg_id':0
                                }
                        },
                        {
                            '$match': match,

                        },
                        {
                            "$skip": (pageIndex - 1) * pageSize
                        },
                        {
                            "$limit": pageSize
                        },
                        {
                            '$sort':
                                {
                                    'created_at': 1
                                }
                        },
                    ]
                }
        }

    ]

    return pipeline

def CommandCursor_to_list(results):
    result_list = [result for result in results]
    print(result_list)
    totalCount = 0
    if len(result_list) > 0:
        if len(result_list[0]['total']) > 0:
            totalCount = result_list[0]['total'][0].get('total')
        msg_list = result_list[0]['data']

        return totalCount,msg_list
    else:
        return 0,[]

def make_pipeline2(**kwargs):
    pageIndex = 'pageIndex' in kwargs and kwargs['pageIndex'] or None
    pageSize = 'pageSize' in kwargs and kwargs['pageSize'] or None
    match = 'match' in kwargs and kwargs['match'] or None
    document = 'document' in kwargs and kwargs['document'] or None


    if not match or not pageSize or not pageIndex or not document:
        return None

    pipeline = [
        {
            '$lookup':
                {
                    'from': document,
                    'localField': 'msg_id',
                    'foreignField': 'id',
                    'as': 's_msg_id'
                },
        },
        {
            '$replaceRoot':
                {
                    'newRoot':
                        {
                            '$mergeObjects': [
                                {
                                    '$arrayElemAt':
                                        ["$s_msg_id", 0]
                                }, "$$ROOT"
                            ]
                        }
                }
        },

        {
            '$facet':
                {
                    "total": [
                        {
                            '$match': match,

                        },
                        {"$count": "total"}
                    ],
                    'data':[
                        {
                            '$project':
                                {
                                    's_msg_id': 0,
                                    '_id': 0,
                                    'msg_id':0
                                }
                        },
                        {
                            '$match': match,

                        },
                        {
                            "$skip": (pageIndex - 1) * pageSize
                        },
                        {
                            "$limit": pageSize
                        },
                        {
                            '$sort':
                                {
                                    'created_at': 1
                                }
                        },
                    ]
                }
        }

    ]

    return pipeline


