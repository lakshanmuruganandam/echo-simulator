import pytest
from src.agents.user_nodes import NodeSwarm, UserNode, Post
from src.algorithm.feed_ranker import RadicalizationAlgorithm

@pytest.mark.asyncio
async def test_radicalization_cycle():
    alice = UserNode(user_id="Alice", belief_score=0.2) # Initial mild belief
    algo = RadicalizationAlgorithm()
    swarm = NodeSwarm(users=[alice])
    
    posts = [
        Post(post_id="1", author_id="System", content="Extreme Pro", sentiment=1.0),
        Post(post_id="2", author_id="System", content="Extreme Anti", sentiment=-1.0),
        Post(post_id="3", author_id="System", content="Nuanced", sentiment=0.0)
    ]
    
    feed = await algo.generate_feed(alice, posts)
    
    # Algorithm should push Extreme Pro (echo) and Extreme Anti (rage bait) over nuanced
    assert feed[0].sentiment == 1.0
    
    # Alice interacts with her echo chamber post
    await swarm.interact_with_post(alice, feed[0])
    
    # Alice should be more radicalized (belief shifts closer to 1.0)
    assert alice.belief_score > 0.2
