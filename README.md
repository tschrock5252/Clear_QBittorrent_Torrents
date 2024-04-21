# Clear_QBittorrent_Torrents
Docker Repository to clear qBittorrent torrents once they are completed.

# Build Using:
docker build -t tschrock52/clear_qbt_complete .

# Tag Using:
docker tag tschrock52/clear_qbt_complete tschrock52/clear_qbt_complete

# Push Using:
docker push tschrock52/clear_qbt_complete
# This is hosted on Dockerhub presently

# Run Using
docker run --name Clear_QBittorrent_Torrents -itd --network=host tschrock52/clear_qbt_complete
