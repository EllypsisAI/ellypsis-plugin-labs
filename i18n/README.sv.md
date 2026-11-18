<p align="center">
  <img src="../assets/banner.png" alt="Ellypsis Plugin Labs: expertmetoder för din AI-agent" width="100%">
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
  <b>Svenska</b> ·
  <a href="README.no.md">Norsk</a> ·
  <a href="README.fr.md">Français</a> ·
  <a href="README.es.md">Español</a>
</p>

---

Be din AI-agent om ett registreringsflöde, så ritar den ett åt dig. Den frågar inte vem som ska registrera sig, vad de är nervösa för eller varför hälften hoppar av vid steg två. Den kan lite om allt, men inte mycket om något.

**Plugin Labs ger den spetskompetensen.** Varje plugin fångar hur ett proffs faktiskt jobbar: vilka frågor som ställs först, vilka misstag man har lärt sig undvika och i vilken ordning saker görs. Installera en gång, så kliver det in så fort du ber om den sortens jobb. Du pratar med din agent precis som vanligt. Den slutar bara köra på en höft.

## Det här ingår

| | Plugin | Det här gör det för dig | Funkar i |
|:-:|---|---|---|
| 🧭 | **[ux-before-ui](../plugins/ux-before-ui)** | Tänker som ett designteam innan något ritas. Vem som kommer, vad de behöver, hur de bästa produkterna löser det. Sedan alla skärmar sida vid sida, granskade och redo att lämnas över. | Claude Code · Cowork · Codex |
| 🎞️ | **[not-ai-slop](../plugins/not-ai-slop)** | Gör om ditt inlägg till en karusell som inte ser AI-gjord ut. Du godkänner varje ord först, och bilderna följer ditt varumärke. | **Codex** (bilder inbyggt) · Claude Code · Cowork |
| 🔬 | **[mcp-eval](../plugins/mcp-eval)** | Tar reda på om Claude faktiskt kan använda din MCP-server och ger dig ett rakt besked: shippa eller låt bli. | Claude Code |

Fler är på gång. Lägg till marketplacen en gång, så dyker nya plugins upp av sig själva.

## Igång på två minuter

**Claude Code**

```
/plugin marketplace add EllypsisAI/ellypsis-plugin-labs
/plugin install ux-before-ui@ellypsis-labs
```

**Claude Cowork** (Claudes skrivbordsapp)

Customize → Browse plugins → Personal → **+** → Add marketplace from GitHub → klistra in `EllypsisAI/ellypsis-plugin-labs` → installera det du vill ha.

**ChatGPT Codex** (app eller CLI)

```
codex plugin marketplace add EllypsisAI/ellypsis-plugin-labs
codex plugin add not-ai-slop@ellypsis-labs
```

**Eller hoppa över alltihop.** Klistra in det här i Claude Code eller Codex och låt den göra jobbet:

> Lägg till plugin-marketplacen på github.com/EllypsisAI/ellypsis-plugin-labs och installera ux-before-ui därifrån.

Sedan ber du bara om det du vill ha, med dina egna ord. Rätt plugin hakar på. Du kan också kalla på ett vid namn, till exempel `/ux-before-ui`.

## Därför slår det en bra prompt

En prompt talar om för agenten vad du vill ha. Ett plugin lär den hur en expert skulle gå till väga. Och det får helt enkelt inte plats i en chattruta.

- **Omdöme, inte checklistor.** Agenten anpassar metoden efter ditt fall i stället för att fylla i en mall.
- **Du bestämmer.** Planer, texten på dina slides och allt som får verkliga följder väntar på ditt ja.
- **Inga påhittade fakta.** Vet den inte, så säger den det.

## Vilka ligger bakom?

Vi är [Ellypsis](https://ellypsis.dk), en liten dansk AI-studio. Vi bygger expert-plugins för team som jobbar med AI varje dag. Den här marketplacen är den del som alla får använda, gratis och MIT-licensierad.

Hittat en bugg eller fått en idé? Öppna en issue och skriv pluginnamnet i rubriken.
