# 🧠 Machine Learning Microservice for Street Ninja

`ninja-brain` is a Django Ninja-powered microservice that uses a custom-trained NLP model to extract structured data from incoming SMS messages. It is part of the [Street Ninja](https://github.com/firstflush/street_ninja) ecosystem, a platform designed to help homeless individuals in Vancouver access critical resources through fast, SMS-based support.

This service performs Named Entity Recognition (NER) to detect:

- 📍 **Location** — Where the help is needed (address, intersection, landmark, neighborhood)
- 🍽️ **Resource** — What is being requested (food, shelter, toilet, water fountain, wifi, etc.)
- 🏷️ **Qualifiers** — Additional constraints (`women-only` or `pet-friendly` shelters, for example)

Built using:

- 🧠 **Machine Learning** (spaCy NER)
- 💬 **Natural Language Processing** (custom annotation pipeline)
- ⚙️ **Django Ninja** (high-performance API framework for Django)


## 🕸 Street Ninja Ecosystem

- [Ninja Brain (you are here)](https://github.com/FirstFlush/ninja_brain) — NLP microservice for parsing and routing SMS inquiries
- [Streetlight API](https://github.com/FirstFlush/streetlight-api) — Public API for homelessness resources in Greater Vancouver
- [Ninja Crawl](https://github.com/FirstFlush/ninja_crawl) — Python-based scraping engine (HTML/PDF → JSON)
- [Street Ninja SMS App](https://github.com/FirstFlush/street_ninja) — SMS assistant for accessing resources by text
- [Street Ninja Website](https://github.com/FirstFlush/website_street_ninja) — Try out the SMS assistant and explore the project

