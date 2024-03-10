from flask import Flask, request
import logging
import gitlabsqlite
import gitlabUtils
import slackWrapper
import os

TEST_PROJECT_ID = 55706687
NEW_MR_EXPIRE_MINUTES = 1
PORT_NUMBER = 8080
CONTEXT_PATH = "/slackbot"

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route(CONTEXT_PATH, methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
    except:
        return

    if data["object_kind"] == "merge_request":
        print(data)
        project = data["project"]
        projId = project["id"]
        print(projId)
        attrs = data["object_attributes"]
        mergeId = attrs["iid"]
        created_at = attrs["created_at"]

        if gitlabUtils.apiTimeStrMalformed(created_at):
            # if the data comes in the form of malformed ISO from gitlab api, format it correctly..
            created_at = gitlabUtils.apiTimeStrToIso((created_at))

        mergeExistsInDb = gitlabsqlite.mergeRequestExists(mergeId)
        deltaTime = gitlabUtils.getDeltaIsoMinutes(created_at)

        if not mergeExistsInDb:
            mrIsOld = deltaTime > NEW_MR_EXPIRE_MINUTES
            if mrIsOld:
                # we detected an MR considered old, but we haven't logged it. add to db
                gitlabsqlite.insertMergeRequest(mergeId, projId)
            else:
                # we detected a new MR! add it to db and send a chat message.
                gitlabsqlite.insertMergeRequest(mergeId, projId)

                title = attrs["title"]
                author_username = data["user"]["username"]
                url = attrs["url"]

                message = "Merge Request Created By " + author_username + '\n' + title + '\n' + url
                slackWrapper.sendMessage(message)
    return 1


if __name__ == '__main__':
    app.run(port=PORT_NUMBER)