
def request_url(url):
    import requests
    from datetime import datetime
    import codecs
    import logging

    r = requests.get(url)

    if r:
        msg = u'[{}][request_url] {} status code {}, length {}\n'.format(datetime.now().isoformat()[:19], url, r.status_code, len(r.content))
    else:
        msg = u'[{}][request_url] {} status code {}\n'.format(datetime.now().isoformat()[:19], url, r.status_code)

    logging.info(msg)

    filename_log = "/tmp/restful_scheduler.log"
    with codecs.open(filename_log, "a", encoding="utf-8") as f:
        f.write(msg)