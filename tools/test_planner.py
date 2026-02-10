import asyncio

async def run():
    import sys, os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    try:
        from src.agents.planner import PlannerAgent
    except Exception as e:
        print('IMPORT ERROR:', type(e), e)
        return

    planner = PlannerAgent()
    try:
        res = await planner.execute('https://play.ezygamers.com/')
        print('OK:', res['total_tests_generated'])
        for t in res['test_cases'][:5]:
            print(t)
    except Exception as e:
        print('ERROR:', type(e), e)

asyncio.run(run())
