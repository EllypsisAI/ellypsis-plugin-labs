<p align="center">
  <img src="../assets/banner.png" alt="Ellypsis Plugin Labs: Expertenmethoden für deinen KI-Agenten" width="100%">
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
  <b>Deutsch</b> ·
  <a href="README.sv.md">Svenska</a> ·
  <a href="README.no.md">Norsk</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

---

Bitte deinen KI-Agenten um einen Signup-Flow, und er zeichnet dir einen. Er fragt nicht, wer sich da anmeldet, was die Leute verunsichert oder warum die Hälfte bei Schritt zwei abspringt. Er kann von allem ein bisschen und nichts so richtig.

**Plugin Labs liefert die Expertise.** Jedes Plugin zeigt, wie Fachleute wirklich arbeiten: welche Fragen sie zuerst stellen, welche Fehler sie längst nicht mehr machen, in welcher Reihenfolge sie vorgehen. Einmal installiert, springt es an, sobald du diese Art Arbeit anfragst. Du redest mit deinem Agenten wie immer. Nur wurstelt er nicht mehr einfach drauflos.

## Das steckt drin

| | Plugin | Was es für dich tut | Läuft in |
|:-:|---|---|---|
| 🧭 | **[ux-before-ui](../plugins/ux-before-ui)** | Denkt wie ein Designteam, bevor es irgendetwas zeichnet. Wer kommt, was braucht diese Person, wie lösen die besten Produkte das? Danach alle Screens nebeneinander, kritisch geprüft und übergabefertig. | Claude Code · Cowork · Codex |
| 🎞️ | **[not-ai-slop](../plugins/not-ai-slop)** | Macht aus deinem Post ein Karussell, das nicht nach KI aussieht. Du gibst vorher jedes Wort frei, und die Bilder folgen deiner Marke. | **Codex** (Bilder inklusive) · Claude Code · Cowork |
| 🔬 | **[mcp-eval](../plugins/mcp-eval)** | Findet heraus, ob Claude deinen MCP-Server wirklich nutzen kann, und sagt dir klipp und klar: Go oder No-Go. | Claude Code |

Weitere sind schon unterwegs. Füg den Marketplace einmal hinzu, und neue Plugins tauchen einfach auf.

## In zwei Minuten startklar

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

**Claude Cowork** (die Claude-Desktop-App)

Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → `EllypsisAI/ellypsis-plugin-labs` einfügen → installieren, was du willst.

**ChatGPT Codex** (App oder CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**Oder mach's dir bequem.** Kopier das hier in Claude Code oder Codex und lass den Agenten die Arbeit machen:

> Füge den Plugin-Marketplace unter github.com/EllypsisAI/ellypsis-plugin-labs hinzu und installiere daraus ux-before-ui.

Danach sagst du einfach in deinen eigenen Worten, was du willst. Das passende Plugin übernimmt. Du kannst eins auch direkt beim Namen rufen, etwa `/ux-before-ui`.

## Warum das mehr bringt als ein guter Prompt

Ein Prompt sagt deinem Agenten, was du willst. Ein Plugin bringt ihm bei, wie ein Profi an die Sache rangehen würde. Und genau das passt in kein Chatfenster.

- **Urteilsvermögen statt Checklisten.** Dein Agent passt die Methode an deinen Fall an, statt eine Vorlage auszufüllen.
- **Du hast das letzte Wort.** Pläne, Slide-Texte und alles, was in der echten Welt etwas verändert, warten auf dein Ja.
- **Keine erfundenen Fakten.** Wenn er etwas nicht weiß, sagt er das.

## Wer dahintersteckt

Wir sind [Ellypsis](https://ellypsis.dk), ein kleines KI-Studio aus Dänemark. Wir bauen Experten-Plugins für Teams, die jeden Tag mit KI arbeiten. Dieser Marketplace ist der Teil, den alle nutzen können: kostenlos und unter MIT-Lizenz.

Bug gefunden oder eine Idee? Mach ein Issue auf und nenn das Plugin im Titel.
