from flask import Flask, request
import logging
import gitlabsqlite
import gitlabUtils
import slackWrapper
TEST_PROJECT_ID = 55706687
NEW_MR_EXPIRE_MINUTES = 1

gitlabsqlite.parseOpenMergeRequests(TEST_PROJECT_ID)

# print(gitlabsqlite.mergeRequestExists(287648705))
# data = gitlabsqlite.getMergeRequest(287648705)

#print(data)
#print(gitlabUtils.getDeltaIsoMinutes(data["created_at"]))

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/slackbot', methods=['POST'])
def receive_data():
    try:
        data = request.get_json()
        # print(data)
    except:
        return

    if data["object_kind"] == "merge_request":
        project = data["project"]
        projId = project["id"]
        attrs = data["object_attributes"]
        mergeId = attrs["iid"]
        created_at = attrs["created_at"]

        print("unf: " + created_at)

        # print(created_at)
        # print(gitlabUtils.apiTimeStrMalformed(created_at))
        if gitlabUtils.apiTimeStrMalformed(created_at):
            # if the data comes in the form of malformed ISO from gitlab api, format it correctly..
            created_at = gitlabUtils.apiTimeStrToIso((created_at))
        # print(created_at)
        # print(gitlabUtils.getDeltaIsoMinutes(created_at))

        print("fil : " + created_at)

        mergeExistsInDb = gitlabsqlite.mergeRequestExists(mergeId)
        deltaTime = gitlabUtils.getDeltaIsoMinutes(created_at)

        print("min: " + str(deltaTime))

        if not mergeExistsInDb:
            mrIsOld = deltaTime > NEW_MR_EXPIRE_MINUTES
            if mrIsOld:
                # we detected an MR considered old, but we haven't logged it. add to db
                gitlabsqlite.insertMergeRequest(mergeId, projId)
            else:
                # we detected a new MR! add it to db and send a chat message.
                gitlabsqlite.insertMergeRequest(mergeId, projId)
                title = attrs["title"]
                message = text="Merge Request Created\n" + title + '\n' + str(mergeId)
                slackWrapper.sendMessage(message)

        # Return a response (optional)
    return 'Data received successfully!'


if __name__ == '__main__':
    app.run(port=8080)