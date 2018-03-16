from flask import Flask, request, render_template
from werkzeug.contrib.cache import SimpleCache
import json
import dribbble_util
import util
import itertools
from celery import group
import tasks
import settings
app = Flask(__name__)
app.config.from_object(settings)

cache = SimpleCache()

WEBSITE = dribbble_util.WEBSITE


@app.route('/')
def main():
    return render_template('index.html')


# @cache.cached(timeout=3600, key_prefix='search')
@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('q')
    limit = request.args.get('limit')
    if limit and limit.isdigit():
        limit = int(limit)
    else:
        limit = 60
    if len(keyword) == 0:
        return json.dumps({
            "results": [],
            "palette": [],
            "cluster": []
        })
    rv = cache.get(keyword + str(limit))
    if rv is None:
        # Fetch Search Results
        results, images = dribbble_util.search(keyword, limit)

        # Fetch Shots (parallel with celery)
        jobs = [tasks.request.s(WEBSITE + result["path"]) for  result in results]
        job = group(jobs)()
        palette = job.get()
        chain = itertools.chain(*palette)
        palette = list(chain)
        palette.sort(key=util.get_hsv)

        cluster = dribbble_util.cluster(palette)

        rv = json.dumps({
            "results": results,
            "palette": palette,
            "cluster": cluster,
            "images": images
        })
        cache.set(keyword + str(limit), rv, timeout=5 * 60)
    return rv

# if __name__ == '__main__':
#     app.run(debug=True)
