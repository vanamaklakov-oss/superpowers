#!/usr/bin/env bash
# Поднимает FreeLLMAPI (github.com/tashfeenahmed/freellmapi) локально на :3001 и кладёт единый ключ в $S/unified.key.
# Ключи провайдеров НЕ хранятся здесь: в конфиге стоят заглушки, настоящий ключ подставляет прокси облачной сессии
# (сейчас — generativelanguage.googleapis.com). Новые провайдеры добавляются через защищённую форму, не через чат.
set -e
S=${S:-/tmp/freellm}; R=/home/user/tashfeenahmed/freellmapi; mkdir -p $S; chmod 700 $S
[ -d $R ] || GIT_LFS_SKIP_SMUDGE=1 git clone -q --depth 1 https://github.com/tashfeenahmed/freellmapi $R
[ -d $R/node_modules ] || (cd $R && npm install --no-audit --no-fund >/dev/null)
if [ ! -f $S/env.txt ]; then
  PW=$(openssl rand -hex 12); printf "ENCRYPTION_KEY=%s\nPORT=3001\nADMIN_PW=%s\n" "$(openssl rand -hex 32)" "$PW" > $S/env.txt
  printf '{"admin":{"email":"local@localhost.dev","password":"%s"},"keys":[{"platform":"google","key":"AIzaDummyProxyInjected0000000000000000","label":"proxy"}],"routing":{"strategy":"balanced"}}' "$PW" > $S/config.json
  chmod 600 $S/env.txt $S/config.json
fi
set -a; . $S/env.txt; set +a
curl -s -o /dev/null localhost:3001/v1/models || (cd $R && FREEAPI_CONFIG_PATH=$S/config.json NODE_USE_ENV_PROXY=1 nohup npm run dev -w server > $S/server.log 2>&1 &)
for i in $(seq 60); do curl -s -o /dev/null localhost:3001/v1/models && break; sleep 1; done
TOK=$(curl -s -H 'Content-Type: application/json' localhost:3001/api/auth/login -d "{\"email\":\"local@localhost.dev\",\"password\":\"$ADMIN_PW\"}" | python3 -c "import json,sys;print(json.load(sys.stdin)['token'])")
curl -s -H "Authorization: Bearer $TOK" localhost:3001/api/settings/api-key | python3 -c "import json,sys;open('$S/unified.key','w').write(json.load(sys.stdin)['apiKey'])"; chmod 600 $S/unified.key
echo "FreeLLMAPI: http://localhost:3001/v1  (ключ в $S/unified.key)"
