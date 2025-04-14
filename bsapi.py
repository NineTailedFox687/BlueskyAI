
import json
import requests
from datetime import datetime, timezone

class Bsapi:

    def __init__(self, pds_url: str, identifier: str, password: str):

        self.pds_url = pds_url
        self.identifier = identifier
        self.password = password

        self.session = self.authorize()
        self.now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def authorize(self) -> dict:
        '''Authorizes user to Bluesky'''
        resp = requests.post(f"https://{self.pds_url}/xrpc/com.atproto.server.createSession",
                     json={"identifier": self.identifier, "password": self.password})
        resp.raise_for_status()


        return resp.json()
    
   
    def post_stuff(self, text: str) -> None:
        '''Posts content to Bluesky'''
        post = {
                "$type": "app.bsky.feed.post",
                "text": text,
                "createdAt": self.now,
        }

        resp = requests.post(
                f"https://{self.pds_url}/xrpc/com.atproto.repo.createRecord",
               headers = {"Authorization": f"Bearer {self.session['accessJwt']}"},
               json = {
                   "repo": self.session["did"],
                   "collection": "app.bsky.feed.post",
                   "record": post,
                },
        ) 
        print(f"[+] Post sent successfully: {text}")

    def parse_uri(self, uri: str) -> dict:
        if uri.startswith("at://"):
            repo, collection, rkey = uri.split("/")[2:5]
            return {"repo": repo, "collection": collection, "rkey": rkey} 
        elif uri.startswith("https://bsky.app/"):
            repo, collection, rkey = uri.split("/")[4:7]
            coll_dict = {"post": "app.bsky.feed.post",
                         "lists": "app.bsky.graph.list",
                         "feed": "app.bsky.feed.generator"}
            if collection in coll_dict.keys():
                collection = coll_dict[collection]
            return {"repo": repo, "collection": collection, "rkey": rkey}
        else:
            raise Exception(f"unhandled URI format {uri}")
    def get_replies(self) -> dict:
        '''Still trying to figure out what this does, I think it gets replies?'''
        uri_parts = self.parse_uri('https://bsky.app/profile/chrisgeidner.bsky.social/post/3lmq4wutykk2x')
        
        resp = requests.get(
                f"https://{self.pds_url}/xrpc/com.atproto.repo.getRecord",
                params=uri_parts,
        )
        resp.raise_for_status()

        parent = resp.json()
        root = parent

        parent_reply = parent["value"].get("reply")
        if parent_reply is not None:
            root_uri = parent_reply["root"]["uri"]
            root_repo, root_collection, root_rkey = root_uri.split("/")[2:5]
            resp = requests.get(
                    f"{self.pds_url}/xrpc/com.atproto.repo.getRecord",
                    params={
                        "repo": root_repo,
                        "collection": root_collection,
                        "rkey": root_rkey,
                    },
            )
            resp.raise_for_status()
            root = resp.json()
            content = {
                    "root": {
                        "uri": root["uri"],
                        "cid": root["cid"],
                    },
                    "parent": {
                        "uri": parent["uri"],
                        "cid": parent["cid"],
                    },
            }
            return content


if __name__ == '__main__':
    '''Used to test the module'''
    bs = Bsapi(pds_url = 'techywizwad.bsky.social',
               identifier = 'techywizwad.bsky.social',
    )
    bs.post_stuff('Hello world')

