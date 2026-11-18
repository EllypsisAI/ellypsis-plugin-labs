<p align="center">
  <img src="../assets/banner.png" alt="Ellypsis Plugin Labs: métodos de experto para tu agente de IA" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-works-7c3f63?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Claude_Cowork-works-7c3f63?style=flat-square" alt="Claude Cowork">
  <img src="https://img.shields.io/badge/ChatGPT_Codex-works-7c3f63?style=flat-square" alt="ChatGPT Codex">
  <img src="https://img.shields.io/badge/license-MIT-191713?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <a href="../README.md">English</a> ·
  <a href="README.da.md">Dansk</a> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.sv.md">Svenska</a> ·
  <a href="README.no.md">Norsk</a> ·
  <a href="README.fr.md">Français</a> ·
  <b>Español</b>
</p>

---

Pídele a tu agente de IA un flujo de registro y te dibuja uno. No te pregunta quién se va a registrar, qué le preocupa ni por qué la mitad abandona en el paso dos. Es aprendiz de todo y maestro de nada.

**Plugin Labs le da el oficio.** Cada plugin recoge cómo trabaja de verdad un especialista: las preguntas que hace primero, los errores que ya aprendió a evitar, el orden en que hace las cosas. Lo instalas una vez y entra en acción cada vez que pides ese tipo de trabajo. Le hablas a tu agente como siempre. Solo que deja de improvisar.

## Lo que trae

| | Plugin | Qué hace por ti | Funciona en |
|:-:|---|---|---|
| 🧭 | **[ux-before-ui](../plugins/ux-before-ui)** | Piensa como un equipo de diseño antes de dibujar nada. Quién llega, qué necesita, cómo lo resuelven los mejores productos. Después, todas las pantallas lado a lado, criticadas y listas para entregar. | Claude Code · Cowork · Codex |
| 🎞️ | **[not-ai-slop](../plugins/not-ai-slop)** | Convierte tu post en un carrusel que no parece hecho por IA. Tú apruebas cada palabra antes, y las imágenes siguen tu marca. | **Codex** (imágenes integradas) · Claude Code · Cowork |
| 🔬 | **[mcp-eval](../plugins/mcp-eval)** | Averigua si Claude sabe usar de verdad tu servidor MCP y te da un veredicto sin rodeos: sale o no sale. | Claude Code |

Vienen más en camino. Añade el marketplace una vez y los plugins nuevos aparecen solos.

## En marcha en dos minutos

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

**Claude Cowork** (la app de escritorio de Claude)

Ve a Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → pega `EllypsisAI/ellypsis-plugin-labs` → instala lo que quieras.

**ChatGPT Codex** (app o CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**O no te compliques.** Pega esto en Claude Code o Codex y deja que se encargue:

> Añade el marketplace de plugins de github.com/EllypsisAI/ellypsis-plugin-labs e instala ux-before-ui desde ahí.

Luego pide lo que quieras, con tus propias palabras. El plugin adecuado se activa solo. También puedes llamarlo por su nombre, como `/ux-before-ui`.

## Por qué esto le gana a un buen prompt

Un prompt le dice a tu agente qué quieres. Un plugin le enseña cómo lo abordaría un experto, y eso es justo lo que no cabe en una caja de chat.

- **Criterio, no checklists.** Tu agente adapta el método a tu caso en vez de rellenar una plantilla.
- **Tú tienes la última palabra.** Los planes, el texto de las diapositivas y todo lo que cambie algo en el mundo real esperan tu visto bueno.
- **Cero datos inventados.** Si no lo sabe, lo dice.

## Quiénes somos

Somos [Ellypsis](https://ellypsis.dk), un pequeño estudio danés de IA. Creamos plugins expertos para equipos que trabajan con IA a diario. Este marketplace es la parte que cualquiera puede usar, gratis y con licencia MIT.

¿Algún bug o alguna idea? Abre un issue y pon el nombre del plugin en el título.
