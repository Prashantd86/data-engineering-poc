print(">>> RUNNING test0.py <<<")


def get_posts_count():
    import requests

    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    data = response.json()
    return len(data)

def lambda_handler(event, context):
    count = get_posts_count()

    print("Number of posts:", count)

    return {
        "statusCode": 200,
        "record_count": count
    }
    
if __name__ == "__main__":
    result = lambda_handler({}, {})
    print(result) 