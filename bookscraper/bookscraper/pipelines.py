# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'one' in adapter.get('rating'):
            adapter['rating'] = 1
        elif 'two' in adapter.get('rating'):
            adapter['rating'] = 2
        elif 'three' in adapter.get('rating'):
            adapter['rating'] = 3
        elif 'four' in adapter.get('rating'):
            adapter['rating'] = 4
        elif 'five' in adapter.get('rating'):
            adapter['rating'] = 5
        
        return item
