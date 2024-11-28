# Sketchfab Backup

3D models uploaded to https://sketchfab.com will become unavailable for download sometime during 2025. More info:
* https://www.change.org/p/keep-sketchfab-alive-preserve-open-access-to-3d-art-museum-collections
* https://sketchfab.com/blogs/community/fab-publishing-portal-open-for-sketchfab-migration/

We try to download and mirror as many [CC](https://creativecommons.org/) licensed models as possible, so that they can later be reuploaded in one go to another place, without the need for intervention of every individual contributor. Currently, we're focusing on the Cultural Heritage & History section, which contains many digitized collections of museums. Depending on available storage and time, we will continue with other categories.

The mirrored data is available here for the time being: __https://mirror.traines.eu/sketchfab-backup/__

They should move ASAP somewhere else, where they can be properly browsed:

* https://commons.wikimedia.org/ – glb format compatibility is in the works (?)
* https://henge.io/ - another private, but seemingly open platform
* TBD...

In the meantime, if you have spare storage (the entirety of Sketchfab could be dozens of terabytes) or other propositions/ideas, get in touch (e.g. via issues or email)!

You can also help scraping. But then it probably makes sense to coordinate who scapes what (e.g. via issues). If you want to scrape yourself, you may check out this repo and run with Docker:
```
docker run -it --name sketchfab-backup \
-v /your/path/:/your/path/ \
-e SKETCHFAB_DEST_PATH=/your/path/ \
-e SKETCHFAB_API_TOKEN=<your-token-from-sketchfab> $(docker build -q .) 
```
Token can be obtained from https://sketchfab.com/settings/password.