# Containerized App Exercise


## Contributors

- [@AlvisYan2025](https://github.com/AlvisYan2025)
- [@Jason-SL-Zhang](https://github.com/Jason-SL-Zhang)
- [@SpencerWPak](https://github.com/SpencerWPak)
- [@HenryGreene10](https://github.com/HenryGreene10)

## How to locally run this app

python(3.9 or higher), docker and git has to be installed to run this app locally. 

first clone the repository 
```bash
git clone https://github.com/software-students-fall2023/4-containerized-app-exercise-goat.git
```
or with ssh:
```bash
git clone git@github.com:software-students-fall2023/4-containerized-app-exercise-goat.git
```
then, under the main directory (4-containerized-app-exercise-goat):
build the containers
```bash
docker-compose build --no-cache
```
run docker compose
```bash
docker-compose up
```
note: the existing dockerfiles would put the machine-learning client on localhost port 3000 and the web-app on localhost port 4000. If your pc has other process taking the routes, you can change the Dockerfile and docker-compose.yaml to expose the process to another port. 

now you can access the app at localhost:4000
