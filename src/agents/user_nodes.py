from pydantic import BaseModel, Field
import asyncio
from typing import List

class Post(BaseModel):
    post_id: str
    author_id: str
    content: str
    sentiment: float = Field(..., ge=-1.0, le=1.0) # -1 extreme against, 1 extreme for
    engagement: int = 0

class UserNode(BaseModel):
    user_id: str
    belief_score: float = Field(..., ge=-1.0, le=1.0)
    
class NodeSwarm:
    def __init__(self, users: List[UserNode]):
        self.users = users
        
    async def interact_with_post(self, user: UserNode, post: Post):
        await asyncio.sleep(0.01) # Simulate reading
        
        # If the post aligns with their belief, they engage and become slightly more radicalized
        alignment = abs(user.belief_score - post.sentiment)
        
        if alignment < 0.3: # Strong agreement
            post.engagement += 10
            # Shift belief towards the post
            user.belief_score = (user.belief_score + post.sentiment) / 2
        elif alignment > 1.5: # Strong disagreement
            post.engagement += 5 # Hate reading
            # Shift belief further away from the post (polarization)
            user.belief_score = user.belief_score - (post.sentiment * 0.1)
            
        # Clamp belief
        user.belief_score = max(-1.0, min(1.0, user.belief_score))
