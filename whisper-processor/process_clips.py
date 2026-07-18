import os
import sqlite3
import time
import requests
import subprocess
import tempfile
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger(__name__)

FRIGATE_URL = os.environ.get('FRIGATE_URL', 'http://frigate:5000')
WHISPER_URL = os.environ.get('WHISPER_URL', 'http://whisper:9000')
DB_PATH = os.environ.get('DB_PATH', '/data/transcripts.db')
POLL_INTERVAL = int(os.environ.get('POLL_INTERVAL', '300'))

def init_db(conn):
    conn.execute('''CREATE TABLE IF NOT EXISTS transcripts (
        event_id TEXT PRIMARY KEY,
        camera TEXT,
        timestamp INTEGER,
        label TEXT,
        transcript TEXT,
        created_at INTEGER
    )''')
    conn.commit()

def get_processed_ids(conn):
    return {r[0] for r in conn.execute('SELECT event_id FROM transcripts')}

def transcribe(audio_path):
    with open(audio_path, 'rb') as f:
        r = requests.post(
            f'{WHISPER_URL}/asr',
            params={'encode': 'true', 'task': 'transcribe', 'language': 'sl', 'output': 'json'},
            files={'audio_file': f},
            timeout=120
        )
    r.raise_for_status()
    data = r.json()
    return data.get('text', '').strip()

def process_event(event, conn):
    eid = event['id']
    camera = event['camera']
    timestamp = int(event.get('start_time', 0))
    label = event.get('label', '')

    log.info(f'Processing {eid} ({camera}, {label})')

    clip_url = f'{FRIGATE_URL}/api/events/{eid}/clip.mp4'
    r = requests.get(clip_url, timeout=60)
    if r.status_code != 200:
        log.warning(f'No clip for {eid}: {r.status_code}')
        return

    with tempfile.TemporaryDirectory() as tmp:
        mp4 = os.path.join(tmp, 'clip.mp4')
        wav = os.path.join(tmp, 'audio.wav')
        with open(mp4, 'wb') as f:
            f.write(r.content)

        result = subprocess.run(
            ['ffmpeg', '-y', '-i', mp4, '-vn', '-ar', '16000', '-ac', '1', wav],
            capture_output=True, timeout=60
        )
        if result.returncode != 0 or not os.path.exists(wav):
            log.warning(f'ffmpeg failed for {eid}')
            return

        try:
            transcript = transcribe(wav)
        except Exception as e:
            log.warning(f'Whisper failed for {eid}: {e}')
            return

    conn.execute(
        'INSERT OR REPLACE INTO transcripts VALUES (?,?,?,?,?,?)',
        (eid, camera, timestamp, label, transcript, int(time.time()))
    )
    conn.commit()
    log.info(f'Saved transcript for {eid}: {repr(transcript[:80])}')

def main():
    log.info('Whisper processor starting')
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    while True:
        try:
            r = requests.get(
                f'{FRIGATE_URL}/api/events',
                params={'limit': 100, 'has_clip': 1},
                timeout=15
            )
            r.raise_for_status()
            events = r.json()
            processed = get_processed_ids(conn)
            new_events = [e for e in events if e['id'] not in processed]
            log.info(f'Found {len(new_events)} new events to process')
            for event in new_events:
                try:
                    process_event(event, conn)
                except Exception as e:
                    log.error(f'Error processing {event[id]}: {e}')
        except Exception as e:
            log.error(f'Poll error: {e}')

        time.sleep(POLL_INTERVAL)

if __name__ == '__main__':
    main()
