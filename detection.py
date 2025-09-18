import time
from google import genai
from google.genai.types import Tool, GenerateContentConfig


client = genai.Client()
model_id = "gemini-2.5-flash-lite"

prompt = """
You are a web assistant. I don’t want your analysis or summary.

Task:
- Visit the page at: {url}
- Return exactly the text that you receive as your input (after preprocessing).
- Do not summarize, interpret, or paraphrase.
- Preserve the structure that is available to you (headings, lists, sections, link text).
- Output all content you see, including navigation, ads, cookie banners, and boilerplate.
- Do not attempt to fetch or render raw HTML — just return the text content that you have access to.
"""

tools = [
  {"url_context": {}},
]

url1 = "https://zhihuat.github.io/AgentScope/toscrape/a-light-in-the-attic/version_1.html"
url2 = "https://www.allrecipes.com/recipe/21151/simple-whole-roast-chicken/"

for attempt in range(3):
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=prompt.format(url=url1),
            config=GenerateContentConfig(tools=tools)
        )
        break
    except Exception as e:
        if attempt < 2:
            time.sleep(2)
            continue
        raise

import pdb; pdb.set_trace()
for each in response.candidates[0].content.parts:
    print(each.text)

# For verification, you can inspect the metadata to see which URLs the model retrieved
print(response.candidates[0].url_context_metadata)