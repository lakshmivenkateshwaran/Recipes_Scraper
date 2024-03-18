from fastapi import FastAPI, HTTPException
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher
from spiders.receipes_spider_snacks import RecipesSpider as snacks_spider
from spiders.receipes_spider_mushroom import RecipesSpider as mushroom_spider 
import json

app = FastAPI()

def crawl_and_return_results(spider_cls, output_file):
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(dict(item))

    dispatcher.connect(crawler_results, signal=signals.item_scraped)
    
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    
    try:
        process.crawl(spider_cls)
        process.start()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error while scraping: {str(e)}")

    # Creating the JSON structure with the scraped data
    json_data = {
        "code": 200,
        "status": "success",
        "Message": "Successful",
        "recipe_data": results,
        "recipe_count": len(results)
    }

    # Save JSON data to the specified output file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False, indent=4)

    return json_data

# Endpoint to scrape Snacks data
@app.get("/scrape")
def scrape():
    try:
        return crawl_and_return_results(snacks_spider, 'final_snacks_recipes.json')
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

# Endpoint to scrape Mushroom data
@app.get("/scrape/mushroom")
def scrape_mushroom():
    return crawl_and_return_results(mushroom_spider, 'final_mushroom_recipes.json')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
