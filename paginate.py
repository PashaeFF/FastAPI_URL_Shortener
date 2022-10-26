def paginate(data, data_length, page_num,page_size):

    {
        "data": [...],
        "pagination": {
            "next":"link to next page",
            "previous":"link to the previous page"
        },
        "count":"total number of items",
        "total":"total number of items"
    }
    start = (page_num - 1) * page_size
    end = start + page_size

    response = {
        "data": data[start:end],
        "total": data_length,
        "count": page_size,
        "pagination": {}
    }

    if end >= data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"/?page_num{page_num - 1}&page_size = {page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"/?page_num{page_num - 1}&page_size = {page_size}"
        else:
            response["pagination"]["previous"] = None
        response["pagination"]["next"] = f"/?page_num{page_num + 1}&page_size = {page_size}"

    return response
            
