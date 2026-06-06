from agent.main_agent.daily21_main import Daily21MainAgent
from skill.daily21_skill.send_report_skill import exec as send

async def run_flow():
    res = await Daily21MainAgent().run()
    await send(res["data"])
    return res
