<p align="center">
  <img src="../assets/banner.png" alt="Ellypsis Plugin Labs: ekspertmetoder for AI-agenten din" width="100%">
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
  <b>Norsk</b> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

---

Be AI-agenten din om en registreringsflyt, så tegner den en. Den spør ikke hvem som skal registrere seg, hva de er usikre på, eller hvorfor halvparten faller fra på steg to. Den kan litt om alt, men ingenting skikkelig.

**Plugin Labs gir den ekspertisen.** Hver plugin er måten en spesialist faktisk jobber på: spørsmålene de stiller først, feilene de har lært å unngå, rekkefølgen de gjør ting i. Installer den én gang, så trår den til hver gang du ber om den typen jobb. Du snakker med agenten din akkurat som før. Den slutter bare å skyte fra hofta.

## Dette får du

| | Plugin | Hva den gjør for deg | Fungerer i |
|:-:|---|---|---|
| 🧭 | **[ux-before-ui](../plugins/ux-before-ui)** | Tenker som et designteam før den tegner noe som helst. Hvem som kommer, hva de trenger, hvordan de beste produktene løser det. Så alle skjermene side om side, kritisert og klare til overlevering. | Claude Code · Cowork · Codex |
| 🎞️ | **[not-ai-slop](../plugins/not-ai-slop)** | Gjør innlegget ditt om til en karusell som ikke ser AI-laget ut. Du godkjenner hvert ord først, og bildene følger merkevaren din. | **Codex** (bilder innebygd) · Claude Code · Cowork |
| 🔬 | **[mcp-eval](../plugins/mcp-eval)** | Finner ut om Claude faktisk klarer å bruke MCP-serveren din, og gir deg en ærlig dom: shippe eller ikke shippe. | Claude Code |

Flere er på vei. Legg til markedsplassen én gang, så dukker nye plugins bare opp.

## Oppe og går på to minutter

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

**Claude Cowork** (Claude-appen for desktop)

Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → lim inn `EllypsisAI/ellypsis-plugin-labs` → installer det du vil ha.

**ChatGPT Codex** (app eller CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**Orker du ikke?** Lim inn dette i Claude Code eller Codex, og la den gjøre jobben:

> Legg til plugin-markedsplassen på github.com/EllypsisAI/ellypsis-plugin-labs og installer ux-before-ui derfra.

Så ber du bare om det du vil ha, med dine egne ord. Riktig plugin tar ballen. Du kan også kalle på en ved navn, for eksempel `/ux-before-ui`.

## Derfor slår dette en god prompt

En prompt forteller agenten hva du vil ha. En plugin lærer den hvordan en ekspert ville gått fram, og det får du ikke plass til i en chatboks.

- **Skjønn, ikke sjekklister.** Agenten tilpasser metoden til din situasjon i stedet for å fylle ut en mal.
- **Du har styringen.** Planer, teksten på slidene og alt som endrer noe ute i den virkelige verden, venter på et ja fra deg.
- **Ingen oppdiktede fakta.** Vet den ikke, sier den det.

## Hvem står bak

Vi er [Ellypsis](https://ellypsis.dk), et lite dansk AI-studio. Vi bygger ekspertplugins for team som jobber med AI hver dag. Denne markedsplassen er delen alle kan bruke, gratis og MIT-lisensiert.

Har du funnet en bug eller fått en idé? Åpne en issue og skriv navnet på pluginen i tittelen.
