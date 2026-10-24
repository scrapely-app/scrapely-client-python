# Derived from apify-client-python (docs/03_guides/code/02_tasks_sync.py), Copyright Apify Technologies s.r.o., Apache License 2.0. Modified by TeraShift GmbH.
from scrapely_client import ScrapelyClient

TOKEN = 'MY-SCRAPELY-TOKEN'
HASHTAGS = ['zebra', 'lion', 'hippo']


def main() -> None:
    scrapely_client = ScrapelyClient(token=TOKEN)

    # Create Scrapely tasks
    scrapely_tasks = []
    scrapely_tasks_client = scrapely_client.tasks()

    for hashtag in HASHTAGS:
        scrapely_task = scrapely_tasks_client.create(
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
    task_run_results = [client.call() for client in scrapely_task_clients]

    # Filter out None results (tasks that failed to return a run)
    successful_runs = [run for run in task_run_results if run is not None]

    print('Task results:', successful_runs)


if __name__ == '__main__':
    main()
