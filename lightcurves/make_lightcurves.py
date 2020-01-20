import os, sys
import io
import fastavro
import json
import time

# Code to read in a lot of ZTF avro files, extract the parts that are not binary images,
# and save the results as JSON files.

# this is the directory with the night directories, which contain the avros
avros = '/data/ztf/avros/'

# the directory for the output JSON files
light_curves = '/data/ztf/light_curves'

def msg_text(message):
# Remove postage stamp cutouts from an alert message.
    message_text = {k: message[k] for k in message
                    if k not in ['cutoutDifference', 'cutoutTemplate', 'cutoutScience']}
    return message_text

def get_lightcurve(message, debug=False):
# Takes the binary read in from a avro file, and returns dictionaries 
# that have everything except the images
    bytes_io = io.BytesIO(message)
    bytes_io.seek(0)
    decoded_msg = fastavro.reader(bytes_io)

    alerts = []
    nalert = 0
# in general each avro message can have multiple alerts, though this does not 
# seem to happen in practice
    for full_alert in decoded_msg:
        nalert += 1

# where we cut out the images
        alert = msg_text(full_alert)
        alerts.append(alert)

# write out the light curve if wanted
        if debug:
            c = alert['candidate']
            print('candidate %.3f %.3f' % (c['jd'], c['magpsf']))
            for c in alert['prv_candidates']:
# if the previous candidate does not have a magnitude it is a non-detection record
# which goes into the JSON output file but is not written out in this dump
                if c['magpsf']:
                    print('prv_candidate %.3f %.3f' % (c['jd'], c['magpsf']))
# does not seem to happen
    if nalert > 1: print('Number of alerts=', nalert)
    return alerts


def get_night_lightcurves(night):   
    start = time.time()
    nfiles = 0
    jd_dict = {}
    night_dir = avros + '/' + night
    for candidate in sorted(os.listdir(night_dir)):
        candidate_file = night_dir + '/' + candidate
        avro_message = open(candidate_file, 'rb').read()
        alerts = get_lightcurve(avro_message)
        for alert in alerts:
            jd = alert['candidate']['jd']
            objectId = alert['objectId']

            if objectId in jd_dict and jd_dict['objectId'] > jd:
                print('%s newer exists by %.3f' % (objectId, jd_dict['objectId'] - jd))

            if not objectId in jd_dict or jd_dict['objectId'] < jd:
                outfile = open(light_curves + '/' + objectId + '.json', 'w')
                outfile.write(json.dumps(alert, indent=2))
                jd_dict['objectId'] = jd
        nfiles += 1
    print ('%s: processed %d files %.1f seconds' % (night, nfiles, time.time()-start))
    return

def main():
    if len(sys.argv) > 1:
        # do a specific night, for example ztf_20190923_programid1
        night = sys.argv[1]
        get_night_lightcurves(night)
    else:
        # do all nights
        for night in sorted(os.listdir(avros)):
            get_night_lightcurves(night)

if __name__ == "__main__":
    main()
