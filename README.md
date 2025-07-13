# Telegram UserBot - Member Transfer Tool

Este userbot de Telegram utiliza Pyrogram para transferir miembros de un grupo a otro.

## ⚠️ ADVERTENCIAS IMPORTANTES

- **USO BAJO TU PROPIA RESPONSABILIDAD**: Este script puede violar los Términos de Servicio de Telegram
- **RIESGO DE BAN**: El uso excesivo puede resultar en la suspensión de tu cuenta
- **LÍMITES DE TELEGRAM**: Respeta los límites de rate limiting para evitar restricciones
- **PRIVACIDAD**: Solo funciona con usuarios que permiten ser agregados por desconocidos

## 📋 Requisitos

1. Python 3.7+
2. Cuenta de Telegram
3. API ID y API Hash de Telegram
4. Permisos de administrador en ambos grupos

## 🚀 Instalación

1. Clona o descarga este proyecto
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Copia el archivo de configuración:
```bash
cp .env.example .env
```

4. Edita el archivo `.env` con tus credenciales:
```
API_ID=tu_api_id
API_HASH=tu_api_hash
PHONE_NUMBER=tu_numero_de_telefono
```

## 🔑 Obtener API Credentials

1. Ve a https://my.telegram.org/
2. Inicia sesión con tu número de teléfono
3. Ve a "API Development Tools"
4. Crea una nueva aplicación
5. Copia el `API ID` y `API Hash`

## 💻 Uso

1. Ejecuta el script:
```bash
python main.py
```

2. En la primera ejecución, se te pedirá el código de verificación de Telegram

3. Ingresa los IDs o usernames de los grupos:
   - Grupo origen (de donde sacar miembros)
   - Grupo destino (donde agregar miembros)

4. Confirma la operación y establece el delay entre requests

## 📝 Formato de Grupos

Puedes usar:
- ID del grupo: `-1001234567890`
- Username del grupo: `@mi_grupo`
- Username sin @: `mi_grupo`

## ⚙️ Configuración

- **Delay**: Tiempo entre requests (recomendado: 2-5 segundos)
- **Rate Limiting**: El script maneja automáticamente los límites de Telegram
- **Error Handling**: Manejo de errores comunes como usuarios privados

## 🛡️ Características de Seguridad

- Manejo de FloodWait automático
- Detección de usuarios con privacidad restringida
- Logging detallado de todas las operaciones
- Confirmación antes de ejecutar transferencias

## 📊 Limitaciones

- Solo transfiere usuarios que permiten ser agregados
- No funciona con bots
- Requiere permisos de administrador
- Sujeto a límites de Telegram API

## 🔧 Estructura del Proyecto

```
telegram_userbot/
├── main.py              # Script principal
├── config.py            # Configuración
├── requirements.txt     # Dependencias
├── .env.example        # Plantilla de configuración
└── README.md           # Este archivo
```

## 🐛 Solución de Problemas

### Error: "API ID/Hash inválido"
- Verifica que las credenciales sean correctas
- Asegúrate de que no haya espacios extra

### Error: "FloodWait"
- El script pausará automáticamente
- Reduce la frecuencia de requests

### Error: "PeerFlood"
- Has excedido los límites de Telegram
- Espera unas horas antes de intentar de nuevo

### Error: "UserPrivacyRestricted"
- El usuario no permite ser agregado por desconocidos
- Esto es normal y se omitirá automáticamente

## 📜 Disclaimer Legal

Este software se proporciona "tal como está" sin garantías. El uso de este script puede violar los Términos de Servicio de Telegram. Los desarrolladores no se hacen responsables por cualquier consecuencia derivada del uso de este software.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.
