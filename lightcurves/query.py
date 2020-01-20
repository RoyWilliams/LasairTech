import sys
import settings
import mysql.connector
import requests
import json
import time
# program to check a lot of lightcurves around a specific time 'critical_jd'
# looking for a strong brightness increase

# checks a specific object for a detection before and after the critical_jd
def check(objectId, critical_jd, use_url):
    # open the file
    if use_url == 1:
        url = 'https://lasair-dev.roe.ac.uk/lasair/static/ztf/light_curves/%s.json'  % objectId
        response = requests.get(url)
        try:
            obj = json.loads(response.content)
        except:
            return None
    else:
        filename = '/data/ztf/light_curves/%s.json'  % objectId
        try:
            obj = json.loads(open(filename).read())
        except:
            return None

    # the latest detection
    nowc = obj['candidate']

    # filter for latest detection
    fid = nowc['fid']

    # accumulate light curve. They come in time order.
    m = []
    for c in obj['prv_candidates']:
        if c['magpsf'] and c['fid'] == fid:
            m.append((c['jd'], c['magpsf']))
    if c['magpsf']:
        m.append((c['jd'], c['magpsf']))

    # find a point before and a point after the critical jd
    jd0 = mag0 = -1
    for (jd1, mag1) in m:
        if jd0 > 0 and jd0 < critical_jd and jd1 > critical_jd:
            return({'fid':fid, 'jd0':jd0, 'jd1':jd1, 'mag0':mag0, 'mag1':mag1})
        jd0  = jd1
        mag0 = mag1
    return None

def run_query(critical_jd, use_url):
    config = {
        'user'    : settings.DB_USER,
        'password': settings.DB_PASS,
        'host'    : settings.DB_HOST,
        'database': settings.DB_DATABASE
    }
    msl = mysql.connector.connect(**config)
    cursor  = msl.cursor(buffered=True, dictionary=True)
    
# a query to find all objects in a 5x5 degree square of sky
    query = """
SELECT objects.objectId FROM objects
WHERE
objects.ramean between 60 and 65
and objects.decmean between 5 and 10
and objects.jdmin < %f
"""

    # find objects with a start time before the critical jd
    start = time.time()
    query = query % critical_jd
    cursor.execute(query)
    print('SQL query executed in %.1f seconds' % (time.time()-start))

    start = time.time()
    ncheck = 0
    for row in cursor:
        objectId = row['objectId']
        r = check(objectId, critical_jd, use_url)
        if r:
            # increasing brightness is decreasing magnitude
            mags_per_day = (r['mag0'] - r['mag1'])/(r['jd1'] - r['jd0'])
            if mags_per_day > 0.2:
                print('object %s filter %d brightens %.2f mags per day' 
                    % (objectId, r['fid'], mags_per_day))
        ncheck += 1
    print('%d objects checked in %.1f seconds' % (ncheck, time.time()-start))

use_url = 0
if len(sys.argv) > 1:
    use_url = int(sys.argv[1])
# here is the critical jd
critical_jd = 2458734.5
run_query(critical_jd, use_url)
    
