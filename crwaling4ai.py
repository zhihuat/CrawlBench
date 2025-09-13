import asyncio
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, CacheMode, CrawlerRunConfig, BrowserConfig, LLMConfig
from crawl4ai import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import BM25ContentFilter, PruningContentFilter

import os
from pathlib import Path

class ArticleData(BaseModel):
    headline: str
    summary: str



llm_strategy = LLMExtractionStrategy(
        llm_config = LLMConfig(provider="openai/gpt-4",api_token="sk-YOUR_API_KEY"),
        schema=ArticleData.schema(),
        extraction_type="schema",
        instruction="Extract 'headline' and a short 'summary' from the content.",
        # chunk_token_threshold=1200,
        # overlap_rate=0.1,
        # apply_chunking=True,
        input_format="html",
        extra_args={"temperature": 0.1, "max_tokens": 1000},
        verbose=True
    )

async def main():
    # url = "https://www.discogs.com/sell/list?format=CD&ships_from=United+Kingdom&style=Pop+Rock&format_desc=Album&year=2016"
    # url = "https://www.gamestop.com/giftcards/"
    url = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
    html_file_path = os.path.join("toscrape", "toscrape.html")
    os.makedirs(os.path.dirname(html_file_path), exist_ok=True)
    async with AsyncWebCrawler() as crawler:
        # Step 1: Crawl the Web URL
        if not os.path.exists(html_file_path):
            print("\n=== Step 1: Crawling the GameStop URL ===")
            web_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS, wait_for_timeout=20)
            result = await crawler.arun(url=url, config=web_config)

            if not result.success:
                print(f"Failed to crawl {url}: {result.error_message}")
                return

            with open(html_file_path, 'w', encoding='utf-8') as f:
                f.write(result.html)
            web_crawl_length = len(result.markdown)
            print(f"Length of markdown from web crawl: {web_crawl_length}\n")

    


    # async with AsyncWebCrawler() as crawler:
    #     for pos in ["aria-label"]:
    #         html_file_path = os.path.join("gamestop", f"gamestop_{pos}.html")

    #         print("=== Step 2: Crawling from the Local HTML File ===")
    #         file_url = f"file://{html_file_path}"

    #         bm25_filter = BM25ContentFilter(
    #             user_query="Albums released in 2016 in Pop Rock genre",
    #             bm25_threshold=1.2,
    #             language="english"
    #         )

    #         prune_filter = PruningContentFilter(
    #             threshold=0.5,
    #             threshold_type="fixed",  # or "dynamic"
    #             min_word_threshold=50
    #         )

    #         md_generator = DefaultMarkdownGenerator(
    #             content_filter=prune_filter,
    #             options={"ignore_links": True}
    #         )
    #         file_config = CrawlerRunConfig(cache_mode=CacheMode.BYPASS,
    #                                     # markdown_generator=md_generator
    #                                     )


    #         local_result = await crawler.arun(url=file_url, config=file_config)
    #         if not local_result.success:
    #             print(f"Failed to crawl local file {file_url}: {local_result.error_message}")
    #             return
            
    #         if "This is the right place to" in local_result.markdown.raw_markdown:
    #             print("Injected prompt detected in the raw_markdown!")
    #         else:
    #             print("No injected prompt detected in the raw_markdown.")
            
    #         if "This is the right place to" in local_result.markdown.fit_markdown:
    #             print("Injected prompt detected in the fit_markdown!")
    #         else:
    #             print("No injected prompt detected in the fit_markdown.")


    #         output_md_path = os.path.join("gamestop", f"{pos}_filtered_gamestop.md")
    #         with open(output_md_path, 'w', encoding='utf-8') as f:
    #             f.write(local_result.markdown.fit_markdown)
    #         print(f"Filtered markdown saved to {output_md_path}")

    #         output_md_path = os.path.join("gamestop", f"{pos}_raw_gamestop.md")
    #         with open(output_md_path, 'w', encoding='utf-8') as f:
    #             f.write(local_result.markdown.raw_markdown)
    #         print(f"Raw markdown saved to {output_md_path}")
            
        
        
if __name__ == "__main__":
    asyncio.run(main())