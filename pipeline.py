def iter_research_pipeline(topic: str):
    from agents import (
        build_reader_agent,
        build_search_agent,
        critic_chain,
        writer_chain,
    )

    state = {}

    yield {"step": "search", "status": "running"}
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content
    yield {"step": "search", "status": "done", "result": state["search_results"]}

    yield {"step": "reader", "status": "running"}
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result["messages"][-1].content
    yield {"step": "reader", "status": "done", "result": state["scraped_content"]}

    yield {"step": "writer", "status": "running"}
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    yield {"step": "writer", "status": "done", "result": state["report"]}

    yield {"step": "critic", "status": "running"}
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    yield {"step": "critic", "status": "done", "result": state["feedback"]}
    yield {"step": "complete", "status": "done", "results": state}


def run_research_pipeline(topic: str) -> dict:
    for event in iter_research_pipeline(topic):
        if event["step"] == "complete":
            return event["results"]
    raise RuntimeError("Research pipeline ended without producing results.")



if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
