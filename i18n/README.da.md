<p align="center">
  <img src="../assets/banner.png" alt="Ellypsis Plugin Labs: ekspertmetoder til din AI-agent" width="100%">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude_Code-works-7c3f63?style=flat-square" alt="Claude Code">
  <img src="https://img.shields.io/badge/Claude_Cowork-works-7c3f63?style=flat-square" alt="Claude Cowork">
  <img src="https://img.shields.io/badge/ChatGPT_Codex-works-7c3f63?style=flat-square" alt="ChatGPT Codex">
  <img src="https://img.shields.io/badge/license-MIT-191713?style=flat-square" alt="MIT license">
</p>

<p align="center">
  <a href="../README.md">English</a> ·
  <b>Dansk</b> ·
  <a href="README.de.md">Deutsch</a> ·
  <a href="README.sv.md">Svenska</a> ·
  <a href="README.no.md">Norsk</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

---

Bed din AI-agent om et signup-flow, og du får et. Den spørger ikke, hvem der skal oprette sig, hvad de er nervøse for, eller hvorfor halvdelen falder fra ved trin to. Den kan lidt af det hele og intet til bunds.

**Plugin Labs giver den ekspertisen.** Hvert plugin er sådan, en specialist rent faktisk arbejder: de spørgsmål, de stiller først, de fejl, de har lært at undgå, og rækkefølgen, de gør tingene i. Installér det én gang, så træder det til, hver gang du beder om den slags opgave. Du taler med din agent, som du plejer. Den holder bare op med at skyde fra hoften.

## Det er der i kassen

| | Plugin | Hvad det gør for dig | Virker i |
|:-:|---|---|---|
| 🧭 | **[ux-before-ui](../plugins/ux-before-ui)** | Tænker som et designteam, før det tegner noget som helst. Hvem kommer forbi, hvad har de brug for, og hvordan løser de bedste produkter det? Derefter alle skærme side om side, gennemgået kritisk og klar til handoff. | Claude Code · Cowork · Codex |
| 🎞️ | **[not-ai-slop](../plugins/not-ai-slop)** | Gør dit opslag til en karrusel, der ikke ligner AI-arbejde. Du godkender hvert ord først, og billederne følger dit brand. | **Codex** (billeder indbygget) · Claude Code · Cowork |
| 🔬 | **[mcp-eval](../plugins/mcp-eval)** | Finder ud af, om Claude rent faktisk kan bruge din MCP-server, og giver dig en ærlig dom: klar til at shippe eller ej. | Claude Code |

Der er flere på vej. Tilføj marketplacet én gang, så dukker nye plugins bare op.

## Kom i gang på to minutter

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

**Claude Cowork** (Claudes desktopapp)

Gå til Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → indsæt `EllypsisAI/ellypsis-plugin-labs` → installér det, du har lyst til.

**ChatGPT Codex** (app eller CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**Gider du ikke selv?** Indsæt det her i Claude Code eller Codex, og lad den klare resten:

> Tilføj plugin-marketplacet på github.com/EllypsisAI/ellypsis-plugin-labs, og installér ux-before-ui derfra.

Derefter beder du bare om det, du vil have, med dine egne ord. Det rigtige plugin griber bolden. Du kan også kalde et ved navn, fx `/ux-before-ui`.

## Derfor slår det en god prompt

En prompt fortæller din agent, hvad du vil have. Et plugin lærer den, hvordan en ekspert ville tackle opgaven, og det er den del, du ikke kan proppe ned i en chatboks.

- **Dømmekraft, ikke tjeklister.** Din agent tilpasser metoden til din situation i stedet for at udfylde en skabelon.
- **Du bestemmer.** Planer, teksten på dine slides og alt, der ændrer noget i den virkelige verden, venter på dit ja.
- **Ingen opdigtede fakta.** Ved den det ikke, siger den det.

## Hvem står bag?

Vi er [Ellypsis](https://ellypsis.dk), et lille dansk AI-studie. Vi bygger ekspert-plugins til teams, der arbejder med AI hver dag. Det her marketplace er den del, alle kan bruge. Gratis og MIT-licenseret.

Fundet en fejl eller fået en idé? Opret et issue, og skriv pluginnets navn i titlen.
