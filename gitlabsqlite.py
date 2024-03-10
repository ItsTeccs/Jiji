import sqlite3
import gitlab
import datetime
import json

FILENAME = "database.db"
TOKEN = "glpat-FJGNRUxy8LE4_2xxG_Er"
def init():
    # Connect to the database (create it if it doesn't exist)
    conn = sqlite3.connect(FILENAME)

    # Create a cursor object
    cursor = conn.cursor()

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS projects
                          (id INTEGER PRIMARY KEY, json TEXT)''')

    # Create a table
    cursor.execute('''CREATE TABLE IF NOT EXISTS merge_requests
                      (mergeId INTEGER PRIMARY KEY, projectId INTEGER, jsonStr TEXT)''')

    conn.commit()
    conn.close()


def insertMergeRequest(mergeId, projectId):
    with gitlab.Gitlab(private_token=TOKEN) as gl:
        proj = gl.projects.get(id=projectId)
        mr = proj.mergerequests.get(mergeId, lazy=True)

    jsonStr = mr.to_json()

    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()

    success = False
    with conn:
        try:
            cursor.execute("INSERT INTO merge_requests(mergeId, projectId, jsonStr) VALUES (?, ?, ?)", (mergeId, projectId, jsonStr))
            success = True
        except sqlite3.IntegrityError:
            print("ERROR: Record already exists. Data: ", end="")
        # Commit the changes
    conn.close()
    return success


def getMergeRequest(mergeId):
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    with conn:
        cursor.execute("SELECT * FROM merge_requests WHERE mergeId = ?", (mergeId,))
    row = cursor.fetchone()
    if bool(row):
        conn.close()
        return json.loads(json.loads(row[2]))  # why?
    else:
        conn.close()
        return None


def mergeRequestExists(mergeId):
    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    with conn:
        cursor.execute("SELECT * FROM merge_requests WHERE mergeId = ?", (mergeId,))
    row = cursor.fetchone()
    conn.close()
    return bool(row)


def parseOpenMergeRequests(projectId):
    with gitlab.Gitlab(private_token=TOKEN) as gl:
        proj = gl.projects.get(id=projectId, lazy=True)
        mrs = proj.mergerequests.list(state="opened", scope="all")

    for mr in mrs:
        jsonStr = json.dumps(mr.to_json())
        projectId = mr.project_id
        mergeId = mr.id
        insertMergeRequest(mergeId, projectId)


def insertProject(projectId):
    with gitlab.Gitlab(private_token=TOKEN) as gl:
        proj = gl.projects.get(id=projectId)
        jsonStr = proj.to_json()

    conn = sqlite3.connect(FILENAME)
    cursor = conn.cursor()
    with conn:
        try:
            cursor.execute("INSERT INTO projects(projectId, jsonStr) VALUES (?, ?)",
                           (projectId, jsonStr))
        except sqlite3.IntegrityError:
            print("ERROR: Record already exists. Data: ", end="")
        # Commit the changes
    conn.close()
    pass

init()