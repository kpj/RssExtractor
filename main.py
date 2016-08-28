from flask import Flask, Response, request

from feed_parser import Feed


app = Flask(__name__)

@app.route('/')
def main():
    return 'Receive feed via <pre>{}rss/&lt;url&gt;</pre>'.format(request.url)

@app.route('/rss/<path:rss_url>')
def parse_rss(rss_url):
    xml =  Feed(rss_url).get_feed()
    return Response(xml, mimetype='text/xml')

if __name__ == '__main__':
    app.run()
