# import asyncio


# async def delayed_print(text, time=1):
#     await asyncio.sleep(time)
#     print(text)


# async def main_coro():
#     # python >= 3.7
#     task1 = asyncio.create_task(delayed_print("I'm printed second!", 2))
#     # python >= 3.3
#     task2 = asyncio.ensure_future(delayed_print("I'm printed first!"))
#     await asyncio.gather(task1, task2, delayed_print("I'm printed last!", 3))


# # python >= 3.7
# asyncio.run(main_coro())


# import aiohttp
# import asyncio
# from itertools import chain

# API_URL = "https://en.wikipedia.org/w/api.php"

# HEADERS = {
#     "user-agent": "ConcurrentSearchBot/0.1 (educational project)",
# }

# PARAMS = {
#     "action": "query",
#     "list": "search",
#     "srsearch": "biology",
#     "srlimit": 1,
#     "format": "json",
# }


# async def fetch(session, url, params):
#     async with session.get(url, params=params) as response:

#         print(response.status)
#         print(response.headers.get("Content-Type"))
#         print(response.url)

#         return await response.json()


# async def fetch_all():
#     async with aiohttp.ClientSession(headers=HEADERS) as session:
#         task = asyncio.create_task(fetch(session, API_URL, PARAMS))

#         response = await task

#         print()
#         print(f"Название статьи: {response["query"]["search"][0]["title"]}")
#         print()
#         print("SNIPPET:")
#         print(response["query"]["search"][0]["snippet"].strip())
#         print()
#         for k in response:
#             print(response[k])


# print(asyncio.run(fetch_all()))


# gh_result = {
#     "total_count": 24,
#     "incomplete_results": False,
#     "items": [
#         {
#             "id": 861202119,
#             "node_id": "R_kgDOM1Tmxw",
#             "name": "firerequests",
#             "full_name": "rishiraj/firerequests",
#             "private": False,
#             "owner": {
#                 "login": "rishiraj",
#                 "id": 44090649,
#                 "node_id": "MDQ6VXNlcjQ0MDkwNjQ5",
#                 "avatar_url": "https://avatars.githubusercontent.com/u/44090649?v=4",
#                 "gravatar_id": "",
#                 "url": "https://api.github.com/users/rishiraj",
#                 "html_url": "https://github.com/rishiraj",
#                 "followers_url": "https://api.github.com/users/rishiraj/followers",
#                 "following_url": "https://api.github.com/users/rishiraj/following{/other_user}",
#                 "gists_url": "https://api.github.com/users/rishiraj/gists{/gist_id}",
#                 "starred_url": "https://api.github.com/users/rishiraj/starred{/owner}{/repo}",
#                 "subscriptions_url": "https://api.github.com/users/rishiraj/subscriptions",
#                 "organizations_url": "https://api.github.com/users/rishiraj/orgs",
#                 "repos_url": "https://api.github.com/users/rishiraj/repos",
#                 "events_url": "https://api.github.com/users/rishiraj/events{/privacy}",
#                 "received_events_url": "https://api.github.com/users/rishiraj/received_events",
#                 "type": "User",
#                 "user_view_type": "public",
#                 "site_admin": False,
#             },
#             "html_url": "https://github.com/rishiraj/firerequests",
#             "description": "High-performance, asynchronous Python HTTP client library designed for faster file transfers using concurrency, semaphores, and fault-tolerant features.",
#             "fork": False,
#             "url": "https://api.github.com/repos/rishiraj/firerequests",
#             "forks_url": "https://api.github.com/repos/rishiraj/firerequests/forks",
#             "keys_url": "https://api.github.com/repos/rishiraj/firerequests/keys{/key_id}",
#             "collaborators_url": "https://api.github.com/repos/rishiraj/firerequests/collaborators{/collaborator}",
#             "teams_url": "https://api.github.com/repos/rishiraj/firerequests/teams",
#             "hooks_url": "https://api.github.com/repos/rishiraj/firerequests/hooks",
#             "issue_events_url": "https://api.github.com/repos/rishiraj/firerequests/issues/events{/number}",
#             "events_url": "https://api.github.com/repos/rishiraj/firerequests/events",
#             "assignees_url": "https://api.github.com/repos/rishiraj/firerequests/assignees{/user}",
#             "branches_url": "https://api.github.com/repos/rishiraj/firerequests/branches{/branch}",
#             "tags_url": "https://api.github.com/repos/rishiraj/firerequests/tags",
#             "blobs_url": "https://api.github.com/repos/rishiraj/firerequests/git/blobs{/sha}",
#             "git_tags_url": "https://api.github.com/repos/rishiraj/firerequests/git/tags{/sha}",
#             "git_refs_url": "https://api.github.com/repos/rishiraj/firerequests/git/refs{/sha}",
#             "trees_url": "https://api.github.com/repos/rishiraj/firerequests/git/trees{/sha}",
#             "statuses_url": "https://api.github.com/repos/rishiraj/firerequests/statuses/{sha}",
#             "languages_url": "https://api.github.com/repos/rishiraj/firerequests/languages",
#             "stargazers_url": "https://api.github.com/repos/rishiraj/firerequests/stargazers",
#             "contributors_url": "https://api.github.com/repos/rishiraj/firerequests/contributors",
#             "subscribers_url": "https://api.github.com/repos/rishiraj/firerequests/subscribers",
#             "subscription_url": "https://api.github.com/repos/rishiraj/firerequests/subscription",
#             "commits_url": "https://api.github.com/repos/rishiraj/firerequests/commits{/sha}",
#             "git_commits_url": "https://api.github.com/repos/rishiraj/firerequests/git/commits{/sha}",
#             "comments_url": "https://api.github.com/repos/rishiraj/firerequests/comments{/number}",
#             "issue_comment_url": "https://api.github.com/repos/rishiraj/firerequests/issues/comments{/number}",
#             "contents_url": "https://api.github.com/repos/rishiraj/firerequests/contents/{+path}",
#             "compare_url": "https://api.github.com/repos/rishiraj/firerequests/compare/{base}...{head}",
#             "merges_url": "https://api.github.com/repos/rishiraj/firerequests/merges",
#             "archive_url": "https://api.github.com/repos/rishiraj/firerequests/{archive_format}{/ref}",
#             "downloads_url": "https://api.github.com/repos/rishiraj/firerequests/downloads",
#             "issues_url": "https://api.github.com/repos/rishiraj/firerequests/issues{/number}",
#             "pulls_url": "https://api.github.com/repos/rishiraj/firerequests/pulls{/number}",
#             "milestones_url": "https://api.github.com/repos/rishiraj/firerequests/milestones{/number}",
#             "notifications_url": "https://api.github.com/repos/rishiraj/firerequests/notifications{?since,all,participating}",
#             "labels_url": "https://api.github.com/repos/rishiraj/firerequests/labels{/name}",
#             "releases_url": "https://api.github.com/repos/rishiraj/firerequests/releases{/id}",
#             "deployments_url": "https://api.github.com/repos/rishiraj/firerequests/deployments",
#             "created_at": "2024-09-22T09:27:39Z",
#             "updated_at": "2026-08-27T14:03:35Z",
#             "pushed_at": "2025-05-12T05:43:27Z",
#             "git_url": "git://github.com/rishiraj/firerequests.git",
#             "ssh_url": "git@github.com:rishiraj/firerequests.git",
#             "clone_url": "https://github.com/rishiraj/firerequests.git",
#             "svn_url": "https://github.com/rishiraj/firerequests",
#             "homepage": "https://pypi.org/project/firerequests/",
#             "size": 104,
#             "stargazers_count": 59,
#             "watchers_count": 59,
#             "language": "Python",
#             "has_issues": True,
#             "has_projects": True,
#             "has_downloads": False,
#             "has_wiki": True,
#             "has_pages": False,
#             "has_discussions": False,
#             "forks_count": 5,
#             "mirror_url": None,
#             "archived": False,
#             "disabled": False,
#             "open_issues_count": 0,
#             "license": {
#                 "key": "apache-2.0",
#                 "name": "Apache License 2.0",
#                 "spdx_id": "Apache-2.0",
#                 "url": "https://api.github.com/licenses/apache-2.0",
#                 "node_id": "MDc6TGljZW5zZTI=",
#             },
#             "allow_forking": True,
#             "is_template": False,
#             "web_commit_signoff_required": False,
#             "has_pull_requests": True,
#             "pull_request_creation_policy": "all",
#             "topics": [
#                 "aiohttp",
#                 "asynchronous",
#                 "asyncio",
#                 "concurrency",
#                 "file-transfer",
#                 "hacktoberfest",
#                 "http-client",
#             ],
#             "visibility": "public",
#             "forks": 5,
#             "open_issues": 0,
#             "watchers": 59,
#             "default_branch": "main",
#             "score": 1.0,
#         },
#         {
#             "id": 522294201,
#             "node_id": "R_kgDOHyGTuQ",
#             "name": "self-limiters",
#             "full_name": "snok/self-limiters",
#             "private": False,
#             "owner": {
#                 "login": "snok",
#                 "id": 64945977,
#                 "node_id": "MDEyOk9yZ2FuaXphdGlvbjY0OTQ1OTc3",
#                 "avatar_url": "https://avatars.githubusercontent.com/u/64945977?v=4",
#                 "gravatar_id": "",
#                 "url": "https://api.github.com/users/snok",
#                 "html_url": "https://github.com/snok",
#                 "followers_url": "https://api.github.com/users/snok/followers",
#                 "following_url": "https://api.github.com/users/snok/following{/other_user}",
#                 "gists_url": "https://api.github.com/users/snok/gists{/gist_id}",
#                 "starred_url": "https://api.github.com/users/snok/starred{/owner}{/repo}",
#                 "subscriptions_url": "https://api.github.com/users/snok/subscriptions",
#                 "organizations_url": "https://api.github.com/users/snok/orgs",
#                 "repos_url": "https://api.github.com/users/snok/repos",
#                 "events_url": "https://api.github.com/users/snok/events{/privacy}",
#                 "received_events_url": "https://api.github.com/users/snok/received_events",
#                 "type": "Organization",
#                 "user_view_type": "public",
#                 "site_admin": False,
#             },
#             "html_url": "https://github.com/snok/self-limiters",
#             "description": "Async distributed rate limiters for Python",
#             "fork": False,
#             "url": "https://api.github.com/repos/snok/self-limiters",
#             "forks_url": "https://api.github.com/repos/snok/self-limiters/forks",
#             "keys_url": "https://api.github.com/repos/snok/self-limiters/keys{/key_id}",
#             "collaborators_url": "https://api.github.com/repos/snok/self-limiters/collaborators{/collaborator}",
#             "teams_url": "https://api.github.com/repos/snok/self-limiters/teams",
#             "hooks_url": "https://api.github.com/repos/snok/self-limiters/hooks",
#             "issue_events_url": "https://api.github.com/repos/snok/self-limiters/issues/events{/number}",
#             "events_url": "https://api.github.com/repos/snok/self-limiters/events",
#             "assignees_url": "https://api.github.com/repos/snok/self-limiters/assignees{/user}",
#             "branches_url": "https://api.github.com/repos/snok/self-limiters/branches{/branch}",
#             "tags_url": "https://api.github.com/repos/snok/self-limiters/tags",
#             "blobs_url": "https://api.github.com/repos/snok/self-limiters/git/blobs{/sha}",
#             "git_tags_url": "https://api.github.com/repos/snok/self-limiters/git/tags{/sha}",
#             "git_refs_url": "https://api.github.com/repos/snok/self-limiters/git/refs{/sha}",
#             "trees_url": "https://api.github.com/repos/snok/self-limiters/git/trees{/sha}",
#             "statuses_url": "https://api.github.com/repos/snok/self-limiters/statuses/{sha}",
#             "languages_url": "https://api.github.com/repos/snok/self-limiters/languages",
#             "stargazers_url": "https://api.github.com/repos/snok/self-limiters/stargazers",
#             "contributors_url": "https://api.github.com/repos/snok/self-limiters/contributors",
#             "subscribers_url": "https://api.github.com/repos/snok/self-limiters/subscribers",
#             "subscription_url": "https://api.github.com/repos/snok/self-limiters/subscription",
#             "commits_url": "https://api.github.com/repos/snok/self-limiters/commits{/sha}",
#             "git_commits_url": "https://api.github.com/repos/snok/self-limiters/git/commits{/sha}",
#             "comments_url": "https://api.github.com/repos/snok/self-limiters/comments{/number}",
#             "issue_comment_url": "https://api.github.com/repos/snok/self-limiters/issues/comments{/number}",
#             "contents_url": "https://api.github.com/repos/snok/self-limiters/contents/{+path}",
#             "compare_url": "https://api.github.com/repos/snok/self-limiters/compare/{base}...{head}",
#             "merges_url": "https://api.github.com/repos/snok/self-limiters/merges",
#             "archive_url": "https://api.github.com/repos/snok/self-limiters/{archive_format}{/ref}",
#             "downloads_url": "https://api.github.com/repos/snok/self-limiters/downloads",
#             "issues_url": "https://api.github.com/repos/snok/self-limiters/issues{/number}",
#             "pulls_url": "https://api.github.com/repos/snok/self-limiters/pulls{/number}",
#             "milestones_url": "https://api.github.com/repos/snok/self-limiters/milestones{/number}",
#             "notifications_url": "https://api.github.com/repos/snok/self-limiters/notifications{?since,all,participating}",
#             "labels_url": "https://api.github.com/repos/snok/self-limiters/labels{/name}",
#             "releases_url": "https://api.github.com/repos/snok/self-limiters/releases{/id}",
#             "deployments_url": "https://api.github.com/repos/snok/self-limiters/deployments",
#             "created_at": "2022-08-07T18:34:37Z",
#             "updated_at": "2025-07-29T12:24:01Z",
#             "pushed_at": "2024-01-18T05:05:26Z",
#             "git_url": "git://github.com/snok/self-limiters.git",
#             "ssh_url": "git@github.com:snok/self-limiters.git",
#             "clone_url": "https://github.com/snok/self-limiters.git",
#             "svn_url": "https://github.com/snok/self-limiters",
#             "homepage": "",
#             "size": 2329,
#             "stargazers_count": 32,
#             "watchers_count": 32,
#             "language": "Rust",
#             "has_issues": True,
#             "has_projects": True,
#             "has_downloads": False,
#             "has_wiki": True,
#             "has_pages": False,
#             "has_discussions": False,
#             "forks_count": 1,
#             "mirror_url": None,
#             "archived": False,
#             "disabled": False,
#             "open_issues_count": 2,
#             "license": {
#                 "key": "bsd-4-clause",
#                 "name": 'BSD 4-Clause "Original" or "Old" License',
#                 "spdx_id": "BSD-4-Clause",
#                 "url": "https://api.github.com/licenses/bsd-4-clause",
#                 "node_id": "MDc6TGljZW5zZTM5",
#             },
#             "allow_forking": True,
#             "is_template": False,
#             "web_commit_signoff_required": False,
#             "has_pull_requests": True,
#             "pull_request_creation_policy": "all",
#             "topics": [
#                 "async",
#                 "asyncio",
#                 "distributed",
#                 "python",
#                 "rate-limiter",
#                 "redis",
#                 "rust",
#                 "semaphore",
#                 "tokenbucket",
#             ],
#             "visibility": "public",
#             "forks": 1,
#             "open_issues": 2,
#             "watchers": 32,
#             "default_branch": "main",
#             "score": 1.0,
#         },
#     ],
# }

# for k in gh_result["items"][0].keys():
#     print("---")
#     print(k)
#     print("---")
