import asyncio

from scrapely_client import ScrapelyClientAsync

TOKEN = 'MY-SCRAPELY-TOKEN'
HASHTAGS = ['zebra', 'lion', 'hippo']


async def main() -> None:
    scrapely_client = ScrapelyClientAsync(token=TOKEN)

    # Create Scrapely tasks
    scrapely_tasks = []
    scrapely_tasks_client = scrapely_client.tasks()

    for hashtag in HASHTAGS:
        scrapely_task = await scrapely_tasks_client.create(
            name=f'hashtags-{hashtag}',
            actor_id='scrapely/instagram-hashtag-scraper',
            task_input={'hashtags': [hashtag], 'resultsLimit': 20},
            memory_mbytes=1024,
        )
        scrapely_tasks.append(scrapely_task)

    print('Tasks created:', scrapely_tasks)

    # Create Scrapely task clients
    scrapely_task_clients = [scrapely_client.task(task.id) for task in scrapely_tasks]

    print('Task clients created:', scrapely_task_clients)

    # Execute Scrapely tasks
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(client.call()) for client in scrapely_task_clients]

    task_run_results = [task.result() for task in tasks]

    # Filter out None results (tasks that failed to return a run)
    successful_runs = [run for run in task_run_results if run is not None]

    print('Task results:', successful_runs)


if __name__ == '__main__':
    asyncio.run(main())
