# tipsofday — landing page copy

Drop these blocks into any static page. English first, then pt-BR (the primary market).

---

## Hero (EN)

# Your morning crypto briefing, written by AI that runs on *your* machine.

One command. Today's news, real market data, and a local open-weight model that tells you
which asset the news flow points at — with evidence, confidence, and what would prove it
wrong. No API bills. No watchlist leaving your laptop. No "best investment" nonsense.

**`tipsofday` — information, not investment advice.**

[ Install in 2 minutes ]  [ See a sample briefing ]  [ GitHub ]

## The three promises

1. **Local by default.** The AI step runs on your PC. The only thing that needs the
   internet is the news and price fetch.
2. **Numbers never come from the model.** Prices, volumes and the Fear & Greed index come
   from public APIs, and every number in the output is checked against them.
3. **"No clear signal today" is allowed.** When the news is thin or contradictory, the app
   says so instead of forcing a pick.

## How it works

Fetch today's RSS + market data → summarize each article → aggregate the news signal in
plain Python → one local model writes the briefing → guardrails check every number and
every word → you read it. Details and a diagram in the README.

## What you get every day

- **Market mood** in two sentences.
- **Top stories** with a link to each source.
- **Asset in focus** with the reasons, the evidence, a confidence level, the risks, and
  what would invalidate the call.
- **Runners-up.**
- Your **track record** over time (Pro): how each day's focus actually did, versus BTC.

## FAQ

**Do I need a GPU?** No. A 4B-class Q4 model runs on CPU. A GPU makes it ~10× faster.

**What does it cost?** Free every day for one briefing. Pro is for power users: custom
watchlists, history, the track record and export.

**Is it financial advice?** No. It is a news summary with a signal label. Crypto is
volatile and you can lose everything. Do your own research.

**What leaves my machine?** Nothing about you. The app fetches public news and prices and
writes history to a local SQLite file. No telemetry.

---

## pt-BR

# Seu resumo diario de cripto, escrito por uma IA que roda no *seu* computador.

Um comando. As noticias do dia, dados reais de mercado, e um modelo local de pesos
abertos que mostra **qual ativo o fluxo de noticias aponta hoje** — com evidencias,
confianca e o que invalidaria o argumento. Sem conta em API. Sem mandar sua watchlist para
fora. Sem promessa de "melhor investimento".

**`tipsofday` — informacao, nao recomendacao de investimento.**

[ Instalar em 2 minutos ]  [ Ver um exemplo de resumo ]  [ GitHub ]

## As tres promessas

1. **Local por padrao.** A etapa de IA roda no seu PC. So a busca de noticias e precos usa
   a internet.
2. **Numeros nunca vem do modelo.** Preco, volume e o indice Fear & Greed vem de APIs
   publicas, e todo numero no texto e conferido contra eles.
3. **"Sem sinal claro hoje" e uma resposta valida.** Quando as noticias sao poucas ou
   contraditorias, o app diz isso em vez de forcar um palpite.

## O que voce recebe todo dia

- **Humor do mercado** em duas frases.
- **Principais noticias**, cada uma com link para a fonte.
- **Destaque do dia**: por que, evidencias, nivel de confianca, riscos e o que
  invalidaria a leitura.
- **Alternativas.**
- Seu **historico** e track record (Pro): como cada destaque realmente foi, contra o BTC.

## Perguntas frequentes

**Preciso de placa de video?** Nao. Um modelo 4B em Q4 roda na CPU. Com GPU fica ~10x
mais rapido.

**Quanto custa?** Um resumo por dia e gratis. O Pro e para quem usa todo dia: watchlist
propria, historico, track record e exportacao.

**E recomendacao de investimento?** Nao. E um resumo de noticias com um rotulo de sinal.
Cripto e muito volatil e voce pode perder todo o capital. Faca sua propria pesquisa.
