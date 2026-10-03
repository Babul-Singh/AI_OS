from duckduckgo_search import DDGS

def web_search(query):

    results_list = []

    with DDGS() as ddgs:

        results = ddgs.text(
            query,
            max_results=5
        )

        for result in results:

            results_list.append({

                "title": result["title"],

                "body": result["body"],

                "link": result["href"]
            })

    return results_list