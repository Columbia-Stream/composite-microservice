from utils.db import get_db_connection

def search_videos(q=None, offering_id=None, prof=None, limit=20):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM Videos WHERE 1=1"
    params = []

    # Filters
    if q:
        query += " AND title LIKE %s"
        params.append(f"%{q}%")
    if offering_id:
        query += " AND offering_id = %s"
        params.append(offering_id)
    if prof:
        query += " AND prof_uni LIKE %s"
        params.append(f"%{prof}%")

    query += " LIMIT %s"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()

    for r in rows:
        r["signed_url"] = None

    cursor.close()
    conn.close()

    return rows
'''
# Skipping GCS for now
    # generate signed URLs
    storage_client = storage.Client()
    bucket = storage_client.bucket(os.getenv("GCS_BUCKET_NAME"))

    for r in rows:
        blob = bucket.blob(r["gcs_path"])
        r["signed_url"] = blob.generate_signed_url(expiration=timedelta(minutes=10))
    return rows
'''


