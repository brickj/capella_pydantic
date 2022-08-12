# Pydantic Imports
from pydantic import BaseModel
from typing import List, Optional

# Capella Imports
from couchbase.cluster import Cluster, ClusterOptions
from couchbase.auth import PasswordAuthenticator


class Review(BaseModel):
    author: str
    review: str
    likes: int


class UserPost(BaseModel):
    author: str
    date: str
    title: Optional[str] = None
    content: str
    id: int
    likes: List[str]
    reviews: List[Review]


review = [
    Review(author="johndoe", review="This is a comment!", likes=3),
    Review(author="rickJ", review="This is a Rick J comment!", likes=1),
    Review(author="janedoe", review="This is a Jane Doe comment!", likes=2)

]

user_post1 = UserPost(author="johndoe",
                      date="1/1/1970",
                      title="Cool post",
                      content="Cool content",
                      id=10101,
                      likes=["johndoe", "janedoe"],
                      reviews=review)

#Print UserPost
print(user_post1)
#Print first review
print(user_post1.reviews[0].review)


def capella_connect():
    endpoint = <'cluster endpoint'>
    username = <"database user name">
    password = <"database user password">
    bucketName = 'pydantic'
    #### User Input ends here.
    
    # Initialize the Connection
    cluster = Cluster('couchbases://' + endpoint + '?ssl=no_verify',
                      ClusterOptions(PasswordAuthenticator(username, password)))
    cb = cluster.bucket(bucketName)
    cb_coll = cb.default_collection()
    # Create a N1QL Primary Index (but ignore if it exists)
    cluster.query_indexes().create_primary_index(bucketName, ignore_if_exists=True)

    # Upsert JSON dict with key 'u:pydantic_document'
    cb_coll.upsert('u:pydantic_document', user_post1.dict())

    # Load the Document and print it
    print(cb_coll.get('u:pydantic_document').content_as[str])


capella_connect()
