from plexapi.server import PlexServer


def update_plexapi():
    baseurl = 'http://192.168.1.9:32400'
    token = 'z2bbh3MJ3pYjJdLcZFDp'
    plex = PlexServer(baseurl, token)

    # ------- Find Clients -------
    clients = [client.title for client in plex.clients()]

    plex.library.update()
