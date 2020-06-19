    if request.method == 'POST':
        if request.form['keyword']:
            sbin =  request.form['keyword']
            data = (requests.get(f"https://www.googleapis.com/books/v1/volumes?q=isbn:{sbin}")).json()
            context = {
                "name" : data["items"][0]["volumeInfo"]["title"],
                "writer" : data["items"][0]["volumeInfo"]["authors"][0],
                "publication" : data["items"][0]["volumeInfo"]["publishedDate"],
                "description" : data["items"][0]["volumeInfo"]["description"]
                }