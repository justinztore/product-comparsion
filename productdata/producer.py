import sys

from productdata.tasks import crawler

def update(dataset):

    if dataset == "watsons_category" :
        print(f"starting run {dataset}")
        task = crawler.s(dataset, '')
        task.apply_async()

if __name__ == "__main__":
    (
        dataset,
    ) = sys.argv[1:]
    
    update(dataset)