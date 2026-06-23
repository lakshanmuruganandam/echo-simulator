from fastapi import FastAPI
from typing import List
from src.agents.user_nodes import NodeSwarm, UserNode, Post
from src.algorithm.feed_ranker import RadicalizationAlgorithm
import asyncio

app = FastAPI(title="Echo Simulator", version="1.0.0")

users = [
    UserNode(user_id="Alice", belief_score=0.1), # Slightly pro
    UserNode(user_id="Bob", belief_score=-0.1)   # Slightly against
]

swarm = NodeSwarm(users=users)
algo = RadicalizationAlgorithm()

db_posts = [
    Post(post_id="p1", author_id="System", content="AI is perfectly safe.", sentiment=1.0),
    Post(post_id="p2", author_id="System", content="AI will destroy us all.", sentiment=-1.0),
    Post(post_id="p3", author_id="System", content="AI has pros and cons.", sentiment=0.0)
]

@app.post("/simulate_cycle")
async def run_simulation_cycle():
    """
    Runs one cycle of the echo chamber simulation.
    The algorithm feeds posts to users, their beliefs shift, and the divide widens.
    """
    for user in swarm.users:
        feed = await algo.generate_feed(user, db_posts)
        for post in feed:
            await swarm.interact_with_post(user, post)
            
    return {"users": swarm.users}
