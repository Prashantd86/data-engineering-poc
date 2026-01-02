def get_posts():
    import requests

    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    return data
print("Fetching posts...")
posts = get_posts()
print("Number of posts:", len(posts))
print("First post title:", posts[1]["title"])
