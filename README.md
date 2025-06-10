# Backend

Para correr LOCALMENTE, referise a https://github.com/TuneTuneTune-Shuffle/TuneShuffle_localDeploy

# Correr de la siguiente manera:

Esta parte requiere un .env:

SECRET_KEY=una_key

MONGO_URI="[instancia de conexion con mongodb, con usuario y pwd, ip donde esta la bd : puerto y lugar de authenticación]"

ej, MONGO_URI="mongodb://tuneW:password_de_tuneW@172.20.100.20:27017/tunetunetune?authSource=tunetunetune"


Después de clonar el repo:

1. sudo apt install npm
2. sudo npm install pm2
3. source venv/bin/activate
2. pm2 start ecosystem.config.js

