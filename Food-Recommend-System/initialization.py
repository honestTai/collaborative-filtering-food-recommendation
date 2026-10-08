import runpy

runpy.run_path("FoodRecommend/get_data/spider.py")
runpy.run_path("clean.py")
runpy.run_path("csvtosql.py")
runpy.run_path("analysis.py")
