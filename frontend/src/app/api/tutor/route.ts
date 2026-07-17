import { NextRequest, NextResponse } from 'next/server'
import OpenAI from 'openai'

const SYSTEM_PROMPT = `You are Aku, an expert AI fashion tutor and tailoring coach.
Your mission: teach tailors, fashion students, and learners in a warm,
encouraging, step-by-step style — especially those in low-resource settings.

Guidelines:
- Always teach, don't just answer. Break every technique into numbered steps.
- Name the skill being practised (e.g. "This is called a 'Hong Kong seam finish'").
- Suggest what to practise offline when internet is unavailable.
- Celebrate progress: acknowledge when a learner masters a technique.
- When generating patterns, output precise measurements in centimetres.
- Skill tags: at the END of every response, output a JSON block like:
  \`\`\`skill_tags
  ["zipper", "ankara-finishing", "hidden-stitch"]
  \`\`\`

Language: English (Pidgin/Yoruba/Hausa code-switching welcome if the learner uses it).`

export async function POST(req: NextRequest) {
  const { messages, imageBase64 } = await req.json()

  const apiKey = process.env.OPENAI_API_KEY
  if (!apiKey) {
    // Return rich stub response for demo mode
    return NextResponse.json(stubResponse(messages.at(-1)?.content ?? ''))
  }

  const client = new OpenAI({ apiKey })

  // Build messages — support multimodal (image) input
  const builtMessages: OpenAI.Chat.ChatCompletionMessageParam[] = [
    { role: 'system', content: SYSTEM_PROMPT },
    ...messages.slice(0, -1),
  ]

  const lastUserContent = messages.at(-1)?.content ?? ''
  if (imageBase64) {
    builtMessages.push({
      role: 'user',
      content: [
        { type: 'text', text: lastUserContent || 'Analyse this garment and provide pattern + sewing instructions.' },
        { type: 'image_url', image_url: { url: imageBase64 } },
      ],
    })
  } else {
    builtMessages.push({ role: 'user', content: lastUserContent })
  }

  const t0 = Date.now()
  const completion = await client.chat.completions.create({
    model: process.env.MODEL_NAME ?? 'gpt-4o',
    messages: builtMessages,
    max_tokens: 1024,
    temperature: 0.7,
    stream: false,
  })

  const text = completion.choices[0].message.content ?? ''
  const skill_tags = extractSkillTags(text)

  return NextResponse.json({
    text,
    skill_tags,
    latency_ms: Date.now() - t0,
    model: completion.model,
    tokens: completion.usage?.total_tokens ?? 0,
  })
}

function extractSkillTags(text: string): string[] {
  try {
    const start = text.indexOf('```skill_tags') + '```skill_tags'.length
    const end = text.indexOf('```', start)
    return JSON.parse(text.slice(start, end).trim())
  } catch {
    return []
  }
}

function stubResponse(userMessage: string) {
  const msg = userMessage.toLowerCase()
  let text = ''

  if (msg.includes('zipper') || msg.includes('zip')) {
    text = STUB_ZIPPER
  } else if (msg.includes('dart')) {
    text = STUB_DART
  } else if (msg.includes('sleeve')) {
    text = STUB_SLEEVE
  } else if (msg.includes('pattern') || msg.includes('draft')) {
    text = STUB_PATTERN
  } else {
    text = STUB_DEFAULT
  }

  return {
    text,
    skill_tags: extractSkillTags(text),
    latency_ms: 0,
    model: 'stub (no API key)',
    tokens: 0,
  }
}

const STUB_ZIPPER = `Great question! Let's master the **hidden/invisible zipper** — one of the most prized finishing techniques. 🧵

**Skill: Invisible Zipper Installation**

**Step-by-Step:**
1. **Press the zipper coils open** — run a warm iron along the zipper teeth to uncurl them. This is the secret most beginners miss!
2. **Mark your seam allowance** — chalk a 1.5 cm seam line on both fabric panels.
3. **Pin zipper face-down** — place the right side of the zipper against the right side of fabric, coils ON the seam line.
4. **Sew the first side** — stitch from the top tape down toward the zipper pull, stopping 2 cm from the bottom.
5. **Repeat on second side** — close the zipper before pinning the second panel for alignment.
6. **Close the seam below** — switch to a regular presser foot, complete the seam beneath the zipper.

**Practice tip (offline):** Practise on scrap fabric 3× before touching your ankara. Muscle memory is everything here.

\`\`\`skill_tags
["invisible-zipper", "zipper-installation", "ankara-finishing", "seam-technique"]
\`\`\``

const STUB_DART = `Excellent! Darts are the foundation of fitted garments. 🪡

**Skill: Sewing Darts**

**Step-by-Step (Straight Dart):**
1. **Mark your dart** — transfer all dart markings from pattern to fabric using tailor's chalk.
2. **Fold the dart** — fold fabric RIGHT sides together, matching the two leg lines exactly.
3. **Pin from wide end to tip** — pin perpendicular to the stitching line.
4. **Stitch** — sew from the wide end, tapering to a sharp point at the tip.
5. **Secure the tip** — tie off thread ends (don't backstitch at the tip — it creates a bump).
6. **Press** — press bust darts downward, waist darts toward centre.

\`\`\`skill_tags
["dart", "bust-dart", "waist-dart", "garment-fitting", "tailoring-basics"]
\`\`\``

const STUB_SLEEVE = `Sleeves can feel intimidating — but once you understand **ease**, it clicks! 💪

**Skill: Setting In Sleeves**

**Key concept: Ease** — The sleeve head is slightly LARGER than the armhole. That extra fabric allows arm movement.

**Step-by-Step:**
1. **Staystitch the sleeve cap** — two rows of basting stitches between the notches.
2. **Pull the basting threads** — gently gather the sleeve cap to match armhole circumference.
3. **Pin sleeve into armhole** — match shoulder seam to sleeve cap notch.
4. **Ease check** — smooth from the RIGHT side. No tucks, no puckers.
5. **Sew with sleeve on TOP** — always stitch with sleeve facing you to control the ease.
6. **Press seam INTO the sleeve** — never press the ease flat.

\`\`\`skill_tags
["sleeve-setting", "ease", "armhole", "garment-construction"]
\`\`\``

const STUB_PATTERN = `Let's draft your pattern! 📐

**Skill: Pattern Drafting — Basic Bodice Block**

For a standard size 12 (88cm bust):

\`\`\`python
# Generated by Codex — pattern_math.py
def bodice_block(bust_cm: float, waist_cm: float, back_length_cm: float) -> dict:
    """Calculate key points for a basic bodice block."""
    half_bust = bust_cm / 2
    half_waist = waist_cm / 2
    return {
        "back_width": half_bust / 2 + 0.5,
        "front_width": half_bust / 2 + 1.0,
        "side_seam_length": back_length_cm - 2,
        "dart_intake": half_bust - half_waist,
    }
\`\`\`

Use the /design page to generate a full SVG pattern!

\`\`\`skill_tags
["pattern-drafting", "bodice-block", "garment-math", "measurements"]
\`\`\``

const STUB_DEFAULT = `Welcome to **Aku** — your AI Fashion Tutor! 🎓✂️

I'm here to teach you tailoring and fashion design, step by step.

**Try asking me:**
- "How do I sew an invisible zipper?"
- "Teach me about darts"
- "How do I set in sleeves?"
- "Help me draft a bodice pattern"

**Works offline too** — your lessons are saved locally. 📴

\`\`\`skill_tags
["welcome", "onboarding"]
\`\`\``
