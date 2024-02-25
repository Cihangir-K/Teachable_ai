from autogen import UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent  # As an example

import os
import sys



try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x

config_list = config_list_from_json(
      env_or_file="OAI_CONFIG_LIST.json", 
      filter_dict={
          "model": ["Mistral"]  #"model": ["phi"]
      }
  )
# config_list = config_list_from_json(
#      env_or_file="OAI_CONFIG_LIST.json", 
#      filter_dict={
#          "model": [
#              "gemma:7b"
#          ]
#      }
# config_list = config_list_from_json(
#      env_or_file="OAI_CONFIG_LIST.json", 
#      filter_dict={
#          "model": [
#              "gemma"
#          ]
#      }
#)

cache_seed = None  # Use an int to seed the response cache. Use None to disable caching.

llm_config={
    "config_list": config_list, 
    "timeout": 120, 
    "cache_seed": cache_seed
}



verbosity = 0  # 0 for basic info, 1 to add memory operations, 2 for analyzer messages, 3 for memo lists.
recall_threshold = 1.5  # Higher numbers allow more (but less relevant) memos to be recalled.



teachable_agent = ConversableAgent(
    name="teachable_agent",  # The name can be anything.
    llm_config=llm_config
)



# Instantiate a Teachability object. Its parameters are all optional.
teachability = Teachability(
    reset_db=False,  # Use True to force-reset the memo DB, and False to use an existing DB.
    path_to_db_dir="./tmp/interactive/teachability_db",  # Can be any path, but teachable agents in a group chat require unique paths.
    verbosity=0,
    recall_threshold=1.5
)

# Now add teachability to the agent.
teachability.add_to_agent(teachable_agent)

# For this test, create a user proxy agent as usual.
user = UserProxyAgent("user", human_input_mode="ALWAYS",code_execution_config={"work_dir":"coding", "use_docker":False})



# This function will return once the user types 'exit'.
teachable_agent.initiate_chat(user, message="Hi, I'm a teachable user assistant! What's on your mind?")
