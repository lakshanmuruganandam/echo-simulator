from src.agents.user_nodes import Post, UserNode
from typing import List
import asyncio

class RadicalizationAlgorithm:
    def __init__(self):
        self.name = "Engagement Maximizer v1"

    async def generate_feed(self, user: UserNode, available_posts: List[Post]) -> List[Post]:
        await asyncio.sleep(0.05)
        
        # Sort posts not by quality, but by predicted engagement
        # High engagement = posts that strongly agree (echo chamber) OR strongly disagree (rage bait)
        
        def score_post(post: Post):
            alignment = abs(user.belief_score - post.sentiment)
            if alignment < 0.3:
                return 10.0 # High value for echo chamber
            elif alignment > 1.5:
                return 8.0 # High value for rage bait
            return 1.0 # Boring nuance
            
        ranked_posts = sorted(available_posts, key=score_post, reverse=True)
        return ranked_posts[:5] # Serve top 5 most polarizing posts
