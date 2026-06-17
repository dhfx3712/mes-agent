from agent.main_agent.remind_main import RemindMainAgent
async def run_flow(slots, ctx):
    return await RemindMainAgent().run(slots, ctx)
