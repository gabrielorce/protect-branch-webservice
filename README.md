# protect-branch-webservice
Python-based webservice. Whenever a repository is created in a given organization:
- Automatically creates protection for main branch
- Also notifies user with @mention in an issue within the repository that outlines the protections that were added.


## Requirements
- Python 3.x
- web.py library (pip install web.py)
- ngrok if you wish to run locally


## Execution
- You must set GH_USER and GH_TOKEN variables before executing this script. Example Powershell:

    - `$Env:GH_TOKEN = "ghp_4hb4M0WHc2AU32nN3BsJQi13hXGAUZA43Olkyh"`

    - `$Env:GH_USER = "johhnyb" `

- then execute webservice: `python app.py 4567`

- if using ngrok, open it in a separate console: `ngrok http 4567`

- Logs can be found in ./log/actions.log



## References
- [Creating an issue in Github via API](https://docs.github.com/en/rest/reference/issues#create-an-issue)
- [Adding branch protection via API](https://docs.github.com/en/rest/reference/repos#update-branch-protection)
- [Creating webhooks in Github (with ngrok example)](https://docs.github.com/en/developers/webhooks-and-events/webhooks/creating-webhooks)
- [webpy.org](https://webpy.org/)


## Comments
Easily expandible for further actions. Just add paths and corresponding class name in the urls section, and add the action as a class.
