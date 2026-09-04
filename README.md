# FieldControl---Official-Integration---Home-Assistant
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2026.3%2B-blue.svg?logo=home-assistant)](https://www.home-assistant.io/)
[![HACS Custom Repository](https://img.shields.io/badge/HACS-Custom%20Repo-orange.svg?logo=home-assistant)](https://hacs.xyz/)
[![Hardware](https://img.shields.io/badge/Hardware-ESP32--C6%20%7F%20S2%20%7F%20S3-green.svg)](https://www.espressif.com/)
[![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)](LICENSE)
[![Local Control](https://img.shields.io/badge/Control-100%25%20Local-green.svg)]()

Integración **100% local y autónoma** para controladores de riego inteligente **FieldControl** con **Home Assistant**. Permite supervisar y comandar válvulas, bombas de agua, control de riego climatico, sin depender de internet ni servidores en la nube.

---

## 🛍️ Dos Métodos de Instalación Disponibles

Puedes elegir la opción que mejor se adapte a tus clientes:

### 🌟 Opción 1: Instalación Gráfica 1-Click mediante HACS (Recomendada)
*Ideal para clientes que quieren ingresar la IP en un formulario en pantalla sin editar archivos de código.*

1. En Home Assistant, abre **HACS** -> **Integraciones**.
2. Haz clic en los tres puntos (arriba a la derecha) -> **Repositorios personalizados**.
3. Añade la URL de este repositorio con la categoría **Integración**.
4. Busca **FieldControl** y presiona **Descargar**.
5. Reinicia Home Assistant.
6. Ve a **Ajustes** -> **Dispositivos y Servicios** -> **Añadir Integración** -> Busca **FieldControl**.
7. ¡Ingresa la IP local de tu equipo (ej. `192.168.1.50`) en la ventana emergente y listo!

---

### 📦 Opción 2: Instalación Manual mediante Paquetes YAML (Sin HACS)
*Ideal si no utilizas HACS o prefieres configurar tus entidades mediante archivos YAML tradicionales.*

1. Copia el archivo [`packages/fieldcontrol.yaml`](packages/fieldcontrol.yaml) dentro de la carpeta `packages/` de tu Home Assistant.
2. Reemplaza la IP `192.168.1.50` por la IP asignada a tu FieldControl en tu red local.
3. Asegúrate de incluir en tu `configuration.yaml`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
4. Reinicia Home Assistant.

---

## 🎨 Importar el Dashboard Lovelace (Estilo WebApp)

1. En Home Assistant, ve a **Ajustes -> Cuadros de mando -> Añadir cuadro de mando**.
2. Selecciona **Cuadro de mando en blanco**, nómbralo "FieldControl" y guarda.
3. Abre el menú de tres puntos (arriba a la derecha) -> **Editar cuadro de mando** -> **Editar código YAML**.
4. Copia el contenido de [`dashboards/fieldcontrol_dashboard.yaml`](dashboards/fieldcontrol_dashboard.yaml) y pégalo.

---

## 📡 Referencia de la API REST Local (ESP32 Firmware)

| Endpoint | Método | Parámetros | Descripción |
| :--- | :--- | :--- | :--- |
| `/api/status` | `GET` | Ninguno | Devuelve el JSON completo de estado del equipo |
| `/api/manual/start` | `GET` | `v` (válvula 0-indexed), `t` (minutos) | Enciende la válvula `v` durante `t` minutos |
| `/api/stop` | `GET` | Ninguno | Parada de emergencia (cierra todas las válvulas) |
| `/api/auto/play` | `GET` | Ninguno | Habilita el modo de riego automático |
| `/api/auto/stop` | `GET` | Ninguno | Deshabilita el modo automático |
| `/api/acc/set` | `GET` | `s` (`1` = ON, `0` = OFF) | Enciende o apaga el relé accesorio / bomba |

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
