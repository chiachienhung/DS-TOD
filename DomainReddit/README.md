# DomainReddit 

`DomainReddit` is the dataset created for intermediate training purpose. 
It is currently shared under [here](https://drive.google.com/drive/folders/1mHQVjwawehL4OxbKzifbztXzVuB_I3_h?usp=sharing).
Feel free to download and unzip to use it.

If you would like to crawl your own Reddit dataset from [Pushshift API](https://github.com/pushshift/api), 
the scripts in this folder can be modified for your own usage.

For crawling the raw data from Reddit:
```
python crawl_reddit_domain.py --input_query="restaurant|food|type|reservation|cuisine" --subreddit="travel" --after="01/01/2015" --before="31/12/2019" --domain="restaurant" --save_file_name="food_travel_01012015_31122019.json"
```

For further preprocessing:
```
python prep_reddit.py --domain="restaurant" --subreddit="travel" --save_file_name="restaurant_01012015_31122019.json"
```

For constructing context-response pair:
```
python concat_reddit.py --domain="restaurant"
```

For constructing context-response pair in contrastive loss learning format:
```
python concat_reddit_ir.py --domain="restaurant"
```