# Clear_QBittorrent_Torrents
Docker Repository to clear qBittorrent torrents once they are completed.

### Build Using:
docker build -t tschrock52/clear_qbt_complete .

### Tag Using:
docker tag tschrock52/clear_qbt_complete tschrock52/clear_qbt_complete:latest

### Push Using:
docker push tschrock52/clear_qbt_complete
##### This is hosted on Dockerhub presently

### Run on unRAID Using
docker run --name Clear-qBittorrent-Torrents -itd --network=host tschrock52/clear_qbt_complete
